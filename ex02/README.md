# Exercise 2: ROS2 Sensors

Instructions for running the code and answers to questions presented in the exercise instructions.

## 1. Quick introduction to Gazebo Simulation Environment

### 1.2 Get familiar with Ignition Gazebo Simulator

* Understanding the GUI:

  https://gazebosim.org/docs/fortress/gui

```bash
ign gazebo shapes.sdf
```

* Manipulating models: Interact with the models.

  https://gazebosim.org/docs/fortress/manipulating_models

```bash
ign gazebo shapes.sdf
```

* Model insertion from Fuel: (The online model database for Ignition Gazebo)

  https://gazebosim.org/docs/fortress/fuel_insert

```bash
ign gazebo world_demo.sdf
```

* Building robot – Understanding how to create a Gazebo world using SDF format and including a custom-built robot

  https://gazebosim.org/docs/fortress/building_robot

```bash
ign gazebo building_robot.sdf
```

* Moving the robot: Introduction to plugins, topics and messages

  https://gazebosim.org/docs/fortress/moving_robot

```bash
ign gazebo moving_robot.sdf
```

To move the robot, we can use the 'diff_drive' plugin we have added to our model. With this plugin we can send linear and angular velocity commands to control our differential drive robot:

```bash
ign topic -t "/cmd_vel" -m ignition.msgs.Twist -p "linear: {x: 0.5}, angular: {z: 0.05}"
```

We can also use the plugin 'KeyPublisher'. KeyPublisher is an ign-gui plugin that reads the keyboard’s keystrokes and sends them on a default topic /keyboard/keypress. We can control the robot by remapping this data to /cmd_vel topic using the 'TriggeredPublisher' plugin we have added to our model.

We can inspect the published data by running in a separate terminal:

```bash
ign topic -e -t /keyboard/keypress
```

## 2. Simulating sensors

### 2.1 Get familiar with sensors
	
**Question**:

What are the different attributes of the Lidar sensor and what difference do they make when set to different values?
                  
**Answer**:

	<pose> = position relative to which frame (mount point of the sensor).

	<topic> = name of the topic on which the lidar data will be published

	<update_rate> = frequency at which the lidar data is generated	

	Under <horizontal> and <vertical> tags we define the properties of the horizontal and vertical laser rays:  
		  		
		<samples> = is the number of simulated lidar rays to 
		            generate per complete laser sweep cycle
		  	
		<resolution> = this number is multiplied by samples to 
					   determine the number range data points

		<min_angle> and <max_angle> are the angle range of the generated rays

	Under the <range> tags we define range properties of each simulated ray:

		<min> and <max> define the minimum and maximum distance for each lidar ray

		<resolution> defines the linear resolution of each lidar ray.

	<always_on> = if true the sensor will always be updated according to the <update_rate>

	<visualize> = if true the sensor is visualized in the GUI
		
### 2.2 Segmentation camera example

**Demo**:

Start
```bash
ign gazebo segmentation_camera.sdf
```

and run the simulation. Once the camera has reached the ground, close Gazebo. The simulation data is saved in

	segmentation_data/

We can visualize this data using the python script:

```bash
python3 segmentation_visualizer.py --path segmentation_data/instance_camera
```
and

```bash
python3 segmentation_visualizer.py --path segmentation_data/semantic_camera
```
	
**Question 1**:

 Explain what information is being published over each of the ignition topics.
	
**Answer**:

By running the simulation
```bash
ign gazebo segmentation_camera.sdf
```
and listing the topics
```bash
ign topic -l
```
we can see the topics the RGB camera publishes to:
	        
	/world/shapes/model/realsense_d435/link/link/sensor/realsense_d435/camera_info
    /world/shapes/model/realsense_d435/link/link/sensor/realsense_d435/depth_image
    /world/shapes/model/realsense_d435/link/link/sensor/realsense_d435/image
    /world/shapes/model/realsense_d435/link/link/sensor/realsense_d435/points
                
To get the message types corresponding to these topics, we run the command
```bash
ign topic -t <topic_name> -i
```
We can examine the resulting message types with
```bash
ign msg -i <msg_type>
```

As a result, we can deduce the information being published for each of the topics.

We could also just echo the topics with
```bash
ign topic -e -t <topic_name>
```
                
**Question 2**:

What are the message types of them?
	
**Answer**:

See above.
	
**Question 3**:

Do you see the same list of topics in ros2 topics list? If the answer is no, then why?
                
**Answer**:

No, the ign topics are not visible with ros2 topic list. ROS2 and gazebo use different underlying communication architectures, middleware and data serialization formats. As middleware, ros2 uses DDS and gazebo uses gz-transport. This is the underlying reason why gazebo topics are not visible in ros2 topic list.

For example, the discovery protocols for DDS and gz-transport use different UDP ports for discovering messages etc. Thus, the messages need to be bridged from ROS2 to Gazebo and vice versa to allow communication between them.
                
                
## 3. ROS Integration with Gazebo

Demos found in:

https://github.com/gazebosim/ros_gz/tree/ros2/ros_gz_sim_demos

**Question 1**:

What are the different topics being published, what information do they publish? What are the message types?
	
**Answer**:

Topics, info, and message types can be discovered either from ros2 side
```bash
ros2 topic list -t
```
And then
```bash
ros2 interface show <msg_type>
```	       
for the desired message type.

Or from gazebo side
```bash
ign topic -l
ign topic -t <topic_name> -i
ign msg -i <msg_type>
```

**Question 2**:

The rostopics were not being published in the example in section 2.2. However, the rostopics are being published over the ROS master in this implementation in section 3. What is the reason for this difference between the two implementations?
	
**Answer**:

The reason is the installed integration package for ROS and Gazebo, which bridges the ROS2 and gazebo communication layers.


## 4. ros_ignition_bridge

1. Run your previous example with segmentation camera with Ignition:

```bash
ign gazebo segmentation_camera.sdf
```

2. On a 2nd terminal run the command below:

```bash
ros2 run ros_gz_bridge parameter_bridge /panoptic/camera_info@sensor_msgs/msg/CameraInfo@ignition.msgs.CameraInfo
```

3. On a 3rd terminal run the command to list rostopics:

```bash
ros2 topic list
```

Now you can see the translated rostopic
/panoptic/camera_info being published over ROS.

4. Try to bridge more messages from 3 more different message types and observe them being published over ROS:

```bash
ros2 run ros_gz_bridge parameter_bridge /panoptic/colored_map@sensor_msgs/msg/Image@ignition.msgs.Image
ros2 run ros_gz_bridge parameter_bridge /world/shapes/pose/info@tf2_msgs/msg/TFMessage@ignition.msgs.Pose_V
ros2 run ros_gz_bridge parameter_bridge /world/shapes/stats@ros_gz_interfaces/msg/WorldStatistics@ignition.msgs.WorldStatistics
```


## 5. Implement your own task

**Demo**:

TODO