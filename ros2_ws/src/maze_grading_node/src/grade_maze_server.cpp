#include <memory>
#include <rclcpp/rclcpp.hpp>
#include "maze_interface/srv/grade_maze.hpp"
#include "ament_index_cpp/get_package_share_directory.hpp"
#include <iostream>
#include <fstream>
#include <stdint.h>

#define WALL_SCORE 3
#define METADATA_PENALTY -5

void gradeMaze(const std::shared_ptr<maze_interface::srv::GradeMaze::Request> request, 
    std::shared_ptr<maze_interface::srv::GradeMaze::Response> response) {
        std::string package_share_directory = ament_index_cpp::get_package_share_directory("maze_grading_node");
        std::string file_path = package_share_directory + "/mazes/" + std::to_string(request->maze_nr) +".maze";
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Grading request received with ID: %d.", request->maze_nr);
        std::ifstream maze_file(file_path);

        if(!maze_file.is_open()) {
            // If not found return default maze
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Could not find maze file with ID: %d.", request->maze_nr);
            response->score = 0;
            return;
        }

        // If valid maze nr.
        // Get metadata to grade
        // ToDo: Add logic to evaluate maze given by the students.


    }

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = rclcpp::Node::make_shared("maze_grading_server");
  rclcpp::Service<maze_interface::srv::GradeMaze>::SharedPtr service = 
        node->create_service<maze_interface::srv::GradeMaze>("grade_maze", &gradeMaze);
    
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Ready to send mazes.");
    
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}