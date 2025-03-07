import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node  # noqa: E402
from launch import LaunchDescription, LaunchService  # noqa: E402

def generate_launch_description():
    peripherals_package_path = os.path.join(os.environ['HOME'], 'workspace/ros2_ws/src/peripherals')
    camera_nodes = Node(
        package='usb_cam',
        executable='usb_cam_node_exe',
        output='screen',
        name='usb_cam',
        parameters=[os.path.join(peripherals_package_path, 'config', 'usb_cam_param.yaml')],
        remappings = [
            ('image_raw', '/ascamera/camera_publisher/rgb0/image'),
            ('image_raw/compressed', '/ascamera/camera_publisher/rgb0/image_compressed'),
            ('image_raw/compressedDepth', '/ascamera/camera_publisher/rgb0/compressedDepth'),
            ('image_raw/theora', '/ascamera/camera_publisher/rgb0/image_raw/theora'),
            ('camera_info', '/ascamera/camera_publisher/rgb0/camera_info'),
        ]
    )

    return LaunchDescription([camera_nodes])

if __name__ == '__main__':
    # 创建一个LaunchDescription对象(create a LaunchDescription object)
    ld = generate_launch_description()

    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()
