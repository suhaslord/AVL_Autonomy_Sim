cmake_minimum_required(VERSION 3.8)
project(avl_gazebo_bringup)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY ../../gazebo/worlds/
  DESTINATION share/${PROJECT_NAME}/worlds
)

ament_package()
