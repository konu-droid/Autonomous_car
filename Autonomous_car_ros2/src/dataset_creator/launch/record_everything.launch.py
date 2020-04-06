from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='dataset_creator', node_executable='gather_data', output='screen'),
        Node(
            package='stereo_yolo3', node_executable='stereo_image_pub', output='screen')
    ])
