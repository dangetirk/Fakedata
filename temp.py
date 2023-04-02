import csv
import subprocess
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
try:
    auth_info = subprocess.check_output(['sfdx', 'force:org:display', '-u', username, '--json']).decode('utf-8')
    auth_info = json.loads(auth_info.strip())
    access_token = auth_info['result']['accessToken']
    instance_url = auth_info['result']['instanceUrl']
except Exception as e:
    print('Error authenticating with Salesforce:', e)
    sys.exit(1)

# Describe the object using the Salesforce API
try:
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    url = instance_url + '/services/data/v51.0/sobjects/{}/describe'.format(object_name)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    result = json.loads(response.text)['fields']
except Exception as e:
    print('Error querying Salesforce:', e)
    sys.exit(1)

# Write data to CSV file
try:
    filename = '{}_{}.csv'.format(object_name, datetime.now().strftime('%Y%m%d_%H%M%S'))
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([field['name'] for field in result])
        
    print('Data written to file:', filename)
except Exception as e:
    print('Error writing data to CSV file:', e)
    sys.exit(1)
