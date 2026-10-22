# Exercise 6: Robot Manipulator

Instructions for running the code and answers to questions presented in the exercise instructions.

This exercise will help students to get familiar with motion and task planning for a robot manipulator. Simulation, task and motion generation will be done with RViz and MoveIt, for the Frank Emika Panda robot manipulator (https://franka.de).

## 1. Preparations

Installation:
https://moveit.picknik.ai/humble/doc/tutorials/getting_started/getting_started.html

MoveIt Quickstart tutorial in RViz:
https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html

Try out all the covered functionalities, and explain the following:
- What functionalities do you need to plan and execute robot end-effector motion?
- How is motion planning via RViz limited, compared to utilizing Python/C++ (see task 2)?
- What is the robot’s Nullspace?

**Demo:**

```bash
ros2 launch moveit2_tutorials demo.launch.py rviz_config:=panda_moveit_config_demo_empty.rviz
```

**Answers to Questions:**

- To plan and execute end effector motion, you need to add Motionlanning display/plugin to RViz. From the plugin, you visualize the goal state and move the goal state to a desired position. You can then plan, execute and visualize the motion from the MotionPlanning panel. Under the 'Planning' tab you can set e.g. 'Velocity Scaling' wich determines the velocity the motion is executed with, you can enable 'Use Cartesian Path' for linear end effector motion, etc.

- In RViz, motion planning is primarily limited to interactive, manual operations, whereas Python/C++ allow more functionality. With Python/C++, it is possible to generate multiple target poses, execute complex sequences of movements, integrate sensor data, and implement conditional logic. Although both approaches can use the same underlying MoveIt planning algorithms, Python and C++ provide greater control over planning parameters and allow motion planning to be integrated into more complex robotic applications.

- Nullspace refers to robot's ability to change the configuration of its joints while keeping the end effector at the same position and orientation. That is, there exist multiple solutions for the inverse kinematics of the robot to reach a specific end effector pose.

    Mathematically, the concept comes from the robot's Jacobian matrix $J(\mathbf{q})$, which relates joint velocities $\dot{\mathbf{q}}$ to end end effector velocity $\dot{\mathbf{x}}$:

    $$
    \dot{\mathbf{x}} = J(\bm{q}) \dot{\bm{q}}
    $$

    If we want the end effector to remain stationary:

    $$
    J(\bm{q}) \dot{\bm{q}} = 0
    $$

    Any joint velocity vector satisfying this equation belongs to the nullspace of the Jacobian.

    In RViz, these different joint configurations can be explored and visualized with the Nullspace exploration slider in 'Joints' tab of 'MotionPlanning' panel.


## 2. Move group C++ interface

The objective of this task is to plan robot motion by the C++ interface of MoveIt2 following the tutorial:

https://moveit.picknik.ai/humble/doc/tutorials/your_first_project/your_first_project.html

Explain the following with knowledge from Task 1 and Task 2 :
- How is planning motions different for robot joint space and Cartesian (or work) space?
- Name few different constraints that apply in joint space.
- Name few different constraints that apply in Cartesian (or work) space.

**Demo:**

ROS2 package creation with moveit:

```bash
ros2 pkg create --build-type ament_cmake --dependencies moveit_ros_planning_interface rclcpp --node-name hello_moveit hello_moveit
```

Building the package after modifying the node:

```bash
colcon build --mixin debug --packages-select hello_moveit
```

Running the node:

We will use the same demo launch file from the previous tutorial to start RViz and the MoveGroup node

```bash
ros2 launch moveit2_tutorials demo.launch.py
```

In RViz, we will uncheck the box 'Query Goal State' under 'Planning Request'. Then we will run our node

```bash
ros2 run hello_moveit hello_moveit
```

Through the C++ MoveGroupInterface of moveit, this node connects to the robot's panda_arm planning group, defines a target pose for the end effector in 3D space, plans a path to that pose, and executes the plan if planning succeeds.

**Answers to Questions:**

- Joint-space planning focuses on joint movements, whereas Cartesian-space planning focuses on the end effector's movement along a desired path. Joint-space planning plans the motion by specifying the positions of the robot's individual joints. The planner finds a path between the initial and target joint configurations. Cartesian-space planning plans the motion of the end effector in terms of its position and orientation in 3D space.
- Joint position, velocity and acceleration limits, joint torque limits.
- End effector position constraints, path constraints, obstacle avoidance.


## 3. Visualizing with RVIZ

The following tutorial introduces utilizing moveit_visual_tools for visualizing the moveit applications in
RVIZ. Complete the tutorial and demonstrate the rviz visualizations.

https://moveit.picknik.ai/humble/doc/tutorials/visualizing_in_rviz/visualizing_in_rviz.html




## 4. Planning around objects



## 5. Pick and place