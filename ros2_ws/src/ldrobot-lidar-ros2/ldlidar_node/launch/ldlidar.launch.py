import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, EmitEvent, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode
from launch_ros.events.lifecycle import ChangeState
from lifecycle_msgs.msg import Transition


def generate_launch_description():

    node_name = LaunchConfiguration('node_name')

    # Lidar node configuration file
    lidar_config_path = os.path.join(
        get_package_share_directory('ldlidar_node'),
        'params',
        'ldlidar.yaml'
    )

    # Launch arguments
    declare_node_name_cmd = DeclareLaunchArgument(
        'node_name',
        default_value='ldlidar_node',
        description='Name of the node'
    )

    # LDLidar lifecycle node
    ldlidar_node = LifecycleNode(
        package='ldlidar_node',
        executable='ldlidar_node',
        name=node_name,
        namespace='',
        output='screen',
        parameters=[
            lidar_config_path  # Parameters
        ]
    )

    # Event to transition the node to the 'configured' state
    configure_event = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=lambda node: 'ldlidar_node' in node.name,
            transition_id=Transition.TRANSITION_CONFIGURE
        )
    )

    # Event to transition the node to the 'active' state
    activate_event = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=lambda node: 'ldlidar_node' in node.name,
            transition_id=Transition.TRANSITION_ACTIVATE
        )
    )

    # Define LaunchDescription variable
    ld = LaunchDescription()

    # Launch arguments
    ld.add_action(declare_node_name_cmd)

    # Add LDLidar Lifecycle node
    ld.add_action(ldlidar_node)

    # Automatically configure the node
    ld.add_action(configure_event)

    # Automatically activate the node
    ld.add_action(activate_event)

    # Add logging
    ld.add_action(LogInfo(msg="Automatically configuring and activating the ldlidar_node."))

    return ld
