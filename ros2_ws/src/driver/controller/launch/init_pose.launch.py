import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription, LaunchService
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, OpaqueFunction

def launch_setup(context, *args, **kwargs):
    compiled = 'False' # os.environ.get('need_compile', 'False')
    namespace = LaunchConfiguration('namespace', default='')
    use_namespace = LaunchConfiguration('use_namespace', default='false')

    namespace_arg = DeclareLaunchArgument('namespace', default_value=namespace)
    use_namespace_arg = DeclareLaunchArgument('use_namespace', default_value=use_namespace)

    if compiled == 'True':
        controller_package_path = get_package_share_directory('controller')
    else:
        controller_package_path = os.path.join(os.environ['HOME'], 'workspace/ros2_ws/src/driver/controller')

    init_pose_param_file = os.path.join(controller_package_path, 'config/init_pose.yaml')

    init_pose_node = Node(
        package='controller',
        executable='init_pose',
        name='init_pose',
        output='screen',
        parameters=[init_pose_param_file],
    )

    return [
        namespace_arg,
        use_namespace_arg,
        init_pose_node
    ]

def generate_launch_description():
    return LaunchDescription([
        OpaqueFunction(function=launch_setup)
    ])

if __name__ == '__main__':
    ld = generate_launch_description()

    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()
