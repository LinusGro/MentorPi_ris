#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy

class JoyListener(Node):
    def __init__(self):
        super().__init__('joy_listener')
        self.subscription = self.create_subscription(
            Joy,
            '/joy',
            self.joy_callback,
            10)
        self.subscription 

    def joy_callback(self, msg):
        self.get_logger().info('Received Joy: Axes: %s Buttons: %s' % (msg.axes, msg.buttons))

def main(args=None):
    rclpy.init(args=args)
    joy_listener = JoyListener()
    rclpy.spin(joy_listener)
    joy_listener.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

