#!/usr/bin/env python3

from flask import Flask
from flask import request

import carla
import roslaunch
import rospy
import subprocess

rospy.init_node('server_obstacle',anonymous=True)

def hashing_port(id):
    print(len(id))
    if len(id)<2:
        str1=id[0]
        str2='1'
        str3='0'
        str4='1'
        port_str=str1+str2+str3+str4
        port_int=int(port_str)
    elif len(id)<3:
        str1=id[0]
        str2='1'
        str3=id[1]
        str4='1'
        port_str=str1+str2+str3+str4
        port_int=int(port_str)
    
    else:
        tr1=id[0]
        str2='1'
        str3=id[1]
        str4=id[2]
        port_str=str1+str2+str3+str4
        port_int=int(port_str)
    return port_int

app = Flask(__name__)

client = carla.Client('10.10.30.199', 2000)
client.set_timeout(30.0)
world = client.get_world()

rospy.set_param("obstacle_recieved",0)

#role_name = rospy.get_param("~role_name")
car_id = rospy.get_param("~car_id")
goal = rospy.get_param("~goal_pose")
print(car_id)
print(type(car_id))

@app.route("/", methods = ['POST'])
def hello_world():

    if (rospy.get_param("obstacle_recieved")==0):
        rospy.set_param("obstacle_recieved",1)
        print(request.json)
        car_id_new = request.json['id']
        print(car_id_new)
        vehicle = world.get_actor(int(car_id_new))
        print(vehicle)
        role_name=vehicle.attributes.get("role_name", "")
        print(role_name)

        command="roslaunch mapp bag.launch role_name:=" + role_name + ' ' + "goal_pose:=" + goal
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])
   
    else :
        print ('Maneuvering is in-progress')

if __name__ == '__main__':
    app.run(host="10.10.30.199", port=hashing_port(str(car_id)))
##port is an argument given based on id 
