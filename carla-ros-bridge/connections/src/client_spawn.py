#!/usr/bin/env python3
import requests
import rospy
from std_msgs.msg import String


rospy.init_node('client')

def callback(car_id):
    # Data that we will send in post request.
    # print(car_id, type(car_id))
    data = {'car_id':car_id.data, 'vin':'TRUUT28N711364065'}
    # The POST request to our node server
    # url = 'http://10.10.30.229:4000/3'
    # url = 'http://10.10.30.41:3000/vehicle_id'
    url = 'http://10.10.30.229:6000/spawn'

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

rospy.Subscriber("vehicle_id", String, callback)
# spin() simply keeps python from exiting until this node is stopped
rospy.spin()