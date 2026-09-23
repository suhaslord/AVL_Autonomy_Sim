from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    world = PathJoinSubstitution(
        [FindPackageShare("avl_gazebo_bringup"), "worlds", "empty_course.sdf"]
    )
    xacro_file = PathJoinSubstitution(
        [FindPackageShare("avl_sim_description"), "urdf", "tracked_rover.urdf.xacro"]
    )
    robot_description = {"robot_description": Command(["xacro ", xacro_file])}

    gazebo = ExecuteProcess(
        cmd=["ign", "gazebo", "-r", world],
        output="screen",
    )

    state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_description],
        output="screen",
    )

    spawn = TimerAction(
        period=2.0,
        actions=[
            Node(
                package="ros_gz_sim",
                executable="create",
                arguments=["-name", "marvin", "-topic", "robot_description"],
                output="screen",
            )
        ],
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist",
            "/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry",
            "/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock",
        ],
        output="screen",
    )

    return LaunchDescription([gazebo, state_publisher, spawn, bridge])
