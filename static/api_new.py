import requests
import json

url = "http://localhost:7000/get_activity_timeinterval"

payload = json.dumps({
  "transaction_id": "daedf16f-b81d-4139-8937-7775df87b7ca",
  "start_datetime": "2017-07-12 12:23:15",
  "end_datetime": "2017-07-12 12:23:20"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

data_dict = json.loads(response.text)

print(data_dict)

print(data_dict['activities_and_recommendations'])