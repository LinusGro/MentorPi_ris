cmake_minimum_required(VERSION 3.8)
project(imu_calib)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
# find dependencies
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(eigen3_cmake_module REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(yaml_cpp_vendor REQUIRED)

include_directories(include src)
add_library(accel_calib
  src//accel_calib.cpp
)
ament_target_dependencies(accel_calib
  rclcpp
  sensor_msgs
  Eigen3
  yaml_cpp_vendor
)

# do_calib node
add_executable(do_calib src/do_calib_node.cpp src/do_calib.cpp)
ament_target_dependencies(do_calib rclcpp sensor_msgs Eigen3 yaml_cpp_vendor)
target_link_libraries(do_calib accel_calib)
target_link_libraries(do_calib yaml-cpp)

# apply_calib node
add_executable(apply_calib src/apply_calib_node.cpp src/apply_calib.cpp)
ament_target_dependencies(apply_calib rclcpp sensor_msgs Eigen3 yaml_cpp_vendor)
target_link_libraries(apply_calib accel_calib)
target_link_libraries(apply_calib yaml-cpp)
install(TARGETS
  do_calib
  apply_calib
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY include/
  DESTINATION include/
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_export_dependencies(rclcpp)
ament_export_dependencies(Eigen3)
ament_export_dependencies(sensor_msgs)
ament_export_dependencies(yaml_cpp_vendor)
ament_export_include_directories(include)
ament_package()
