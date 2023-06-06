#!/usr/bin/env python3
from flask import Flask
from flask import request

import subprocess
import carla
import roslaunch
import rospy

rospy.init_node('server_database')

app = Flask(__name__)

client = carla.Client('10.10.30.199', 2000)
client.set_timeout(30.0)
world = client.get_world()


@app.route("/mapp/init", methods = ['POST'])
def hello_world():

    car_id = str(request.json['car_id']) #check the name of the dic
    vehicle = world.get_actor(int(car_id))
    role_name = vehicle.attributes.get("role_name", "")
    status = str(request.json['process'])
    print(role_name)
    goal = str(request.json['goal']) #check the name of the dic
    print(goal,status,car_id)
    # uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    # roslaunch.configure_logging(uuid)
    # cli_args = ['/home/mazz/carla-ros-bridge/catkin_ws/src/ros-bridge/carla_ad_demo/launch/carla_multi.launch','role_name:={}'.format(role_name),'goal_pose:={}'.format(goal),'car_id:={}'.format(car_id)]
    # roslaunch_args = cli_args[1:]
    # roslaunch_file = [(roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], roslaunch_args)]

    # parent = roslaunch.parent.ROSLaunchParent(uuid, roslaunch_file)


    # parent.start()
    # rospy.spin()
    command="roslaunch mapp selector.launch role_name:=" + role_name +' '+ "goal_pose:="+ goal +' '+"car_id:=" + car_id + ' ' + "status:=" + status
    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])

    return 'MAPP received ' + goal
# if __name__ == '__main__':
app.run(host="10.10.30.199", port=5000)#, debug=False, use_reloader=False)