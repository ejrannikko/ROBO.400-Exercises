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

# Used for acessing csv trajectory files
from ament_index_python.packages import get_package_share_directory
import os


from std_msgs.msg import Float32
from geometry_msgs.msg import Twist, Vector3Stamped
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

        # Publisher for position error
        self.position_error_publisher = self.create_publisher(
            Float32,
            '/controller/position_error',
            10
        )

        # Publisher for orientation error
        self.orientation_error_publisher = self.create_publisher(
            Float32,
            '/controller/orientation_error',
            10
        )

        self.pose = Pose()
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
        self.quit_objective = 4

        self.vel_publish_timer = self.create_timer(0.05, self.publish_velocity)

    def wait_for_odom(self):
        """Wait to ensure that odometry data is received"""
        self.get_logger().info('Waiting for odometry data...')

        while rclpy.ok() and self.odom is None:
            rclpy.spin_once(self, timeout_sec=0.1)

        self.get_logger().info(
            f'Odometry received: x={self.pose.x:.3f}, '
            f'y={self.pose.y:.3f}, theta={self.pose.theta:.3f}'
        )


    def publish_error(self, position_error, orientation_error):
        """Publish errors to their respective topics"""

        pos_error_msg = Float32()
        orient_error_msg = Float32()
        pos_error_msg.data = float(position_error)
        orient_error_msg.data = float(orientation_error)
        self.position_error_publisher.publish(pos_error_msg)
        self.orientation_error_publisher.publish(orient_error_msg)


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

    def euclidean_distance(self, x, y):
        """Calculate the distance between the turtle and the goal."""

        return sqrt(
            pow(x - self.pose.x, 2) +
            pow(y - self.pose.y, 2)
        )

    def steering_angle(self, x, y):
        """Calculate the angle toward the goal."""

        return atan2(
            y - self.pose.y,
            x - self.pose.x
        )

    def angle_error(self, theta):
        """Calculate error of current and desired heading angle"""
        angle_difference = (
            theta - self.pose.theta
        )

        # Normalize the angle to the range [-pi, pi].
        angle_difference = atan2(
            sin(angle_difference),
            cos(angle_difference)
        )
        return angle_difference

    def linear_vel(self, x, y, kp = 2, min_vel = 0.1, max_vel = 0.5):
        """Calculate the linear velocity."""
        dist_diff = self.euclidean_distance(x, y)
    
        return max(min_vel, min(kp * dist_diff, max_vel))

    def angular_vel(self, goal_angle, kp = 3, max_ang_vel = 2.0):
        """Calculate the angular velocity."""
        angle_difference = self.angle_error(goal_angle)
        return max(-max_ang_vel, min(kp * angle_difference, max_ang_vel))

    def get_user_input(self):
        """
        Prompts user to choose what type of objective should the turtle aim for.
        The objectives are the subojectives found in task 2.2:
        - Go to point [x, y]
        - Go to point [x, y, theta]
        - Follow trajectory [x, y, theta]
            - Choose trajectory type [circle, square, spline]
            - Choose how to follow trajectory [point-to-point, smooth]
        """
        # Set placeholder values for all possible user inputs
        x = 0
        y = 0
        theta = 0
        objective = 0
        trajectory = ""
        follow_mode = ""

        valid_objective = False
        while not valid_objective:
            objective = int(input('1: [x,y]\n' \
                                  '2: [x,y,theta]\n' \
                                  '3: trajectory\n' \
                                  '4: quit\n' \
                                  'Select objective (1/2/3/4): '))
            # Exit if quit chosen
            if objective == self.quit_objective:
                return x, y, theta, objective, trajectory, follow_mode
            elif objective in [self.position_objective, 
                             self.full_pose_objective, 
                             self.trajectory_objective]:
                valid_objective = True
            else:
                self.get_logger().error("Non-valid objective!")

        if objective != self.trajectory_objective:
            # Get the goal coordinates from the user.
            x = float(input('Set your x goal: '))
            y = float(input('Set your y goal: '))
            # Additionally ask for desired angle if that is the objective
            if objective == self.full_pose_objective:
                theta = float(input('Set your theta (rad) goal: '))
        else:
            valid_trajectory = False
            while not valid_trajectory:
                trajectory = input('Choose trajectory type (circle/square/spline): ')
                if trajectory not in ["circle", "square", "spline"]:
                    self.get_logger().error("Non-valid trajectory type!")
                else:
                    valid_trajectory = True
            valid_follow_mode = False
            while not valid_follow_mode:
                follow_mode = input('Choose follow mode (p2p/smooth): ')
                if follow_mode not in ["p2p", "smooth"]:
                    self.get_logger().error("Non-valid follow mode!")
                else:
                    valid_follow_mode = True
            

        return x, y, theta, objective, trajectory, follow_mode

    def move2goal(self, x, y):
        """Move the turtle to the specified goal."""
        try:
            self.get_logger().info(f'Moving to goal point: [x: {x:.2f}, y: {y:.2f}]')
            # Keep moving towards goal point until within tolerance
            while (self.euclidean_distance(x, y) > self.distance_tolerance):
                # Check for callbacks and execute them
                rclpy.spin_once(self, timeout_sec = 0.05)
                
                # Calculate linear velocity.
                position_error = self.euclidean_distance(x, y)
                self.vel_msg.linear.x = self.linear_vel(x, y)

                # Calculate angular velocity.
                goal_angle = self.steering_angle(x, y)
                orientation_error = self.angle_error(goal_angle)
                self.vel_msg.angular.z = self.angular_vel(goal_angle)

                # Publish errors
                self.publish_error(position_error, orientation_error)

            self.get_logger().info(f'Goal reached.')

        except KeyboardInterrupt:
            self.get_logger().warn('Movement interrupted.')

    def move2pose(self, theta):
        """Orients the turtle to face the desired way"""
        try:
            self.get_logger().info(f'Orienting to goal angle: {theta:.2f} rad')
            # Keep moving towards goal orientation until angle error within tolerance
            while (abs(self.angle_error(theta)) > self.angle_tolerance):
                rclpy.spin_once(self, timeout_sec = 0.05)
                # Publish error for plotting
                orientation_error = self.angle_error(theta)
                self.publish_error(0.0, orientation_error)
                # Publish angular velocity command
                self.vel_msg.angular.z = self.angular_vel(theta)
            self.get_logger().info('Desired orientation reached.')

        except KeyboardInterrupt:
            self.get_logger().warn('Movement interrupted.')

    
    def move_along_trajectory(self, trajectory, follow_mode):
        """
        Move turtle along chosen trajectory
        str trajectory: specifies which trajectory type to follow
        str follow_mode: specifies how the trajectory is followed
        """
        try:
            # Specify trajectory data filename
            match trajectory:
                case "circle":
                    filename = 'circle_trajectory.csv'
                case "square":
                    filename = 'square_trajectory.csv'
                case "spline":
                    filename = 'spline_trajectory.csv'
            
            # Get the installed package directory
            package_share_directory = get_package_share_directory(
                'turtlebot3_controller'
            )

            # Construct the trajectory file path
            trajectory_path = os.path.join(
                package_share_directory,
                'trajectories',
                filename
            )

            # Read trajectory waypoints
            waypoints = self.read_waypoints(trajectory_path)

            # Move to first point on trajectory
            x0, y0 = waypoints[0]
            theta = self.steering_angle(x0, y0)
            self.move2pose(theta)
            self.move2goal(x0, y0)
            self.stop()
            # Choose either point-to-point or smooth trajectory following
            match follow_mode:
                # Moves turtle in order directly from point-to-point. Stops after reaching point.
                case "p2p":
                    for x, y in waypoints[1:]:
                        theta = self.steering_angle(x, y)
                        self.move2pose(theta)
                        self.move2goal(x, y)
                # Moves turtle between zones around points while maintaining some velocity.
                case "smooth":
                    # Trajectory following parameters
                    point_radius = 0.5
                    max_vel = 0.5
                    beta = 2
                    for x, y in waypoints[1:]:
                        # Keep moving towards a point until radius is hit
                        while (self.euclidean_distance(x, y) > point_radius):
                            theta_goal = self.steering_angle(x, y)
                            # Calculate and publish errors for later plotting
                            orientation_error = self.angle_error(theta_goal)
                            position_error = self.euclidean_distance(x, y)
                            self.publish_error(position_error, orientation_error)
                            # Larger angle error, smaller velocity
                            self.vel_msg.linear.x = max_vel * exp(-abs(orientation_error) * beta)
                            self.vel_msg.angular.z = self.angular_vel(theta_goal)
                            rclpy.spin_once(self, timeout_sec = 0.05)
        except KeyboardInterrupt:
            self.get_logger().warn('Movement interrupted')
    
    def read_waypoints(self, filename):
        """Read csv-file specified with filename and append points to waypoints vector"""
        waypoints = []
        with open(filename, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                x = float(row['x'])
                y = float(row['y'])
                waypoints.append((x, y))

        return waypoints

    def stop(self):
        """Stop all turtle movement"""
        self.vel_msg = Twist()
        rclpy.spin_once(self, timeout_sec=0.05)
        self.velocity_publisher.publish(self.vel_msg)
        self.get_logger().info("Movement stopped.")

def main(args=None):

    rclpy.init(args=args)
    turtlebot = TurtleBot()
    turtlebot.wait_for_odom()

    try:
        quit_chosen = False
        while not quit_chosen:
            x, y, theta, objective, trajectory, follow_mode = turtlebot.get_user_input()
            match objective:
                # Move to goal position [x, y]
                case turtlebot.position_objective:
                    turtlebot.get_logger().info(f'Goal received: [x: {x:.2f}, y: {y:.2f}]')
                    # Orient turtlebot to point towards goal point first
                    turtlebot.move2pose(turtlebot.steering_angle(x, y))
                    turtlebot.move2goal(x, y)
                    turtlebot.stop()
                # Move to goal position and orientation [x, y, theta]
                case turtlebot.full_pose_objective:
                    turtlebot.get_logger().info(f'Goal received: [x: {x:.2f}, y: {y:.2f}, theta: {theta:.2f}]')
                    turtlebot.move2pose(turtlebot.steering_angle(x, y))
                    turtlebot.move2goal(x, y)
                    turtlebot.stop()
                    turtlebot.move2pose(theta)
                    turtlebot.stop()
                # Move along chosen trajectory
                case turtlebot.trajectory_objective:
                    turtlebot.get_logger().info(f'Goal received: [trajectory: {trajectory}, follow mode: {follow_mode}]')
                    turtlebot.move_along_trajectory(trajectory, follow_mode)
                    turtlebot.stop()
                # Quit program
                case turtlebot.quit_objective:
                    turtlebot.get_logger().info('Quitting program.')
                    quit_chosen = True
    except KeyboardInterrupt:
        pass

    finally:
        turtlebot.stop()
        turtlebot.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
