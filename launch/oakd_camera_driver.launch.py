# OAK-D Pro W camera driver launch file.
#
# Created by Martin Kriz on 21.05.2026

from launch import LaunchDescription, LaunchContext, LaunchDescriptionEntity
from launch.actions import DeclareLaunchArgument, EmitEvent, OpaqueFunction
from launch.events import Shutdown
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

from ament_index_python.packages import get_package_share_directory
from nav2_common.launch import RewrittenYaml

import os
from typing import Optional, List


def launch_setup(context: LaunchContext) -> Optional[List[LaunchDescriptionEntity]]:

    robot_name = LaunchConfiguration('robot_name')
    robot_number = LaunchConfiguration('robot_number')
    name = LaunchConfiguration('name')
    config = LaunchConfiguration('config')

    indexed_robot_name = [robot_name.perform(context), '_', robot_number.perform(context)] if robot_number.perform(context) else [robot_name.perform(context)]
    indexed_robot_name = ''.join(indexed_robot_name)

    name_str = name.perform(context)

    config_dir = os.path.join(get_package_share_directory('oak_d_pro_driver'), 'config', robot_name.perform(context))
    os.chdir(config_dir)

    config_substitutions = {
        'i_tf_tf_prefix': name_str,
        'i_tf_base_frame': name_str,
    }

    configured_config = RewrittenYaml(
        source_file=config,
        root_key=indexed_robot_name + '/' + name_str,
        param_rewrites=config_substitutions,
        convert_types=True,
    )

    return [LaunchDescription([
        ComposableNodeContainer(
            name=name_str + '_container',
            namespace=indexed_robot_name,
            package='rclcpp_components',
            executable='component_container',
            composable_node_descriptions=[
                ComposableNode(
                    package='depthai_ros_driver_v3',
                    plugin='depthai_ros_driver::Driver',
                    name=name_str,
                    namespace=indexed_robot_name,
                    parameters=[configured_config],
                ),
            ],
            output='both',
            on_exit=[EmitEvent(event=Shutdown())],
        ),
    ])]


def generate_launch_description():

    this_pkg_dir = get_package_share_directory('oak_d_pro_driver')

    return LaunchDescription([
        DeclareLaunchArgument(
            name='robot_name',
            description='Robot name (ex: "robot").',
        ),
        DeclareLaunchArgument(
            name='robot_number',
            default_value='',
            description='Robot number appended to robot name if defined ("<name>_<number>", default is empty).',
        ),
        DeclareLaunchArgument(
            name='name',
            default_value='oak',
            description='Camera node name.',
        ),
        DeclareLaunchArgument(
            name='config',
            description='Path to platform config YAML (camera, IMU, TF settings).',
        ),
        OpaqueFunction(function=launch_setup),
    ])
