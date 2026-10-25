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

**Solution and Demo:**

```bash
ros2 launch moveit2_tutorials demo.launch.py rviz_config:=panda_moveit_config_demo_empty.rviz
```

**Answers to Questions:**

- To plan and execute end effector motion, you need to add Motionlanning display/plugin to RViz. From the plugin, you visualize the goal state and move the goal state to a desired position. You can then plan, execute and visualize the motion from the MotionPlanning panel. Under the 'Planning' tab you can set e.g. 'Velocity Scaling' wich determines the velocity the motion is executed with, you can enable 'Use Cartesian Path' for linear end effector motion, etc.

- In RViz, motion planning is primarily limited to interactive, manual operations, whereas Python/C++ allow more functionality. With Python/C++, it is possible to generate multiple target poses, execute complex sequences of movements, integrate sensor data, and implement conditional logic. Although both approaches can use the same underlying MoveIt planning algorithms, Python and C++ provide greater control over planning parameters and allow motion planning to be integrated into more complex robotic applications.

- Nullspace refers to robot's ability to change the configuration of its joints while keeping the end effector at the same position and orientation. That is, there exist multiple solutions for the inverse kinematics of the robot to reach a specific end effector pose.

    Mathematically, the concept comes from the robot's Jacobian matrix $J(\mathbf{q})$, which relates joint velocities $\dot{\mathbf{q}}$ to end end effector velocity $\dot{\mathbf{x}}$:

    
    $$\dot{\mathbf{x}} = J(\bm{q}) \dot{\bm{q}}$$

    If we want the end effector to remain stationary:

    $$J(\bm{q}) \dot{\bm{q}} = 0$$

    Any joint velocity vector satisfying this equation belongs to the nullspace of the Jacobian.

    In RViz, these different joint configurations can be explored and visualized with the Nullspace exploration slider in 'Joints' tab of 'MotionPlanning' panel.


## 2. Move group C++ interface

The objective of this task is to plan robot motion by the C++ interface of MoveIt2 following the tutorial:

https://moveit.picknik.ai/humble/doc/tutorials/your_first_project/your_first_project.html

Explain the following with knowledge from Task 1 and Task 2 :
- How is planning motions different for robot joint space and Cartesian (or work) space?
- Name few different constraints that apply in joint space.
- Name few different constraints that apply in Cartesian (or work) space.

**Solution and Demo:**

ROS2 package creation with moveit:

```bash
ros2 pkg create --build-type ament_cmake --dependencies rclcpp moveit_ros_planning_interface --node-name hello_moveit hello_moveit
```

Building the package after modifying the node:

```bash
colcon build --mixin debug --packages-select hello_moveit
```

Running the node:

We will use the same demo launch file and saved RViz configuration from the previous tutorial to start RViz and the MoveGroup node

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

The following tutorial introduces utilizing moveit_visual_tools for visualizing the moveit applications in RVIZ.
Complete the tutorial and demonstrate the rviz visualizations.

https://moveit.picknik.ai/humble/doc/tutorials/visualizing_in_rviz/visualizing_in_rviz.html


**Solution and Demo:**

We will create a new node 'visualize_moveit.cpp' in the package 'hello_moveit' we created in the previous task.

After adding dependencies in CMakeLists.txt and package.xml, and building the node according to the instructions in the demo, we can test the added visualizations. We use the same demo launch file from previous tasks.

In RViz we uncheck “MotionPlanning” in the “Displays” tab to hide it as we aren’t going to be using the “MotionPlanning” plugin here.

To add the buttons to interact with the prompts we added to our program open the dialog with the “Panels/Add New Panel” menu. Then select RvizVisualToolsGui. 

Finally, we need to add a Marker Array to render the visualizations we’ve added uising the “Add” Button in the “Displays” panel. Then under 'MarkerArray' we change the topic to '/rviz_visual_tools'. This configuration has been saved and can be used with:

```bash
ros2 launch moveit2_tutorials demo.launch.py rviz_config:=visualize_moveit.rviz
```

Then we run our node:

```bash
ros2 run hello_moveit visualize_moveit
```

Then from RViz we select 'Next' from the RVizVisualToolGui we added to advance our program.


## 4. Planning around objects

This tutorial introduces utilizing planning_scene_interface in moveit for motion planning. The program introduces a collision object to the planning motion around them.
https://moveit.picknik.ai/humble/doc/tutorials/planning_around_objects/planning_around_objects.html

Try out the following examples given for further reading and explain the following concepts:
https://moveit.picknik.ai/humble/doc/tutorials/planning_around_objects/planning_around_objects.html#further-reading

How does the planning scene monitor work with associated Moveit2 classes (RobotState, CurrentStateMonitor, PlanningScene, PlanningSceneMonitor, and PlanningSceneInterface)?

**Solution and Demo:**

We will create a new node 'object_avoidance' for this taks:

After adding dependencies and building the node according to the instructions in the demo, we can test the obstacle avoiding path planning. We use the same demo launch file from previous tasks and the RViz configuration from taks 3:

```bash
ros2 launch moveit2_tutorials demo.launch.py rviz_config:=visualize_moveit.rviz
```

Then we spin our node:

```bash
ros2 run hello_moveit object_avoidance
```

Then from RViz we select 'Next' from the RVizVisualToolGui we added to advance our program.

**Answers to Questions:**

In MoveIt 2, the PlanningSceneMonitor is the central component that keeps the robot's planning environment up to date. It connects the robot's current joint states, the robot's model, collision objects, sensor data, and the planning scene used by motion planners.

To understand how it works, it helps to distinguish five related classes:

1. RobotState — represents the configuration of the robot at a particular moment.
2. CurrentStateMonitor — receives live robot-state information and maintains an updated robot state.
3. PlanningScene — represents the robot and its environment for collision checking and planning.
4. PlanningSceneMonitor — monitors incoming data and keeps the planning scene synchronized with it.
5. PlanningSceneInterface — provides an interface for external applications to add, remove, or modify objects in the planning scene.

TODO


## 5. Pick and place

This tutorial creates a moveit package that demonstartes a pick and place task using Moveit Task constructor. Complete the tutorial and demonstrate the rviz visualizations.
https://moveit.picknik.ai/humble/doc/tutorials/pick_and_place_with_moveit_task_constructor/pick_and_place_with_moveit_task_constructor.html

**Solution and Demo:**

We create a new package:

```bash
ros2 pkg create --build-type ament_cmake --node-name mtc_tutorial mtc_tutorial
```

After adding dependencies and building the node and launch files according to the instructions outlined in the tutorial, we can build our package:

```bash
colcon build --mixin release --packages-select mtc_tutorial
```

and run the demo:

```bash
ros2 launch mtc_tutorial mtc_demo.launch.py
```

The demanded RViz configuration has been saved. We can then launch the pick and place sequence with

```bash
ros2 launch mtc_tutorial pick_place_demo.launch.py
```