from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    compiled = 'False' # os.environ.get('need_compile', 'False')
    if compiled == 'True':
        calibration_package_path = get_package_share_directory('calibration')
    else:
        calibration_package_path = os.path.join(os.environ['HOME'], 'workspace/ros2_ws/src/calibration')

    calib_file_path = os.path.join(calibration_package_path, 'config/imu_calib.yaml')
    if not os.path.exists(calib_file_path):
        raise FileNotFoundError(f"Calibration file not found: {calib_file_path}")

    imu_calib_node = Node(
        package='imu_calib',
        executable='apply_calib',
        name='imu_calib',
        output='screen',
        parameters=[{"calib_file": calib_file_path}],
        remappings=[
            ('raw', '/ros_robot_controller/imu_raw'),
            ('corrected', 'imu_corrected')
        ]
    )

    imu_filter_node = Node(
        package='imu_complementary_filter',
        executable='complementary_filter_node',
        name='imu_filter',
        output='screen',
        parameters=[
            {
                'use_mag': False,
                'do_bias_estimation': True,
                'do_adaptive_gain': True,
                'publish_debug_topics': True
            }
        ],
        remappings=[
            ('/tf', 'tf'),
            ('/imu/data_raw', 'imu_corrected'),
            ('imu/data', 'imu')
        ]
    )

    return LaunchDescription([
        TimerAction(
            period=5.0,
            actions=[imu_calib_node, imu_filter_node]
        )
    ])

if __name__ == '__main__':
    from launch import LaunchService
    ld = generate_launch_description()

    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()
