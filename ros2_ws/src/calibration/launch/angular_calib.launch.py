from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # 底盘控制(chassis control)
    controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory('controller'),
            '/launch/controller.launch.py'
        ])
    )

    # 速度校准(angular velocity calibration)
    calibrate_angular_node = Node(
        package='calibration',
        executable='calibrate_angular',
        output='screen'
    )

    # rqt
    calibrate_rqt_reconfigure_node = Node(
        package='rqt_reconfigure',
        executable='rqt_reconfigure',
        name='calibrate_rqt_reconfigure'
    )

    return LaunchDescription([
        controller_launch,
        calibrate_angular_node,
        calibrate_rqt_reconfigure_node
    ])

if __name__ == '__main__':
    generate_launch_description()