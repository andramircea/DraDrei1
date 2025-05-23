#!/usr/bin/env python

import rospy
import actionlib
from actions_pkg.msg import ControlAction, ControlFeedback
from std_msgs.msg import Empty

class ActionServer:
    def __init__(self):
        self.server = actionlib.SimpleActionServer('drone_action', ControlAction, self.execute, False)
        self.feedback = ControlFeedback()
        self.takeoff_pub = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
        self.land_pub = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
        self.server.start()

    def execute(self, goal):
        rate = rospy.Rate(1)
        if goal.command == "TAKEOFF":
            self.takeoff_pub.publish(Empty())
            rospy.loginfo("Drone is taking off.")
            while not rospy.is_shutdown():
                self.feedback.current_action = "Taking off..."
                self.server.publish_feedback(self.feedback)
                rate.sleep()
               
        elif goal.command == "LAND":
            self.land_pub.publish(Empty())
            rospy.loginfo("Drone is landing.")
            for i in range(5):
                self.feedback.current_action = "Landing..."
                self.server.publish_feedback(self.feedback)
                rate.sleep()
        self.server.set_succeeded()

if __name__ == '__main__':
    rospy.init_node('drone_action_server')
    server = ActionServer()
    rospy.spin()
