#!/usr/bin/env python
import rospy
import Adafruit_BBIO.GPIO as GPIO
from vortex_msgs.msg import CameraFeedSelection

PIN_MAP_FEED0 = rospy.get_param('/camera/pin_map_feed0')
PIN_MAP_FEED1 = rospy.get_param('/camera/pin_map_feed1')
PIN_MAP_FEED2 = rospy.get_param('/camera/pin_map_feed2')
PIN_MAP_LIST = [PIN_MAP_FEED0, PIN_MAP_FEED1, PIN_MAP_FEED2]
NUM_FEEDS = 3


class CameraSelection(object):
    def __init__(self):
        rospy.init_node('camera_selection')
        self.cam_select_sub = rospy.Subscriber('camera_feed_selection', CameraFeedSelection, self.callback)
        # Set pin as output
        for pin_list in PIN_MAP_LIST:
            for pin in pin_list:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)

    def callback(self, msg):
        if msg.feed < NUM_FEEDS:
            # Get pin map for relevant feed
            feed_pin_map = PIN_MAP_LIST[msg.feed]
            # Convert selected camera to binary array
            cam_select = [int(bit) for bit in format(msg.camera, '03b')]
            for index, output_pin in enumerate(cam_select):
                if output_pin:
                    GPIO.output(feed_pin_map[index], GPIO.HIGH)
                else:
                    GPIO.output(feed_pin_map[index], GPIO.LOW)


if __name__ == '__main__':
    try:
        camera_selection = CameraSelection()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
