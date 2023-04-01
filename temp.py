import csv
import subprocess
import json
import requests
from datetime import datetime
import sys

# Replace with your Salesforce credentials
username = 'YOUR_SALESFORCE_USERNAME'

# Get the object name from the command line arguments
if len(sys.argv) < 2:
    print('Usage: python salesforce_to_csv.py <object_name>')
    sys.exit(1)
object_name = sys.argv[1]

# Authenticate with Salesforce using sfdx
auth_info = json.loads(subprocess.check_output(['sfdx', 'org', 'display', '-u', username, '--json']).decode('utf-8'))
access_token = auth_info['result']['accessToken']
instance_url = auth_info['result']['instanceUrl']

# Query data from the object using the Salesforce API
headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}
query = 'SELECT * FROM {}'.format(object_name)
url = instance_url + '/services/data/v51.0/query/?q=' + query
result = json.loads(requests.get(url, headers=headers).text)['records']

# Write data to CSV file
filename = '{}_{}.csv'.format(object_name, datetime.now().strftime('%Y%m%d_%H%M%S'))
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(result[0].keys())
    for row in result:
        writer.writerow([str(value) for value in row.values()])

print('Data written to file:', filename)
