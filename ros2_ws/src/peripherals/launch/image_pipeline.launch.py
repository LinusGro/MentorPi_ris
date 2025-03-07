import os
from launch import LaunchDescription
from launch_ros.actions import Node, ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    peripherals_package_path = os.path.join(os.environ['HOME'], 'workspace/ros2_ws/src/peripherals')

    # USB Camera Node
    camera_node = Node(
        package='usb_cam',
        executable='usb_cam_node_exe',
        output='screen',
        name='usb_cam',
        parameters=[os.path.join(peripherals_package_path, 'config', 'usb_cam_param.yaml')],
        remappings=[
            ('image_raw', '/ascamera/camera_publisher/rgb0/image'),
            ('image_raw/compressed', '/ascamera/camera_publisher/rgb0/image_compressed'),
            ('image_raw/compressedDepth', '/ascamera/camera_publisher/rgb0/compressedDepth'),
            ('image_raw/theora', '/ascamera/camera_publisher/rgb0/image_raw/theora'),
            ('camera_info', '/ascamera/camera_publisher/rgb0/camera_info'),
        ]
    )

    # Image Processing as a Composable Node
    image_proc_container = ComposableNodeContainer(
        name='image_proc_container',
        namespace='ascamera/camera_publisher/rgb0',
        package='rclcpp_components',
        executable='component_container',
        output='screen',
        composable_node_descriptions=[
            ComposableNode(
                package='image_proc',
                plugin='image_proc::RectifyNode',
                name='rectify_color_node',
                remappings=[
                    ('image', '/ascamera/camera_publisher/rgb0/image'),
                    ('camera_info', '/ascamera/camera_publisher/rgb0/camera_info'),
                    ('image_rect', '/ascamera/camera_publisher/rgb0/image_rect'),
                ],
            ),
        ],
    )

    return LaunchDescription([camera_node, image_proc_container])

