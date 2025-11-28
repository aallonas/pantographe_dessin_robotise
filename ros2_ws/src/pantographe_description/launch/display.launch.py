#!/usr/bin/env python3

import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node


def generate_launch_description():

    pkg_path = get_package_share_directory('pantographe_description')
    urdf_path = os.path.join(pkg_path, 'urdf', 'pantographe.urdf')

    # Optional RViz config
    rviz_config_path = os.path.join(pkg_path, 'rviz', 'view.rviz')

    use_gui = LaunchConfiguration("use_gui")

    return LaunchDescription([

        DeclareLaunchArgument(
            name="use_gui",
            default_value="true",
            description="Use joint_state_publisher_gui"
        ),

        # Joint State Publisher (GUI or non-GUI)
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            condition=use_gui,
            name="joint_state_publisher_gui"
        ),

        Node(
            package="joint_state_publisher",
            executable="joint_state_publisher",
            condition=~use_gui,
            name="joint_state_publisher"
        ),

        # Robot State Publisher
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            parameters=[{"robot_description": open(urdf_path).read()}]
        ),

        # RViz
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", rviz_config_path]
        )
    ])

