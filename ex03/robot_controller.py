"""
This code uses the Go to Goal turtlebot controller from:
https://wiki.ros.org/turtlesim/Tutorials/Go%20to%20Goal
as a basis. The code has been modified from rospy to rclpy to work with ROS2.
"""
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
# Instead of Pose, we use Odometry
from nav_msgs.msg import Odometry

from math import pow, atan2, sqrt
import time


class TurtleBot(Node):

    def __init__(self):
        super().__init__('turtlebot_controller')
        # Publisher for turtle velocity commands.
        self.velocity_publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )
        # Subscriber for the turtle's current odometry.
        # Again, we use Odometry here instead of Pose
        self.pose_subscriber = self.create_subscription(
            Odometry,
            '/odom',
            self.update_pose,
            10
        )
        self.odom = None
        self.get_logger().info('TurtleBot controller initialized.')
    def update_pose(self, msg):
        """Callback function for receiving the turtle's pose."""
        self.odom = msg
        # Correctly find x and y from Odometry data
        self.odom.pose.pose.position.x = round(self.odom.pose.pose.position.x, 4)
        self.odom.pose.pose.position.y = round(self.odom.pose.pose.position.y, 4)

    def euclidean_distance(self, goal_pose):
        """Calculate the distance between the turtle and the goal."""

        return sqrt(
            pow(goal_pose.odom.pose.pose.orientation.x - self.odom.pose.pose.position.x, 2) +
            pow(goal_pose.y - self.odom.pose.pose.position.y, 2)
        )

    def linear_vel(self, goal_pose, constant=0.5):
        """Calculate the linear velocity."""

        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        """Calculate the angle toward the goal."""
        return atan2(
            goal_pose.odom.pose.pose.position.y - self.odom.pose.pose.position.y,
            goal_pose.odom.pose.pose.position.x - self.odom.pose.pose.position.x
        )

    def angular_vel(self, goal_pose, constant=0.5):
        """Calculate the angular velocity."""
        angle_difference = (
            self.steering_angle(goal_pose) - self.pose.pose.orientation.z
        )

        # Normalize the angle to the range [-pi, pi].
        angle_difference = atan2(
            __import__('math').sin(angle_difference),
            __import__('math').cos(angle_difference)
        )

        return constant * angle_difference

    def move2goal(self):
        """Move the turtle to the specified goal."""
        goal_pose = Odometry()

        # Get the goal coordinates from the user.
        goal_pose.odom.pose.pose.orientation.x = float(input('Set your x goal: '))
        goal_pose.odom.pose.pose.orientation.y = float(input('Set your y goal: '))

        distance_tolerance = float(
            input('Set your tolerance (e.g. 0.01): ')
        )

        if distance_tolerance <= 0:
            self.get_logger().error(
                'Distance tolerance must be greater than zero.'
            )
            return

        vel_msg = Twist()

        # Wait until the first pose message arrives.
        self.get_logger().info('Waiting for turtle pose...')

        while rclpy.ok() and self.pose is None:
            rclpy.spin_once(self, timeout_sec=0.1)

        if not rclpy.ok():
            return

        self.get_logger().info(
            f'Moving toward goal: x={goal_pose.odom.pose.pose.orientation.x}, y={goal_pose.y}'
        )

        try:
            while rclpy.ok():

                # Process incoming pose messages.
                rclpy.spin_once(self, timeout_sec=0.1)

                if self.pose is None:
                    continue

                # Stop when the turtle reaches the goal.
                if (
                    self.euclidean_distance(goal_pose)
                    < distance_tolerance
                ):
                    break

                # Calculate linear velocity.
                vel_msg.linear.x = self.linear_vel(goal_pose)
                vel_msg.linear.y = 0.0
                vel_msg.linear.z = 0.0

                # Calculate angular velocity.
                vel_msg.angular.x = 0.0
                vel_msg.angular.y = 0.0
                vel_msg.angular.z = self.angular_vel(goal_pose)

                # Publish the velocity command.
                self.velocity_publisher.publish(vel_msg)

        except KeyboardInterrupt:
            self.get_logger().info('Movement interrupted.')

        finally:
            # Stop the turtle.
            vel_msg.linear.x = 0.0
            vel_msg.linear.y = 0.0
            vel_msg.linear.z = 0.0

            vel_msg.angular.x = 0.0
            vel_msg.angular.y = 0.0
            vel_msg.angular.z = 0.0

            self.velocity_publisher.publish(vel_msg)

        if rclpy.ok():
            self.get_logger().info('Goal reached or movement stopped.')


def main(args=None):

    rclpy.init(args=args)

    turtlebot = TurtleBot()

    try:
        turtlebot.move2goal()

    except KeyboardInterrupt:
        pass

    finally:
        turtlebot.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
