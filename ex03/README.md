# Exercise 3: TurtleBot
## Task 1: TurtleBot simulation
The objective of this task is to get familiar with the turtlebot simulation and how to utilize it.<br>
Complete the following tasks:

1. Open 2 terminals and execute the following command:
    ```bash
    $ ros2 run turtlesim turtlesim_node
    $ ros2 run turtlesim turtle_teleop_key
    ```
2. Try out the tele-operation and investigate the topics and nodes with suitable ROS commands

    Using rqt to investigate the relevant topics, we can find:
    ```
    /turtle1/pose
    /turtle1/color_sensor
    /turtle1/rotate_absolute/_action/feedback
    /turtle1/cmd_vel
    /turtle1/rotate_absolute/_action/status
    ```
    The relevant nodes found from rqt node graph are:
    ```
    /turtlesim
    /teleop_turtle
    ```
3. Find out what topic and message are used for sending velocity commands to the TurtleBot

    Using rqt node graph, it can be seen that the node `/teleop_turtle` sends velocity commands to the node `/turtlesim` through the topic `/turtle1/cmd_vel`. The message type is `geometry_msgs/msg/Twist` which holds linear and angular fields with message types `geometry_msgs/msg/Vector3` that hold velocities for x, y and z directions.

4. Use the ros2 topic command to move the robot in a circle and in a square path

    A circular path can be achieved with some velocity in x or y direction and angular velocity with respect to the z-axis. The command for this is:
    ```bash
    $ ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist '{linear: {x: 1.0}, angular: {z: 1.0}}'
    ```
    One way to achieve a square path accurately is by specifying how many times the velocity command is published. If we want a square with a side length of 3 m, do the following commands sequentially 4 times (the first turn is not necessary):
    ```bash
    $ ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{angular: {z: 1.57}}"
    $ ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 3.0}}"
    ```
    The `--once` option specifies that the message should be published only once.
5. Find a way to concatenate multiple commands to achieve consecutive motions

    Multiple commands can be concatenated if we use the && operator in between commands in the command line. The && operator waits for the previous command to succeed before proceeding. The full command would look like this:
    ```bash
    $ ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 3.0}}" && ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{angular: {z: 1.57}}" && ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 3.0}}" && ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{angular: {z: 1.57}}" && ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 3.0}}" && ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{angular: {z: 1.57}}" && ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 3.0}}"
    ```