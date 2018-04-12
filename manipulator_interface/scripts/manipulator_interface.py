#!/usr/bin/env python

from numpy import clip, interp
import rospy

from vortex_msgs.msg import Manipulator
from stepper import Stepper

COMPUTER = rospy.get_param('/computer')

STEPPER_NUM_STEPS = rospy.get_param('/stepper/steps_per_rev')
STEPPER_RPM = rospy.get_param('/stepper/default_speed_rpm')

STEPPER_CLAW_PINS = rospy.get_param('/stepper/pins/claw')
STEPPER_CLAW_PIN = rospy.get_param('/stepper/pins/claw_pwm')


def healthy_message(msg):
    if abs(msg.claw_direction) > 1:
        rospy.logwarn_throttle(1, 'Claw spinner command out of range. Ignoring message...')
        return False

    return True


class ManipulatorInterface(object):
    def __init__(self):
        self.is_initialized = False
        rospy.init_node('manipulator_interface', anonymous=False)
        self.sub = rospy.Subscriber('manipulator_command', Manipulator, self.callback)

        rospy.on_shutdown(self.shutdown)

        try:
            self.claw_stepper = Stepper(STEPPER_NUM_STEPS,
                                         STEPPER_CLAW_PINS,
                                         STEPPER_CLAW_ENABLE_PIN,
                                         COMPUTER)
            self.claw_direction = 0
        except NameError:
            rospy.logfatal('Could not initialize stepper.py. Is /computer parameter set correctly? '
                           'Shutting down node...')
            rospy.signal_shutdown('')

        self.claw_stepper.disable()

        rospy.loginfo('Initialized with {0} RPM steppers.'.format(STEPPER_RPM))
        self.is_initialized = True
        self.spin()

    def spin(self):
        period = 60.0 / (STEPPER_NUM_STEPS * STEPPER_RPM)
        rate = rospy.Rate(1/period)

        while not rospy.is_shutdown():
            # Step steppers if nonzero direction
            if abs(self.claw_direction) == 1:
                self.claw_stepper.step_once(self.claw_direction)

            rate.sleep()

    def shutdown(self):
        self.claw_stepper.shutdown()

    def callback(self, msg):
        if not self.is_initialized:
            rospy.logwarn('Callback before node initialized, ignoring...')
            return

        if not healthy_message(msg):
            return


        if msg.claw_direction != self.claw_direction:
            self.claw_direction = msg.claw_direction
            if self.claw_direction == 0:
                self.claw_stepper.disable()
            else:
                self.claw_stepper.enable()

        if msg.agar_direction != self.agar_direction:
            self.agar_direction = msg.agar_direction
            if self.agar_direction == 0:
                self.agar_stepper.disable()
            else:
                self.agar_stepper.enable()


if __name__ == '__main__':
    try:
        manipulator_interface = ManipulatorInterface()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
