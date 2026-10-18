cmake_minimum_required(VERSION 3.8)
project(robot_gripper)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(ros_gz_interfaces REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(contact_listener src/contact_subscriber.cpp)
ament_target_dependencies(contact_listener rclcpp ros_gz_interfaces std_msgs)

install(TARGETS
  contact_listener
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
