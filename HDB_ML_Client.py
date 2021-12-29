import json
import requests

#url='http://127.0.0.1:5000/get_params'
url='http://127.0.0.1:5000/get_predictions'
request_data=json.dumps({'town':'BEDOK','floor_area':112,'flat_model':'Improved','street_name':'BEDOK CTRL','remaining_lease':87,'flat_type':'5 room','storey_range':'13 to 15'})
response = requests.post(url,request_data)
print(response.text)