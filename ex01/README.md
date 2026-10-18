# Ex01 Instructions

This file contains brief instructions the client library tutorials part of Ex01: ROS2 Tutorials.

### Writing a simple publisher and subscriber (C++)

The package is located at

    /src/cpp_pubsub

To spin the nodes run

```bash
ros2 run cpp_pubsub talker
ros2 run cpp_pubsub listener
```

### Writing a simple publisher and subscriber (Python)

The package is located at

    /src/py_pubsub

Spin the nodes

```bash
ros2 run py_pubsub talker
ros2 run py_pubsub listener
```

### Writing a simple service and client (C++)

The package is located at

    /src/cpp_srvcli

Spin the nodes

```bash
ros2 run cpp_srvcli server
ros2 run cpp_srvcli client X Y
```
Parameters X and Y are integers.

### Writing a simple service and client (Python)

The package is located at

    /src/py_srvcli

Spin the nodes

```bash
ros2 run py_srvcli server
ros2 run py_srvcli client X Y
```