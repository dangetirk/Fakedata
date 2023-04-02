from dbcomparer import DbComparer
from simple_salesforce import Salesforce
from google.cloud import bigquery

# Connect to Salesforce
sf = Salesforce(username='<your_username>', password='<your_password>', security_token='<your_security_token>')

# Connect to BigQuery
client = bigquery.Client()

# Retrieve data from Salesforce
sf_query = 'SELECT Id, Name, Email FROM Contact'
sf_data = sf.query(sf_query)['records']

# Retrieve data from BigQuery
bq_query = 'SELECT id, name, email FROM mydataset.contacts'
bq_data = client.query(bq_query).to_dataframe()

# Compare the data
comparer = DbComparer()
result = comparer.compare(sf_data, bq_data)

# Print the result
print(result)
