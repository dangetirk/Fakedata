import csv
import subprocess
import json
import requests
from datetime import datetime

# Replace with your Salesforce credentials and object name
username = 'YOUR_SALESFORCE_USERNAME'
object_name = 'YOUR_SALESFORCE_OBJECT_NAME'

# Authenticate with Salesforce using sfdx
auth_info = json.loads(subprocess.check_output(['sfdx', 'org', 'display', '-u', username, '-v', 'json']).decode('utf-8'))
access_token = auth_info['result']['accessToken']
instance_url = auth_info['result']['instanceUrl']

# Query data from the object using the Salesforce API
headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}
query = 'SELECT Id, Name, CreatedDate FROM {}'.format(object_name)
url = instance_url + '/services/data/v51.0/query/?q=' + query
result = json.loads(requests.get(url, headers=headers).text)['records']

# Write data to CSV file
filename = '{}_{}.csv'.format(object_name, datetime.now().strftime('%Y%m%d_%H%M%S'))
with open(filename, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=result[0].keys())
    writer.writeheader()
    for row in result:
        writer.writerow(row)

print('Data written to file:', filename)
