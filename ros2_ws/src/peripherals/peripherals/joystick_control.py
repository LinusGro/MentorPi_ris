#!/usr/bin/env python3
# encoding: utf-8
import os
import math
import rclpy
from enum import Enum
from rclpy.node import Node
from sdk.common import val_map
from std_srvs.srv import Trigger
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from ros_robot_controller_msgs.msg import BuzzerState
from ros_robot_controller_msgs.msg import BuzzerState, SetPWMServoState, PWMServoState


AXES_MAP = 'lx', 'ly', 'rx', 'ry', 'r2', 'l2', 'hat_x', 'hat_y'
BUTTON_MAP = 'cross', 'circle', '', 'square', 'triangle', '', 'l1', 'r1', 'l2', 'r2', 'select', 'start', '', 'l3', 'r3', '', 'hat_xl', 'hat_xr', 'hat_yu', 'hat_yd', ''

class ButtonState(Enum):
    Normal = 0
    Pressed = 1
    Holding = 2
    Released = 3


class JoystickController(Node):
    def __init__(self, name):
        rclpy.init()
        super().__init__(name)

        #PWM servo setup
        self.servo1_state = PWMServoState()
        self.servo2_state = PWMServoState()

        self.min_value = 0.1
        self.declare_parameter('max_linear', 0.7)
        self.declare_parameter('max_angular', 3.0)
        self.declare_parameter('disable_servo_control', True)

        self.max_linear = self.get_parameter('max_linear').value
        self.max_angular = self.get_parameter('max_angular').value
        self.disable_servo_control = self.get_parameter('disable_servo_control').value
        self.machine = os.environ['MACHINE_TYPE']
        self.get_logger().info('\033[1;32m%s\033[0m' % self.max_linear)
        self.servo_state_pub = self.create_publisher(SetPWMServoState, 'ros_robot_controller/pwm_servo/set_state', 1)
        self.joy_sub = self.create_subscription(Joy, '/joy', self.joy_callback, 1)
        self.buzzer_pub = self.create_publisher(BuzzerState, 'ros_robot_controller/set_buzzer', 1)
        self.mecanum_pub = self.create_publisher(Twist, 'controller/cmd_vel', 1)

        self.last_axes = dict(zip(AXES_MAP, [0.0, ] * len(AXES_MAP)))
        self.last_buttons = dict(zip(BUTTON_MAP, [0.0, ] * len(BUTTON_MAP)))
        self.mode = 0
        self.create_service(Trigger, '~/init_finish', self.get_node_state)
        self.get_logger().info('\033[1;32m%s\033[0m' % 'start')
        self.init_servo()

    def get_node_state(self, request, response):
        response.success = True
        return response

    def axes_callback(self, axes):
        twist = Twist()
        if abs(axes['lx']) < self.min_value:
            axes['lx'] = 0
        if abs(axes['ly']) < self.min_value:
            axes['ly'] = 0
        if abs(axes['rx']) < self.min_value:
            axes['rx'] = 0
        if abs(axes['ry']) < self.min_value:
            axes['ry'] = 0

        if self.machine == 'MentorPi_Mecanum':
            twist.linear.y = val_map(axes['lx'], -1, 1, -self.max_linear, self.max_linear)
            twist.linear.x = val_map(axes['ly'], -1, 1, -self.max_linear, self.max_linear)
            twist.angular.z = val_map(axes['rx'], -1, 1, -self.max_angular, self.max_angular)
        elif self.machine == 'JetRover_Tank':
            twist.linear.x = val_map(axes['ly'], -1, 1, -self.max_linear, self.max_linear)
            twist.angular.z = val_map(axes['rx'], -1, 1, -self.max_angular, self.max_angular)
        elif self.machine == 'MentorPi_Acker':
            twist.linear.x = val_map(axes['ly'], -1, 1, -self.max_linear, self.max_linear)
            steering_angle = val_map(axes['rx'], -1, 1, -math.radians(322 / 2000 * 180), math.radians(322 / 2000 * 180))

            if steering_angle == 0:
                twist.angular.z = 0.0
                servo_state = PWMServoState()
                servo_state.id = [3]
                servo_state.position = [1500]
                data = SetPWMServoState()
                data.state = [servo_state]
                data.duration = 0.02
                self.servo_state_pub.publish(data)
            else:
                R = 0.145 / math.tan(steering_angle)
                twist.angular.z = float(twist.linear.x / R)

                servo_state = PWMServoState()
                servo_state.id = [3]
                servo_state.position = [1500 + int(math.degrees(-steering_angle) / 180 * 2000)]
                data = SetPWMServoState()
                data.state = [servo_state]
                data.duration = 0.02
                self.servo_state_pub.publish(data)

        self.mecanum_pub.publish(twist)



    def select_callback(self, new_state):
        pass

    def l1_callback(self, new_state):
        pass

    def l2_callback(self, new_state):
        pass

    def r1_callback(self, new_state):
        pass

    def r2_callback(self, new_state):
        pass

    def square_callback(self, new_state):
        pass

    def cross_callback(self, new_state):
        pass

    def circle_callback(self, new_state):
        pass

    def triangle_callback(self, new_state):
        pass

    def start_callback(self, new_state):
        if new_state == ButtonState.Pressed:
            self.init_servo()
            msg = BuzzerState()
            msg.freq = 2500
            msg.on_time = 0.05
            msg.off_time = 0.01
            msg.repeat = 1
            self.buzzer_pub.publish(msg)

    def hat_xl_callback(self, new_state):
        self.get_logger().info("xl callback")
        if new_state == ButtonState.Pressed:
            # Start a repeating timer
            self.dpad_timer = self.create_timer(0.01, self.dpad_left_action)
        elif new_state == ButtonState.Released:
            # Cancel the timer
            if self.dpad_timer:
                self.dpad_timer.cancel()
                self.dpad_timer = None

    def hat_xr_callback(self, new_state):
        self.get_logger().info("xr callback")
        if new_state == ButtonState.Pressed:
            # Start a repeating timer
            self.dpad_timer = self.create_timer(0.01, self.dpad_right_action)
        elif new_state == ButtonState.Released:
            # Cancel the timer
            if self.dpad_timer:
                self.dpad_timer.cancel()
                self.dpad_timer = None

    def hat_yd_callback(self, new_state):
        self.get_logger().info("yd callback")
        if new_state == ButtonState.Pressed:
            # Start a repeating timer
            self.dpad_timer = self.create_timer(0.01, self.dpad_down_action)
        elif new_state == ButtonState.Released:
            # Cancel the timer
            if self.dpad_timer:
                self.dpad_timer.cancel()
                self.dpad_timer = None

    def hat_yu_callback(self, new_state):
        self.get_logger().info("yu callback")
        if new_state == ButtonState.Pressed:
            # Start a repeating timer
            self.dpad_timer = self.create_timer(0.01, self.dpad_up_action)
        elif new_state == ButtonState.Released:
            # Cancel the timer
            if self.dpad_timer:
                self.dpad_timer.cancel()
                self.dpad_timer = None


    def dpad_left_action(self):
        if self.servo1_state.position[0] < 2000:
            self.servo1_state.position[0] += 5
        self.publish_servo(self.servo1_state)

    def dpad_right_action(self):
        if self.servo1_state.position[0] > 1000:
            self.servo1_state.position[0] -= 5
        self.publish_servo(self.servo1_state)

    def dpad_down_action(self):
        if self.servo2_state.position[0] < 2000:
            self.servo2_state.position[0] += 5
        self.publish_servo(self.servo2_state)

    def dpad_up_action(self):
        if self.servo2_state.position[0] > 1000:
            self.servo2_state.position[0] -= 5
        self.publish_servo(self.servo2_state)

    def publish_servo(self, servo_state):
        data = SetPWMServoState()
        data.state = [servo_state]
        data.duration = 0.01
        self.servo_state_pub.publish(data)

    def init_servo(self):
        self.servo1_state.id = [2] #horisontal
        self.servo1_state.position = [1500]
        self.publish_servo(self.servo1_state)

        self.servo2_state.id = [1] #vertical
        self.servo2_state.position = [1500]
        self.publish_servo(self.servo2_state)

    def joy_callback(self, joy_msg):
        axes = dict(zip(AXES_MAP, joy_msg.axes))
        axes_changed = False
        hat_x, hat_y = axes['hat_x'], axes['hat_y']

        hat_xr = 1 if hat_x < -0.5 else 0
        hat_xl = 1 if hat_x > 0.5 else 0
        hat_yu = 1 if hat_y > 0.5 else 0
        hat_yd = 1 if hat_y < -0.5 else 0

        buttons = list(joy_msg.buttons)
        buttons += [0] * (len(BUTTON_MAP) - len(buttons))  # Ensure `buttons` matches `BUTTON_MAP` length
        buttons[BUTTON_MAP.index('hat_xl')] = hat_xl
        buttons[BUTTON_MAP.index('hat_xr')] = hat_xr
        buttons[BUTTON_MAP.index('hat_yu')] = hat_yu
        buttons[BUTTON_MAP.index('hat_yd')] = hat_yd
        buttons = dict(zip(BUTTON_MAP, buttons))

        for key, value in axes.items():
            if self.last_axes[key] != value:
                axes_changed = True
        if axes_changed:
            try:
                self.axes_callback(axes)
            except Exception as e:
                self.get_logger().error(str(e))
        for key, value in buttons.items():
            if value != self.last_buttons[key]:
                new_state = ButtonState.Pressed if value > 0 else ButtonState.Released
            else:
                new_state = ButtonState.Holding if value > 0 else ButtonState.Normal
            callback = "".join([key, '_callback'])
            if new_state != ButtonState.Normal:
                self.get_logger().info(str(new_state))
                if  hasattr(self, callback):
                    try:
                        getattr(self, callback)(new_state)
                        self.get_logger().info(callback)
                    except Exception as e:
                        self.get_logger().error(str(e))
        self.last_buttons = buttons
        self.last_axes = axes

def main():
    node = JoystickController('joystick_control')
    rclpy.spin(node)

if __name__ == "__main__":
    main()
