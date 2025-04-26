#include "rclcpp/rclcpp.hpp"
#include "maze_interface/msg/ros_maze.hpp"
#include "maze_interface/srv/get_ros_maze.hpp"
#include "ament_index_cpp/get_package_share_directory.hpp"
#include <iostream>
#include <fstream>
#include <stdint.h>

void sendMaze(const std::shared_ptr<maze_interface::srv::GetRosMaze::Request> request, 
    std::shared_ptr<maze_interface::srv::GetRosMaze::Response> response) {
        std::string package_share_directory = ament_index_cpp::get_package_share_directory("maze_publisher_node");
        std::string file_path = package_share_directory + "/mazes/" + std::to_string(request->maze_nr) +".maze";
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Request received with ID: %d.", request->maze_nr);
        std::ifstream maze_file(file_path);
        // std::ifstream maze_file(std::to_string(request->maze_nr) + ".maze");
        maze_interface::msg::RosMaze respMaze;
        // Check if file was found
        if(!maze_file.is_open()) {
            // If not found return default maze
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Could not find maze file with ID: %d.", request->maze_nr);
            respMaze.n = 0;
            respMaze.m = 0;
            respMaze.start_idx = 0;
            respMaze.end_idx = 0;
            respMaze.start_orientation = 0;
            respMaze.l.clear();
            return;
        }
        // If file was found
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Sending maze with ID: %d", request->maze_nr);
        std::string line;
        uint32_t counter = 0;
        while(std::getline(maze_file, line)) {
            switch(counter) {
                case 0:
                    respMaze.n = std::stoi(line);
                    break;
                case 1: 
                    respMaze.m = std::stoi(line);
                    break;
                case 2: 
                    respMaze.start_idx = std::stoi(line);
                    break;
                case 3: 
                    respMaze.end_idx = std::stoi(line);
                    break;
                case 4: 
                    respMaze.start_orientation = std::stoi(line);
                    break;
                default:
                    respMaze.l.push_back(std::stoi(line));
            }
            counter++;
        }
        // Write maze to response and close file
        maze_file.close();
        response->maze = respMaze;
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Maze successfully sent.");
    }

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);

    std::shared_ptr<rclcpp::Node> node = rclcpp::Node::make_shared("maze_publisher_server");
    rclcpp::Service<maze_interface::srv::GetRosMaze>::SharedPtr service = 
        node->create_service<maze_interface::srv::GetRosMaze>("get_ros_maze", &sendMaze);
    
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Ready to send mazes.");

    rclcpp::spin(node);
    rclcpp::shutdown();

}