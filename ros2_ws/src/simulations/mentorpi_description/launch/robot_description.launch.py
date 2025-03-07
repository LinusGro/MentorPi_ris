import os
from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import Node
from launch.conditions import IfCondition
from launch import LaunchDescription, LaunchService
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    compiled = 'False' # os.environ['need_compile']
    use_gui = LaunchConfiguration('use_gui', default='true')
    use_rviz = LaunchConfiguration('use_rviz', default='true')
    namespace = LaunchConfiguration('namespace', default='')
    use_namespace = LaunchConfiguration('use_namespace', default='false')
    frame_prefix = LaunchConfiguration('frame_prefix', default='')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    use_gui_arg = DeclareLaunchArgument('use_gui', default_value=use_gui)
    use_rviz_arg = DeclareLaunchArgument('use_rviz', default_value=use_rviz)
    frame_prefix_arg = DeclareLaunchArgument('frame_prefix', default_value=frame_prefix)
    use_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value=use_sim_time)
    namespace_arg = DeclareLaunchArgument('namespace', default_value=namespace)
    use_namespace_arg = DeclareLaunchArgument('use_namespace', default_value=use_namespace)

    if compiled == 'True':
        mentorpi_description_package_path = get_package_share_directory('mentorpi_description')
    else:
        mentorpi_description_package_path = os.path.join(os.environ['HOME'], 'workspace/ros2_ws/src/simulations/mentorpi_description')
    urdf_path = os.path.join(mentorpi_description_package_path, 'urdf/mentorpi.xacro')
    rviz_config_file = os.path.join(mentorpi_description_package_path, 'rviz/view.rviz')

    robot_description = Command(['xacro ', urdf_path])

    # 动态TF转换(dynamic TF conversion)
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'source_list': ['/controller_manager/joint_states'],
                     'rate': 20.0}]
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen',
        condition=IfCondition(use_gui),
        remappings=[('/joint_states', 'joint_controller')]
    )

    # 静态TF(static TF)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        name='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'frame_prefix': frame_prefix, 'use_sim_time': use_sim_time}],
        arguments=[urdf_path],
        remappings=[('/tf', 'tf'),
                  ('/tf_static', 'tf_static')]
    )

    rviz_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(mentorpi_description_package_path, 'launch', 'rviz.launch.py')),
            condition=IfCondition(use_rviz),
            launch_arguments={
                              'namespace': namespace,
                              'use_namespace': use_namespace,
                              'rviz_config': rviz_config_file}.items())

    return LaunchDescription([
        use_gui_arg,
        use_rviz_arg,
        frame_prefix_arg,
        use_sim_time_arg,
        namespace_arg,
        use_namespace_arg,
        joint_state_publisher_node,
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_launch,
    ])

if __name__ == '__main__':
    # 创建一个LaunchDescription对象(create a LaunchDescription object)
    ld = generate_launch_description()

    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()
