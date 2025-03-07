import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    apriltag_package_path = os.path.join(os.environ['HOME'], 'workspace/ros2_ws/src/peripherals/config')

    return LaunchDescription([
        Node(
            package='apriltag_ros',
            executable='apriltag_node',
            name='apriltag_detector',
            output='screen',
            parameters=[
                os.path.join(apriltag_package_path, 'apriltag_config.yaml'),  # Camera settings
            ],
            remappings=[
                ('/image_rect', '/ascamera/camera_publisher/rgb0/image_rect'),
                ('/camera_info', '/ascamera/camera_publisher/rgb0/camera_info'),
                ('/detections', '/apriltag_detections'),
            ]
        )
    ])

