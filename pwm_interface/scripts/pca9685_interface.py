#!/usr/bin/env python

import Adafruit_PCA9685
import rospy
from vortex_msgs.msg import Pwm

# Constants
PWM_BITS_PER_PERIOD = rospy.get_param('/pwm/counter/max')
FREQUENCY = rospy.get_param('/pwm/frequency/set')
FREQUENCY_MEASURED = rospy.get_param('/pwm/frequency/measured')
PERIOD_LENGTH_IN_MICROSECONDS = 1000000.0 / FREQUENCY_MEASURED
PWM_ON = 0  # Start of duty cycle


class Pca9685InterfaceNode(object):
    def __init__(self):
        rospy.init_node('pwm_node')
        self.sub = rospy.Subscriber('pwm', Pwm, self.callback, queue_size=1)

        self.pca9685 = Adafruit_PCA9685.PCA9685()
        self.pca9685.set_pwm_freq(FREQUENCY)
        self.pca9685.set_all_pwm(0, 0)
        self.current_pwm = [0]*16

        rospy.on_shutdown(self.shutdown)

        rospy.loginfo('Initialized for {0} Hz.'.format(FREQUENCY))

    def callback(self, msg):
        if len(msg.pins) == len(msg.positive_width_us):
            for i in range(len(msg.pins)):
                if msg.positive_width_us[i] != self.current_pwm[msg.pins[i]]:
                    self.pca9685.set_pwm(msg.pins[i], PWM_ON, self.microsecs_to_bits(msg.positive_width_us[i]))
                    self.current_pwm[msg.pins[i]] = msg.positive_width_us[i]

    def microsecs_to_bits(self, microsecs):
        duty_cycle_normalized = microsecs / PERIOD_LENGTH_IN_MICROSECONDS
        return int(round(PWM_BITS_PER_PERIOD * duty_cycle_normalized))

    def shutdown(self):
        self.pca9685.set_all_pwm(0, 0)

if __name__ == '__main__':
    try:
        pwm_node = Pca9685InterfaceNode()
        rospy.spin()
    except IOError:
        rospy.logerr('IOError caught, shutting down.')
    except rospy.ROSInterruptException:
        pass
