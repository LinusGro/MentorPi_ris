#!/usr/bin/env python3
# encoding: utf-8
import os
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
from sensor_msgs.msg import JointState
from ros_robot_controller_msgs.msg import BuzzerState, SetPWMServoState, PWMServoState
import yaml

class InitPose(Node):
    def __init__(self, name):
        rclpy.init()
        super().__init__(name, allow_undeclared_parameters=True, automatically_declare_parameters_from_overrides=True)  
        
        namespace = self.get_namespace()
        if namespace == '/':
            namespace = ''
       
        self.servo_state_pub = self.create_publisher(SetPWMServoState, 'ros_robot_controller/pwm_servo/set_state', 1)
        self.client = self.create_client(Trigger, namespace + '/controller_manager/init_finish')
        self.client.wait_for_service()
        
        config_path = os.path.join(os.environ['HOME'], 'workspace/ros2_ws/src/driver/controller/config/servo_config.yaml')

        with open(config_path, 'r') as file:
            servo_offsets = yaml.safe_load(file)

        pulse = self.get_parameters_by_prefix('servo')
        msg = SetPWMServoState()
        msg.duration = float(pulse['duration'].value)
        data = []   
        for i in ['id1', 'id2', 'id3', 'id4']:  
            servo = PWMServoState()
            servo.id = int(i[2:]) 
            offset = servo_offsets.get(str(servo.id), 0)
            servo.position = int(pulse[i].value) + offset + 1500
            data.append(servo)
        msg.servos = data
        self.servo_state_pub.publish(msg)

        self.create_service(Trigger, '~/init_finish', self.get_node_state)
        self.get_logger().info('\033[1;32m%s\033[0m' % 'start')

    def get_node_state(self, request, response):
        response.success = True
        return response

def main():
    node = InitPose('init_pose')
    rclpy.spin(node)  
if __name__ == "__main__":
    main()

