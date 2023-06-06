import requests
import time

# Data that we will send in post request.
data = {'id': "'hero2'" , 'pose': "'-157.0,-5.2,2,0,0,0.707,0.707'"}

# The POST request to our node server
url = 'http://10.10.30.199:3000/'

try:
    res = requests.post(url, json=data)
    # Convert response data to json
    # returned_data = res#.json()
    # print(returned_data[])
    # result = returned_data['result']
    # print("Sum of Array from Node.js:", result)
    
except:
    print("error")
    #time.sleep(30)