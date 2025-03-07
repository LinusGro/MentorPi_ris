#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import rclpy
import signal
import threading
from rclpy.node import Node
from tf2_ros.buffer import Buffer
from math import copysign, sqrt, pow
from geometry_msgs.msg import Twist, Point
from tf2_ros.transform_listener import TransformListener
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException

class CalibrateLinear(Node):
    def __init__(self, name):
        rclpy.init()
        super().__init__(name)
        signal.signal(signal.SIGINT, self.shutdown)

        #declare parameters
        self.declare_parameter('test_distance', 1.0)
        self.declare_parameter('speed', 0.2)        
        self.declare_parameter('tolerance', 0.03)
        self.declare_parameter('odom_linear_scale_correction', 1.0)
        self.declare_parameter('start_test', False)
        self.update_param()
        
        self.odom_frame = 'odom'
        self.base_frame = 'base_footprint'
        self.cmd_vel = self.create_publisher(Twist,"/controller/cmd_vel", 1)
       
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        self.position = Point()
        self.x_start = self.position.x
        self.y_start = self.position.y    
        
        self.clock = self.get_clock()
        threading.Thread(target=self.main, daemon=True).start()
        
        self.get_logger().info('\033[1;32m%s\033[0m' % 'Bring up rqt_reconfigure to control the test')  

    def update_param(self):
        self.start_test = self.get_parameter('start_test').value
        self.test_distance = self.get_parameter('test_distance').value
        self.speed = self.get_parameter('speed').value
        self.tolerance = self.get_parameter('tolerance').value
        self.odom_linear_scale_correction = self.get_parameter('odom_linear_scale_correction').value

    def main(self):
        while True:
            self.update_param()
            move_cmd = Twist()
            if self.start_test:
                # Get the current position from the tf transform between the odom and base frames
                self.position = self.get_position()

                # Compute the Euclidean distance from the target point
                original_distance = sqrt(pow((self.position.transform.translation.x - self.x_start), 2) +
                                pow((self.position.transform.translation.y - self.y_start), 2))

                # Correct the estimated distance by the correction factor
                calib_distance = original_distance * self.odom_linear_scale_correction

                # How close are we?
                error = calib_distance - self.test_distance
                # self.get_logger().info('\033[1;32moriginal:%f calib:%f\033[0m' % (original_distance, calib_distance))
                # Are we close enough?
                if not self.start_test or abs(error) <  self.tolerance:
                    self.start_test = rclpy.parameter.Parameter('start_test', rclpy.Parameter.Type.BOOL, False)
                    all_new_parameters = [self.start_test]
                    self.set_parameters(all_new_parameters)
                    self.get_logger().info('\033[1;32m%s\033[0m' % 'finish')
                else:
                    # If not, move in the appropriate direction
                    move_cmd.linear.x = copysign(self.speed, -1 * error)
            else:
                self.position = self.get_position()
                if self.position is not None:
                    self.x_start = self.position.transform.translation.x
                    self.y_start = self.position.transform.translation.y

            self.cmd_vel.publish(move_cmd)
            time.sleep(0.05)

    def get_position(self):
        # Get the current transform between the odom and base frames
        try:
            trans = self.tf_buffer.lookup_transform(self.odom_frame, self.base_frame, rclpy.time.Time(), timeout=rclpy.duration.Duration(seconds=1))
            return trans
        except (LookupException, ConnectivityException, ExtrapolationException):
            self.get_logger().info('\033[1;32m%s\033[0m' % 'TF Exception')
            return None

    def shutdown(self, signum, frame):
        # Always stop the robot when shutting down the node
        self.get_logger().info('\033[1;32m%s\033[0m' % 'Stopping the robot...')
        self.start_test = False
        self.cmd_vel.publish(Twist())
        rclpy.shutdown()

def main():
    node = CalibrateLinear('calibrate_linear')
    rclpy.spin(node)  # 循环等待ROS2退出(loop waiting for ROS2 to exit)

if __name__ == "__main__":
    main()
