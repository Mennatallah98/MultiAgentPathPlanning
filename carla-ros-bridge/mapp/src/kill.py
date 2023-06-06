#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

rospy.init_node('kill',anonymous=True)


role_name = rospy.get_param('~role_name')
print(role_name)


i=0


while(rospy.get_param('kill_{}'.format(role_name),0) != 1 ):
    # print(('kill_{}'.format(role_name))) 
    i = i +1



rospy.set_param('kill_{}'.format(role_name),0)    