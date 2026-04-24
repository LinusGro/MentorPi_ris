cmake_minimum_required(VERSION 3.8)
project(maze_grading_node)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(maze_interface REQUIRED)
find_package(ament_index_cpp REQUIRED)

add_executable(grade_maze_server src/grade_maze_server.cpp)
ament_target_dependencies(grade_maze_server
  rclcpp
  maze_interface
  ament_index_cpp
)

install(TARGETS
  grade_maze_server
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY mazes/
  DESTINATION share/${PROJECT_NAME}/mazes
)

ament_package()
