#!/usr/bin/env python3

# import libraries
from carla_msgs.msg import CarlaEgoVehicleInfo
from nav_msgs.msg import Odometry, Path
import rospy
import sys
import numpy as np
from std_msgs.msg import String, Int32
from geometry_msgs.msg import PoseStamped
import time
from carla_waypoint_types.srv import *
import subprocess
import time
#-------------------------------------------------------------------------------------------


rospy.init_node('mapp', anonymous=True)  # initiate the node

# intialising dictionaries that will be used through out the code
paths = {}
ids={}
agents_waypoints = {}
#---------------------------------------------------------------------------------


rate = rospy.Rate(20)  

# gets the nearest waypoint to the agent current location to know at wich waypoint each agent is when a new agent enters
def nearest_waypoint(point,path):
    datum_x = 1000
    datum_y = 1000
    start_index = 0
    for i,waypoint in enumerate(path) :
        dif_x = abs(waypoint[0]-point[0])
        dif_y = abs(waypoint[1]-point[1])
        if dif_x < datum_x and dif_y < datum_y :
            start_index = i
            datum_x = dif_x
            datum_y = dif_y
    return start_index
#----------------------------------------------------------------------------------------------------------------------------------------------

# checks if there is any intersection between 2 paths
def collision_checker(path1,path2):
    for index in range(len(path1)):
        if (abs(int(path1[index][0]) - int(path2[index][0])) < 30) and (int(path1[index][1]) == int(path2[index][1])):

            return True
    return False
#-------------------------------------------------------------------------------------------------------------------------------------------------

# saves the ID for each agent given their role name
def identification(info):
    ids[info.rolename]=info.id
#-----------------------------------------------------------------------------------------------------------------------------------------------

# gets the waypoint for the alternative paths
def waypoints_mapp(waypoints_mapp):
    global waypoints_new
    global flag
    global counter
    waypoints_new = waypoints_mapp
    flag ='blue'
#-----------------------------------------------------------------------------------------------------------------------------------------  

# the main function that checks for collision between the new agent and the running agent 
def waypoints(points):
    print('Algorithm is in progress')
    global role_name
    global waypoints_new
    global counter
    global paths_number
    global flag
    global in_fn
    global shortest_path
    
    flag ='red'
    counter += 1 
    in_fn +=1


    if in_fn ==1:  # saves the shortest path so if all paths failed returns to it
        shortest_path=points
    else:
        print('looking for alternative paths and checking for collisions')

    if counter ==1 :  #make sure the agent enters the function only once 
        new_agent_path = [(pose.pose.position.x,pose.pose.position.y) for pose in points.poses]
        goal = str(new_agent_path[-1]).replace('(', '"').replace(')', '"')  # puts the goal in the approprite form
        waypoints_pub = rospy.Publisher("/carla/{}/waypoints_modified".format(role_name), Path, queue_size=10)
        goal_pub = rospy.Publisher("/carla/{}/goal".format(role_name), PoseStamped, queue_size=10)
        rospy.Subscriber("/carla/{}/waypoints_mapp".format(role_name),Path,callback=waypoints_mapp)

        if paths: # checks if this is the first agent 
            
            keys=paths.keys()
            for hero in keys:  # loops over all the running agents 
                agent_waypoint = rospy.ServiceProxy('/carla_waypoint_publisher/{}/get_actor_waypoint'.format(hero), GetActorWaypoint)
                old_agent_waypoint = agent_waypoint(ids[hero])
                old_agent_pose = (old_agent_waypoint.waypoint.pose.position.x,old_agent_waypoint.waypoint.pose.position.y)

                # adjust the length of the paths
                start_index = nearest_waypoint(old_agent_pose,paths[hero])
                adjusted_start = paths[hero][start_index:]
                if len(new_agent_path) > len(adjusted_start):
                    new_agent_path_adjusted = new_agent_path[:len(adjusted_start)]
                    old_agent_path_adjusted = adjusted_start
                elif len(new_agent_path) < len(adjusted_start):
                    new_agent_path_adjusted = new_agent_path
                    old_agent_path_adjusted = adjusted_start[:len(new_agent_path)]
                else :
                    new_agent_path_adjusted = new_agent_path
                    old_agent_path_adjusted = adjusted_start
                #-----------------------------------------------------------------------

                collision = collision_checker(new_agent_path_adjusted,old_agent_path_adjusted)
                print('Is there a collision ?',collision)

                if collision:
                    print('collision is gonna occur')
                    if paths_number==0: # launch the planner that gives alternative paths and get the first path 
                        paths_number+=1
                        # print(paths_number)
                        # print(goal)
                        command="roslaunch mapp carla_waypoint_publisher_mapp.launch role_name:=" + role_name +' '+ "goal_pose:="+ goal 
                        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])
                        rate.sleep()
                        print('waiting for alternative path')
                        while (flag =='red'):
                            wahed=1
                        counter =0 
                        # print(flag)
                        waypoints(waypoints_new)  # returns to the function to check the avlibality of the path
                        return 0

                    else: # loops through the other paths
                        goal_given = PoseStamped()
                        goal_given.pose.position.x = float(eval(goal.split(',')[0].replace('"', '')))
                        goal_given.pose.position.y = float(eval(goal.split(',')[1].replace('"', '')))
                        goal_given.pose.position.z = 2.0
                        goal_given.pose.orientation.x = 0.0
                        goal_given.pose.orientation.y = 0.0
                        goal_given.pose.orientation.z = 0.707
                        goal_given.pose.orientation.w = 0.707
                        goal_pub.publish(goal_given)
                        
                        if waypoints_new.header.frame_id == "no paths found": # if no path is available it returns to the shortest path 
                            print("no paths found")
                            counter =0
                            print('we are taking the shortest path again in case no collision')
                            waypoints(shortest_path)
                            paths_number=0
                            return 0
                        else:
                            counter =0
                            waypoints(waypoints_new)
                            paths_number+=1
                            return 0
                        
                    
            print('out of loop')

            paths[role_name] = [(pose.pose.position.x,pose.pose.position.y) for pose in points.poses]
            agents_waypoints[role_name] = points

            # print(waypoints_pub.get_num_connections())
            old_connections = waypoints_pub.get_num_connections()
            rate.sleep()
            if (waypoints_pub.get_num_connections()>=1):
                rate.sleep()
                waypoints_pub.publish(points)
            elif (waypoints_pub.get_num_connections()==0):
                while(waypoints_pub.get_num_connections()==0) :
                    rate.sleep()
                    waypoints_pub.publish(points)
                    # print("pub")
            # print(waypoints_pub.get_num_connections())
            # print(counter)

            print('############################')


        else : # For the first agent as it does not need comparison with others  
            print('first agent')
            print('############################')

            paths[role_name] = [(pose.pose.position.x,pose.pose.position.y) for pose in points.poses]
            agents_waypoints[role_name] = points
            rate.sleep()
            if (waypoints_pub.get_num_connections()>=1):
                rate.sleep()
                waypoints_pub.publish(points)
            elif (waypoints_pub.get_num_connections()==0):
                while(waypoints_pub.get_num_connections()==0) :
                    rate.sleep()
                    waypoints_pub.publish(points)
                    # print("pub")
    else:
        print('repeated process')
#-------------------------------------------------------------------------------------------------------------------------------

# function that indicates the entrance of a new agent or the start of a retrival process
def mapp(data):
    global role_name
    global counter
    global paths_number
    global in_fn
    counter = 0
    in_fn = 0
    paths_number=0   
    role_name = data.data
    print('vehicle {} is being processed'.format(role_name))
    id_subscriber = rospy.Subscriber("/carla/{}/vehicle_info".format(role_name), CarlaEgoVehicleInfo, callback=identification)
    path_subscriber = rospy.Subscriber("/carla/{}/waypoints".format(role_name),Path,callback=waypoints)
    alternative_paths_subscriber=rospy.Subscriber("/carla/{}/waypoints_mapp".format(role_name),Path,callback=waypoints_mapp)


# Remove the agent from being taken in consideration after it parks
def update_paths(agent):
    print('agent reached its goal: ',agent)
    paths.pop(agent.data)
#----------------------------------------------------------------------------   


rospy.Subscriber("new_agent",String,callback=mapp)
rospy.Subscriber("update_paths",String,callback=update_paths)

# indicates the start of the node
print('^^^^^')
print('start')
#--------------------------------------

rospy.spin()  # keeps the code running


    

    

