#!/usr/bin/env python3
import requests
import rospy
from std_msgs.msg import String


rospy.init_node('client_obs')

car_id = rospy.get_param("~car_id")
role_name = rospy.get_param("~role_name")

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

def callback(data):
    # Data that we will send in post request.
    # print(car_id, type(car_id))
    data = {'status':data.data, 'car_id':car_id}
    # The POST request to our node server
    ip='http://10.10.30.229:'

    port=str(hashing_port(str(car_id)))

    route='/oh'

    url = ip+port+route

    try:


        res = requests.post(url, json=data)
        print(res)
        # Convert response data to json

        # returned_data = res#.json()

        # print(returned_data[])

        # result = returned_data['result']

        # print("Sum of Array from Node.js:", result)

        

    except:

        print("error")

        #time.sleep(30)

rospy.Subscriber("kill_{}".format(role_name), String, callback)
# spin() simply keeps python from exiting until this node is stopped
rospy.spin()