cmake_minimum_required(VERSION 3.5)
project(orchestrator_launch)

# Use the `ament_cmake` build system
find_package(ament_cmake REQUIRED)

# Install launch files
install(
  DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

# Package export
ament_package()
