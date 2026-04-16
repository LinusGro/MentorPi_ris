#include <memory>
#include <rclcpp/rclcpp.hpp>
#include "maze_interface/srv/grade_maze.hpp"
#include "maze_interface/srv/grade_cubes.hpp"
#include "ament_index_cpp/get_package_share_directory.hpp"
#include <iostream>
#include <fstream>
#include <stdint.h>
#include <algorithm>

#define WALL_SCORE 5
#define WALL_PENALTY -5

void checkWall(uint8_t file_cell, uint8_t req_cell, uint8_t mask, int32_t& score) {
    // Check if wall should be set
    if(file_cell&mask) {
        // Score if wall is set, penalty if not
        if(req_cell&mask) {
            score += WALL_SCORE;
        } else {
            score += WALL_PENALTY;
        }
    }
    // If wall should not be set
    else 
    {
        // Wall was wrongly set
        if(req_cell&mask) {
            score += WALL_PENALTY;
        }
    }
    return;
}

void gradeMaze(const std::shared_ptr<maze_interface::srv::GradeMaze::Request> request, 
    std::shared_ptr<maze_interface::srv::GradeMaze::Response> response) {
        std::string package_share_directory = ament_index_cpp::get_package_share_directory("maze_grading_node");
        std::string file_path = package_share_directory + "/mazes/" + std::to_string(request->maze_nr) +".maze";
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Grading request received with ID: %d.", request->maze_nr);
        std::ifstream maze_file(file_path);

        if(!maze_file.is_open()) {
            // If not found return 0 score
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Could not find maze file with ID: %d.", request->maze_nr);
            response->score = -1;
            return;
        }

        // Maze grading logic
        std::string line;
        uint32_t counter = 0;
        int32_t score = 0;
        auto req_maze = request->maze;
        uint8_t req_n = req_maze.n;
        uint8_t req_m = req_maze.m; 
        auto req_mazedata = req_maze.l;
        uint8_t file_n, file_m, overlap_n, overlap_m;
        std::vector<uint8_t> file_maze;
        while(std::getline(maze_file, line)) {
            switch(counter) {
                case 0:
                    file_n = std::stoi(line);
                    overlap_n = std::min(file_n, req_n);
                    break;
                case 1: 
                    file_m = std::stoi(line);
                    overlap_m = std::min(file_m, req_m);
                    file_maze.reserve(file_n*file_m);
                    break;
                case 2:
                case 3:
                case 4:
                    // Skip start/end idx and orientation
                    break;
                default:
                    /// Save maze
                    file_maze.push_back(std::stoi(line));
                    
                    break;
            }
            counter++;
        }

        // Grade saved mazes by only counting in +x and +y direction with exception of first row/column
        // i iterates over rows and j over columns
        for(uint8_t i=0; i<overlap_n; i++) {
            for(uint8_t j=0; j<overlap_m; j++) {
                uint8_t req_cell = req_mazedata[i + req_n*j];
                uint8_t file_cell = file_maze[i + file_n*j];
                
                /*
                (0000) - no walls, but the cell is part of the maze
                (0001) - wall in postive x-direction
                (0010) - wall in negative x-direction
                (0100) - wall in positive y-direction
                (1000) - wall in negative y-direction
                (1111) - cell is not part of the maze
                */
                // Handling first row (-x wall counts)
                if(i==0) {
                    checkWall(file_cell, req_cell, 0b0010, score);
                }
                // Handling first column (-y walls count)
                if(j==0) {
                    checkWall(file_cell, req_cell, 0b1000, score);
                }

                // Handling +x walls
                checkWall(file_cell, req_cell, 0b0001, score);
                // Handling +y walls
                checkWall(file_cell, req_cell, 0b0100, score);
            }
        }
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Achieved %d points.", score);
        response->score = score;
        return;
    }


void gradeCubes(const std::shared_ptr<maze_interface::srv::GradeCubes::Request> request, 
    std::shared_ptr<maze_interface::srv::GradeCubes::Response> response) {
        std::string package_share_directory = ament_index_cpp::get_package_share_directory("maze_grading_node");
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "%d cube data tuples received.", request->n);

        response->score = 0;

        for(uint8_t i=0; i<request->n; i++) {
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Cube %d at x: %d  y: %d with color %d", i+1, request->x[i], request->y[i], request->color[i]);
        }
        return;
    }



int main(int argc, char ** argv)
{
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("maze_grading_server");
    rclcpp::Service<maze_interface::srv::GradeMaze>::SharedPtr service = 
            node->create_service<maze_interface::srv::GradeMaze>("grade_maze", &gradeMaze);
        
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Ready to send mazes.");

    rclcpp::Service<maze_interface::srv::GradeCubes>::SharedPtr service2 = 
            node->create_service<maze_interface::srv::GradeCubes>("grade_cubes", &gradeCubes);
        
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Ready to grade cubes.");
    
        
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}