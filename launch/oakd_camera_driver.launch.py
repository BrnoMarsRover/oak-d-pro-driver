# OAK-D Pro W camera driver launch file.
#
# Created by Martin Kriz on 21.05.2026

from launch import LaunchDescription, LaunchContext, LaunchDescriptionEntity
from launch.actions import DeclareLaunchArgument, EmitEvent, OpaqueFunction
from launch.events import Shutdown
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode, ParameterFile

from ament_index_python.packages import get_package_share_directory

import os
from typing import Optional, List


def _to_bool(value: str) -> bool:
    return value.lower() == 'true'


def launch_setup(context: LaunchContext) -> Optional[List[LaunchDescriptionEntity]]:

    this_pkg_dir = get_package_share_directory('oak_d_pro_driver')

    robot_name = LaunchConfiguration('robot_name')
    robot_number = LaunchConfiguration('robot_number')
    name = LaunchConfiguration('name')
    parent_frame = LaunchConfiguration('parent_frame')
    cam_pos_x = LaunchConfiguration('cam_pos_x')
    cam_pos_y = LaunchConfiguration('cam_pos_y')
    cam_pos_z = LaunchConfiguration('cam_pos_z')
    cam_roll = LaunchConfiguration('cam_roll')
    cam_pitch = LaunchConfiguration('cam_pitch')
    cam_yaw = LaunchConfiguration('cam_yaw')
    params_file = LaunchConfiguration('params_file')
    camera_fps = LaunchConfiguration('camera_fps')
    imu_update_rate = LaunchConfiguration('imu_update_rate')
    enable_rgb = LaunchConfiguration('enable_rgb')
    enable_depth = LaunchConfiguration('enable_depth')
    enable_infra1 = LaunchConfiguration('enable_infra1')
    enable_infra2 = LaunchConfiguration('enable_infra2')

    indexed_robot_name = [robot_name.perform(context), '_', robot_number.perform(context)] if robot_number.perform(context) else [robot_name.perform(context)]
    indexed_robot_name = ''.join(indexed_robot_name)

    name_str = name.perform(context)
    camera_fps_float = float(camera_fps.perform(context))
    imu_update_rate_int = int(imu_update_rate.perform(context))

    driver_params = {
        'driver': {
            'i_enable_ir': True,
            'i_publish_tf_from_calibration': True,
            'i_tf_tf_prefix': name_str,
            'i_tf_camera_model': '',
            'i_tf_base_frame': name_str,
            'i_tf_parent_frame': parent_frame.perform(context),
            'i_tf_cam_pos_x': cam_pos_x.perform(context),
            'i_tf_cam_pos_y': cam_pos_y.perform(context),
            'i_tf_cam_pos_z': cam_pos_z.perform(context),
            'i_tf_cam_roll': cam_roll.perform(context),
            'i_tf_cam_pitch': cam_pitch.perform(context),
            'i_tf_cam_yaw': cam_yaw.perform(context),
            'i_tf_imu_from_descr': 'false',
        },
        'pipeline_gen': {
            'i_pipeline_type': 'Stereo',
            'i_nn_type': 'none',
        },
        'rgb': {
            'i_fps': camera_fps_float,
            'i_publish_topic': _to_bool(enable_rgb.perform(context)),
        },
        'stereo': {
            'i_fps': camera_fps_float,
            'i_publish_topic': _to_bool(enable_depth.perform(context)),
            'i_left_rect_publish_topic': _to_bool(enable_infra1.perform(context)),
            'i_right_rect_publish_topic': _to_bool(enable_infra2.perform(context)),
        },
        'left': {
            'i_fps': camera_fps_float,
        },
        'right': {
            'i_fps': camera_fps_float,
        },
        'imu': {
            'i_acc_freq': imu_update_rate_int,
            'i_gyro_freq': imu_update_rate_int,
            'i_batch_report_threshold': 1,
            'i_max_batch_reports': 10,
            'i_enable_rotation': False,
            'i_enable_mag': False,
            'i_sync_method': 'LINEAR_INTERPOLATE_ACCEL',
        },
    }

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
                    parameters=[
                        ParameterFile(params_file, allow_substs=True),
                        driver_params,
                    ],
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
            name='parent_frame',
            default_value='oak_parent_frame',
            description='TF parent frame the camera is attached to.',
        ),
        DeclareLaunchArgument(
            name='cam_pos_x',
            default_value='0.0',
            description='Camera X position relative to parent frame [m].',
        ),
        DeclareLaunchArgument(
            name='cam_pos_y',
            default_value='0.0',
            description='Camera Y position relative to parent frame [m].',
        ),
        DeclareLaunchArgument(
            name='cam_pos_z',
            default_value='0.0',
            description='Camera Z position relative to parent frame [m].',
        ),
        DeclareLaunchArgument(
            name='cam_roll',
            default_value='0.0',
            description='Camera roll relative to parent frame [rad].',
        ),
        DeclareLaunchArgument(
            name='cam_pitch',
            default_value='0.0',
            description='Camera pitch relative to parent frame [rad].',
        ),
        DeclareLaunchArgument(
            name='cam_yaw',
            default_value='0.0',
            description='Camera yaw relative to parent frame [rad].',
        ),
        DeclareLaunchArgument(
            name='params_file',
            default_value=os.path.join(this_pkg_dir, 'config', 'oak_d_pro_w.yaml'),
            description='Path to the driver parameter YAML file.',
        ),
        DeclareLaunchArgument(
            name='camera_fps',
            default_value='60',
            description='Camera (color + stereo) output FPS.',
        ),
        DeclareLaunchArgument(
            name='imu_update_rate',
            default_value='400',
            description='IMU update rate [Hz].',
        ),
        DeclareLaunchArgument(
            name='enable_rgb',
            default_value='false',
            description='Enable RGB camera stream.',
        ),
        DeclareLaunchArgument(
            name='enable_depth',
            default_value='false',
            description='Enable stereo depth stream.',
        ),
        DeclareLaunchArgument(
            name='enable_infra1',
            default_value='true',
            description='Enable left rectified (infra1) stream.',
        ),
        DeclareLaunchArgument(
            name='enable_infra2',
            default_value='true',
            description='Enable right rectified (infra2) stream.',
        ),
        OpaqueFunction(function=launch_setup),
    ])
