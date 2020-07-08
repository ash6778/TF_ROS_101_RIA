#! /usr/bin/env python

import rospy
import time
import math
import tf 
import sys
from geometry_msgs.msg import Twist

if __name__=="__main__":
    rospy.init_node("tf_listener_node")
    
    listener = tf.TransformListener()
    if len(sys.argv) < 3:
        print ("update: tf_listener.py follower_model_name model_to_be_followed_name")
    else:
        follower_model_name = sys.argv[1]
        model_to_be_followed_name = sys.argv[2]

        robot_vel = rospy.Publisher(follower_model_name+'/cmd_vel', Twist, queue_size = 5)

        rate = rospy.Rate(10)
        ctrl_c = False

        follower_model_frame = "/"+follower_model_name
        model_to_be_followed_frame = "/"+model_to_be_followed_name

        def shutdownhook():
            global ctrl_c
            print "Time to shutdown!"
            vel = Twist()
            vel.linear.x = 0
            vel.angular.z = 0
            robot_vel.publish(vel)
            ctrl_c = True 
        
        rospy.on_shutdown(shutdownhook)

        while not ctrl_c:
            try:
                (trans,rot) = listener.lookupTransform(follower_model_frame, model_to_be_followed_frame, rospy.Time(0))
            except (tf.ConnectivityException, tf.ExtrapolationException, tf.LookupException):
                continue
            
            angular = 4*math.atan2(trans[1],trans[0])
            linear = 0.5 * math.sqrt(trans[0]**2 + trans[1]**2)
            vel = Twist()
            vel.linear.x = linear
            vel.angular.z = angular
            robot_vel.publish(vel)

            rate.sleep()


    




        

            


        