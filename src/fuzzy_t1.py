#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty
from csv import reader

x = 0
y = 0
theta = 0
x2 = 0
y2 = 0
theta2= 0

def poseCallback1(pose_message):
    global x
    global y
    global theta
    x = pose_message.x
    y = pose_message.y
    theta = pose_message.theta

def poseCallback2(pose_message):
    global x2
    global y2
    global theta2
    x2 = pose_message.x
    y2 = pose_message.y
    theta2 = pose_message.theta
    
def go_to_goal (xgoal, ygoal):
    while(True):
        if theta > math.pi:
            pm_theta = (theta-(2*math.pi))*(180/math.pi)
        else:
            pm_theta = theta*(180/math.pi)
        # print("theta: ", round(theta,3), "\t pm_theta: ", round(pm_theta,3))
        gtheta = (math.atan2(ygoal-y, xgoal-x))*(180/math.pi)
        # print("gtheta: ", round(gtheta,3))
        dtheta = gtheta - pm_theta
        if dtheta > 180:
            dtheta = int(dtheta - 360)
        if dtheta < -180:
            dtheta = int(dtheta + 360)
        dtheta = int(dtheta * -1)
        # print("dtheta: ", dtheta)
        dist = int(round(math.sqrt((x2-x)**2 + (y2-y)**2), 1) * 10)
        # print("dist: ", dist)
        with open("~/surface_out1.csv", 'r') as read_obj:
            csv_reader = reader(read_obj)
            list_z = list(csv_reader)
        z_surface_out1 = [list(map(float, sublist)) for sublist in list_z]
        with open("~/surface_out2.csv", 'r') as read_obj:
            csv_reader = reader(read_obj)
            list_z = list(csv_reader)
        z_surface_out2 = [list(map(float, sublist)) for sublist in list_z]
        cmd_vel = Twist()
        cmd_vel.linear.x = z_surface_out1[dtheta + 180][dist] * 4.0 * 0
        cmd_vel.linear.y = 0
        cmd_vel.linear.z = 0
        cmd_vel.angular.x = 0
        cmd_vel.angular.y = 0
        cmd_vel.angular.z = (z_surface_out2[dtheta + 180][dist] * 4.0) - 2.0
        velocity_publisher.publish(cmd_vel)
        rospy.loginfo(cmd_vel)
        break

if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_motion_pose', anonymous = True) 
        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size = 10)
        position_topic1 = "/turtle1/pose"
        pose_subscriber1 = rospy.Subscriber(position_topic1, Pose, poseCallback1)
        position_topic2 = "/turtle2/pose"
        pose_subscriber2 = rospy.Subscriber(position_topic2, Pose, poseCallback2)
        time.sleep(1.0)
        while(True):         
            go_to_goal(x2,y2)             
    except rospy.ROSInterruptException:        
        pass
