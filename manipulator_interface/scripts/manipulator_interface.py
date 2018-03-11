#!/usr/bin/env python

from numpy import clip, interp
import rospy

from vortex_msgs.msg import Manipulatom
from stepper import Stepper

COMPUTER = rospy.get_param('/computer')

STEPPER_NUM_STEPS = rospy.get_param('/stepper/steps_per_rev')
STEPPER_RPM = rospy.get_param('/stepper/default_speed_rpm')

STEPPER_VALVE_PINS = rospy.get_param('/stepper/pins/valve')
STEPPER_VALVE_ENABLE_PIN = rospy.get_param('/stepper/pins/valve_enable')

def servo_position_to_microsecs(thrust):
    return interp(thrust, LOOKUP_POSITION, LOOKUP_PULSE_WIDTH)


def healthy_message(msg):
    if abs(msg.claw_direction) > 1:
        rospy.logwarn_throttle(1, 'Claw position out of range. Ignoring message...')
        return False

    if abs(msg.valve_direction) > 1:
        rospy.logwarn_throttle(1, 'Valve spinner command out of range. Ignoring message...')
        return False

    if abs(msg.agar_direction) > 1:
        rospy.logwarn_throttle(1, 'Agar screwer command out of range. Ignoring message...')
        return False

    return True


class ManipulatorInterface(object):
    def __init__(self):
        self.is_initialized = False
        rospy.init_node('manipulator_interface', anonymous=False)
        self.pub = rospy.Publisher('pwm', Pwm, queue_size=1)
        self.sub = rospy.Subscriber('manipulator_command', Manipulator, self.callback)

        self.neutral_pulse_width = servo_position_to_microsecs(0)

        rospy.sleep(0.1)  # Initial set to zero seems to disappear without a short sleep here
        self.servo_set_to_zero()
        rospy.on_shutdown(self.shutdown)
        self.claw_direction = 0.0
        self.claw_position = 0.0  # 1 = open, -1 = closed
        self.claw_speed = 1.0

        try:
            self.valve_stepper = Stepper(STEPPER_NUM_STEPS,
                                         STEPPER_VALVE_PINS,
                                         STEPPER_VALVE_ENABLE_PIN,
                                         COMPUTER)
            self.valve_direction = 0

            self.agar_stepper = Stepper(STEPPER_NUM_STEPS,
                                        STEPPER_AGAR_PINS,
                                        STEPPER_AGAR_ENABLE_PIN,
                                        COMPUTER)
            self.agar_direction = 0
        except NameError:
            rospy.logfatal('Could not initialize stepper.py. Is /computer parameter set correctly? '
                           'Shutting down node...')
            rospy.signal_shutdown('')

        self.valve_stepper.disable()
        self.agar_stepper.disable()

        rospy.loginfo('Initialized with {0} RPM steppers.'.format(STEPPER_RPM))
        self.is_initialized = True
        self.spin()

    def spin(self):
        period = 60.0 / (STEPPER_NUM_STEPS * STEPPER_RPM)
        rate = rospy.Rate(1/period)
        prev_time = rospy.get_rostime()
        min_pwm_interval = rospy.Duration(0.1)

        while not rospy.is_shutdown():
            # Accumulate claw position
            self.claw_position += self.claw_speed * period * self.claw_direction
            # Saturate claw position to [-1, 1]
            self.claw_position = clip(self.claw_position, -1, 1)

            # Step steppers if nonzero direction
            if abs(self.valve_direction) == 1:
                self.valve_stepper.step_once(self.valve_direction)
            if abs(self.agar_direction) == 1:
                self.agar_stepper.step_once(self.agar_direction)

            # Move servo if nonzero direction
            if abs(self.claw_direction) == 1:
                if (rospy.get_rostime() - prev_time) > min_pwm_interval:
                    self.set_claw_pwm(self.claw_position)
                    prev_time = rospy.get_rostime()

            rate.sleep()

    def servo_set_to_zero(self):
        msg = Pwm()
        msg.pins.append(SERVO_PWM_PIN)
        msg.positive_width_us.append(self.neutral_pulse_width)
        self.pub.publish(msg)
        if self.is_initialized:
            rospy.loginfo("Setting servo position to zero")

    def servo_disable(self):
        msg = Pwm()
        msg.pins.append(SERVO_PWM_PIN)
        msg.positive_width_us.append(0)
        self.pub.publish(msg)

    def shutdown(self):
        self.servo_disable()
        self.valve_stepper.shutdown()

    def callback(self, msg):
        if not self.is_initialized:
            rospy.logwarn('Callback before node initialized, ignoring...')
            return

        if not healthy_message(msg):
            return

        self.claw_direction = msg.claw_direction

        if msg.valve_direction != self.valve_direction:
            self.valve_direction = msg.valve_direction
            if self.valve_direction == 0:
                self.valve_stepper.disable()
            else:
                self.valve_stepper.enable()

        if msg.agar_direction != self.agar_direction:
            self.agar_direction = msg.agar_direction
            if self.agar_direction == 0:
                self.agar_stepper.disable()
            else:
                self.agar_stepper.enable()

    def set_claw_pwm(self, position):
        microsecs = servo_position_to_microsecs(position)

        msg = Pwm()
        msg.pins.append(SERVO_PWM_PIN)
        msg.positive_width_us.append(microsecs)

        self.pub.publish(msg)


if __name__ == '__main__':
    try:
        manipulator_interface = ManipulatorInterface()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
