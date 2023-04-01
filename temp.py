from simple_salesforce import Salesforce

# Connect to Salesforce using the authorization information
sf = Salesforce(instance_url='https://your_instance.salesforce.com', session_id='your_session_id')

# Run a SOQL query to get data from a table
query = "SELECT Id, Name, Email FROM Contact"
contacts = sf.query(query)

# Do something with the query results...
