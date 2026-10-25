cmake_minimum_required(VERSION 3.8)
project(hello_moveit)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(moveit_visual_tools REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# create executables
add_executable(hello_moveit src/hello_moveit.cpp)
target_include_directories(hello_moveit PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_features(hello_moveit PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17
ament_target_dependencies(
  hello_moveit
  "rclcpp"
  "moveit_ros_planning_interface"
)

add_executable(visualize_moveit src/visualize_moveit.cpp)
target_include_directories(visualize_moveit PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_features(visualize_moveit PUBLIC c_std_99 cxx_std_17)
ament_target_dependencies(
  visualize_moveit
  "rclcpp"
  "moveit_ros_planning_interface"
  "moveit_visual_tools"
)

add_executable(object_avoidance src/object_avoidance.cpp)
target_include_directories(object_avoidance PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_features(object_avoidance PUBLIC c_std_99 cxx_std_17)
ament_target_dependencies(
  object_avoidance
  "rclcpp"
  "moveit_ros_planning_interface"
  "moveit_visual_tools"
)

install(TARGETS
  hello_moveit
  visualize_moveit
  object_avoidance
  DESTINATION lib/${PROJECT_NAME})

ament_package()
