#!/usr/bin/env python3
# license removed for brevity
import rospy
from geometry_msgs.msg import PoseStamped
import sys

goal = PoseStamped()
def node(id,pose):
    print('in')
    role_name = id
    position = pose
    pub = rospy.Publisher("/carla/{}/goal".format(role_name), PoseStamped, queue_size=10)
    rospy.init_node('goal_pub', anonymous=True)
    goal.pose.position.x = float(position.split(',')[0])
    goal.pose.position.y = float(position.split(',')[1])
    goal.pose.position.z = 0.0
    goal.pose.orientation.x = 0.0
    goal.pose.orientation.y = 0.0
    goal.pose.orientation.z = 0.707
    goal.pose.orientation.w = 0.707
    pub.publish(goal)

if __name__ == '__main__':
    try:
        myargv = rospy.myargv(argv=sys.argv)
        node(myargv[1],myargv[2])
    except rospy.ROSInterruptException:
        pass