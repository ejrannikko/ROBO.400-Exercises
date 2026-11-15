"""
This code uses the Go to Goal turtlebot controller from:
https://wiki.ros.org/turtlesim/Tutorials/Go%20to%20Goal
as a basis. The code has been modified from rospy to rclpy to work with ROS2.
Instead of replacing all Pose type variables from the base code,
we use Odometry to get the data and then transfer it into Pose type in code.
This way we can preserve as much of the base code as possible. 
"""
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
# Use Odometry for position and orientation data
from nav_msgs.msg import Odometry
from turtlesim.msg import Pose

from math import pow, atan2, sqrt, exp, sin, cos
from time import sleep

import csv


class TurtleBot(Node):

    def __init__(self):
        super().__init__('turtlebot_controller')

        # Publisher for turtle velocity commands.
        self.velocity_publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Subscriber for the turtle's current pose.
        self.pose_subscriber = self.create_subscription(
            Odometry,
            '/odom',
            self.update_pose,
            10
        )

        self.pose = Pose()
        self.goal_pose = Pose()
        self.vel_msg = Twist()
        self.odom = None
        self.get_logger().info('TurtleBot controller initialized.')
        # Set default tolerances
        self.angle_tolerance = 0.01
        self.distance_tolerance = 0.01

        # Different objectives for the turtle
        self.position_objective = 1
        self.full_pose_objective = 2
        self.trajectory_objective = 3

        self.vel_publish_timer = self.create_timer(0.05, self.publish_velocity)

    def publish_velocity(self):
        self.velocity_publisher.publish(self.vel_msg)

    def update_pose(self, msg):
        """Callback function for receiving the turtle's pose."""
        self.odom = msg
        self.pose.x = round(self.odom.pose.pose.position.x, 4)
        self.pose.y = round(self.odom.pose.pose.position.y, 4)
        q = msg.pose.pose.orientation
        # Extract yaw from quaternion.
        self.pose.theta = 2.0 * atan2(q.z, q.w)

    def euclidean_distance(self, goal_pose):
        """Calculate the distance between the turtle and the goal."""

        return sqrt(
            pow(goal_pose.x - self.pose.x, 2) +
            pow(goal_pose.y - self.pose.y, 2)
        )

    def steering_angle(self, goal_pose):
        """Calculate the angle toward the goal."""

        return atan2(
            goal_pose.y - self.pose.y,
            goal_pose.x - self.pose.x
        )

    def angle_error(self, goal_angle):
        """Calculate error of current and desired heading angle"""
        angle_difference = (
            goal_angle - self.pose.theta
        )

        # Normalize the angle to the range [-pi, pi].
        angle_difference = atan2(
            sin(angle_difference),
            cos(angle_difference)
        )
        return angle_difference

    def linear_vel(self, goal_pose, control_mode, kp = 2, min_vel = 0.1, max_vel = 0.5):
        """Calculate the linear velocity."""
        dist_diff = self.euclidean_distance(goal_pose)
        # Function to slow down when close to the goal. Values: [0, 1]
        #if control_mode == "dynamic":
        #    gain = 1-exp(-beta*dist_diff)
        #elif control_mode == "proportional":
        #    gain = 0.5
        #else:
        #    self.get_logger().info("Non-valid control mode selected!")
        #    gain = 0
        return max(min_vel, min(kp * dist_diff, max_vel))

    def angular_vel(self, goal_angle, kp = 3, max_ang_vel = 2.0):
        """Calculate the angular velocity."""
        angle_difference = self.angle_error(goal_angle)
        # Function to slow down when close to the goal. Values: [0, 1]
        # dynamic_gain = 1-exp(-beta*abs(angle_difference))
        return max(-max_ang_vel, min(kp * angle_difference, max_ang_vel))

    def get_user_input(self):
        """
        Prompts user to choose what type of objective should the turtle aim for.
        The objectives are the subojectives found in task 2.2:
        - Go to point [x, y]
        - Go to point [x, y, theta]
        - Follow trajectory [x, y, theta]
        """
        objective_is_valid = False
        while not objective_is_valid:
            objective = int(input('1: [x,y]\n' \
                                  '2: [x,y,theta]\n' \
                                  '3: trajectory\n'
                                  'Select objective (1/2/3): '))
            if objective in [self.position_objective, 
                             self.full_pose_objective, 
                             self.trajectory_objective]:
                objective_is_valid = True
            else:
                self.get_logger().error("Non-valid objective!")

        if objective != self.trajectory_objective:
            # Get the goal coordinates from the user.
            self.goal_pose.x = float(input('Set your x goal: '))
            self.goal_pose.y = float(input('Set your y goal: '))
            # self.distance_tolerance = float(input('Set your distance tolerance (e.g. 0.01): '))
            # Additionally ask for desired angle if that is the objective
            if objective == self.full_pose_objective:
                self.goal_pose.theta = float(input('Set your theta (rad) goal: '))
                # self.angle_tolerance = float(input('Set your angle tolerance (e.g. 0.01): '))

        return objective

    def move2goal(self, control_mode):
        """Move the turtle to the specified goal."""

        try:
            while (self.euclidean_distance(self.goal_pose) > self.distance_tolerance):
                # Check for callbacks and execute them
                rclpy.spin_once(self, timeout_sec = 0.05)

                # Calculate linear velocity.
                self.vel_msg.linear.x = self.linear_vel(self.goal_pose, control_mode)

                # Calculate angular velocity.
                goal_angle = self.steering_angle(self.goal_pose)
                self.vel_msg.angular.z = self.angular_vel(goal_angle)

        except KeyboardInterrupt:
            self.get_logger().info('Movement interrupted.')

        # finally:
            # Stop the turtle.
            # self.vel_msg = Twist()
            # self.velocity_publisher.publish(Twist())
            # self.get_logger().info('Goal reached or movement stopped.')

    def move2pose(self):
        """Orients the turtle to face the desired way"""
        try:
            self.goal_pose.theta = self.steering_angle(self.goal_pose)
            self.get_logger().info('Starting pose matching...')
            while (abs(self.angle_error(self.goal_pose.theta)) > self.angle_tolerance):
                rclpy.spin_once(self, timeout_sec = 0.05)
                self.vel_msg.angular.z = self.angular_vel(self.goal_pose.theta)
                # self.velocity_publisher.publish(self.vel_msg)
            self.get_logger().info('Desired orientation reached.')

        except KeyboardInterrupt:
            self.get_logger().info('Movement interrupted.')

        # finally:
            # Stop angular velocity of the turtle.
            # self.vel_msg.angular.z = 0.0
            # self.get_logger().info('Goal reached or movement stopped.')

    
    def move_along_trajectory(self):
        """Move turtle along chosen trajectory"""
        waypoints = self.read_waypoints('circle_trajectory.csv')
        x0, y0 = waypoints[0]
        self.goal_pose.x = x0
        self.goal_pose.y = y0
        self.goal_pose.theta = self.steering_angle(self.goal_pose)
        self.move2pose()
        self.move2goal(control_mode="dynamic")
        self.stop()
        for x, y in waypoints[1:]:
            self.goal_pose.x = x
            self.goal_pose.y = y
            self.goal_pose.theta = self.steering_angle(self.goal_pose)
            self.move2pose()
            self.get_logger().info(f'Moving to waypoint: x={x}, y={y}')
            self.move2goal(control_mode="proportional")
    
    def read_waypoints(self, filename):
        waypoints = []
        with open(filename, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                x = float(row['x'])
                y = float(row['y'])
                waypoints.append((x, y))

        return waypoints

    def stop(self):
        """Create vel_msg to stop turtle"""
        self.vel_msg = Twist()
        rclpy.spin_once(self, timeout_sec=0.05)
        self.get_logger().info("Movement stopped.")

def main(args=None):

    rclpy.init(args=args)
    turtlebot = TurtleBot()

    try:
        objective = turtlebot.get_user_input()
        if objective == turtlebot.position_objective:
            turtlebot.get_logger().info('Moving to goal.')
            turtlebot.move2pose()
            turtlebot.move2goal(control_mode="dynamic")
            turtlebot.stop()
        elif objective == turtlebot.full_pose_objective:
            turtlebot.get_logger().info('Moving to goal.')
            turtlebot.move2pose()
            turtlebot.move2goal(control_mode="dynamic")
            # Wait to make sure turtle has stopped
            sleep(0.5)
            turtlebot.get_logger().info('Moving to pose.')
            turtlebot.move2pose()
            turtlebot.stop()
        elif objective == turtlebot.trajectory_objective:
            turtlebot.move_along_trajectory()
            turtlebot.stop()


    except KeyboardInterrupt:
        turtlebot.stop()
        pass

    finally:
        turtlebot.stop()
        turtlebot.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
