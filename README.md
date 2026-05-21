# oak-d-pro-driver

ROS2 launch package for the OAK-D Pro W camera using the DepthAI ROS driver.

## Dependencies

- ROS2 Humble or Jazzy
- `depthai-ros-v3`

```bash
sudo apt install ros2-testing-apt-source
sudo apt update
sudo apt install ros-$ROS_DISTRO-depthai-ros-v3
```

## Usage

Build the package:

```bash
colcon build --packages-select oak_d_pro_driver
source install/setup.bash
```

Launch the driver:

```bash
ros2 launch oak_d_pro_driver oakd_camera_driver.launch.py \
  robot_name:=f450 robot_number:=1 \
  config:=sqrtVINS_config.yaml
```

### Launch arguments

| Argument | Default | Description |
|---|---|---|
| `robot_name` | — | Robot name, used as ROS namespace prefix |
| `robot_number` | `` | Optional number appended to robot name (`<name>_<number>`) |
| `name` | `oak` | Camera node name |
| `config` | — | Config filename relative to `config/<robot_name>/` |

### Config file

Platform-specific configuration is stored in `config/<robot_name>/<config>.yaml`.
The file controls camera FPS, IMU rate, enabled streams and TF position.

Example: `config/f450/sqrtVINS_config.yaml`

```yaml
/**:
  ros__parameters:
    driver:
      i_tf_parent_frame: oak_parent_frame
      i_tf_cam_pos_x: '0.0'
      ...
    pipeline_gen:
      i_pipeline_type: Stereo
    stereo:
      i_fps: 60.0
      i_left_rect_publish_topic: true
      i_right_rect_publish_topic: true
    imu:
      i_gyro_freq: 400
```

## DepthAI ROS driver

The underlying driver is `depthai_ros_driver_v3`. To run it directly:

```bash
ros2 launch depthai_ros_driver_v3 driver.launch.py
ros2 launch depthai_ros_driver_v3 driver.launch.py use_rviz:=true
ros2 run depthai_ros_driver_v3 driver_node
```

Full driver documentation: https://docs.luxonis.com/software-v3/depthai/ros/driver/

## Author

Martin Kriz
