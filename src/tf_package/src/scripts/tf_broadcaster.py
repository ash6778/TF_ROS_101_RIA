#! /usr/bin/env python
import rospy
import time
import tf
from turtle_tf_3d.get_model_gazebo_pose import GazeboModel

def handle_tf(pose_msg,robot_name):
    br = tf.TransformBroadcaster()
    br.sendTransform((pose_msg.position.x, pose_msg.position.y, pose_msg.position.z),
    (pose_msg.orientation.x, pose_msg.orientation.y, pose_msg.orientation.z, pose_msg.orientation.w), 
    rospy.Time.now(), robot_name, "/world")

def publish_tf():
    rospy.init_node("tf_publisher_node")
    robot_name_list = ['turtle1','turtle2','coke_can']
    gazebo_model_object = GazeboModel(robot_name_list)

    time.sleep(1) #Giving some time for models to load
    rospy.loginfo("Ready....Starting to publish transforms")

    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        for robot_name in robot_name_list:
            pose_now = gazebo_model_object.get_model_pose(robot_name)
            if not pose_now:
                print "The pose"+str(pose_now)+"is not ready yet. Please wait"
            else:
                handle_tf(pose_now, robot_name)
        rate.sleep()


if __name__=="__main__":
    try:
        publish_tf()
    except rospy.ROSInterruptException:
        pass
    
    
