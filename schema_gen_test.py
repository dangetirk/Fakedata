import csv
import yaml

source_file = 'table.csv'
output_file = 'dbt_tests.yml'

# Define a dictionary to hold the models and their columns
models = {}

# Read in the CSV file and create the models and columns
with open(source_file, mode='r') as f_in:
    reader = csv.DictReader(f_in)
    for row in reader:
        model_name = row['table_name']
        column_name = row['column_name']
        datatype = row['datatype']
        size = row['size']
        if model_name not in models:
            models[model_name] = {'name': model_name, 'columns': []}
        model_columns = models[model_name]['columns']
        column = next((c for c in model_columns if c['name'] == column_name), None)
        if column is None:
            column = {'name': column_name, 'tests': []}
            model_columns.append(column)
        if datatype == 'integer':
            column['tests'].append('schema_check_integer')
        elif datatype == 'string':
            column['tests'].append({'test_length': {'max_length': int(size)}})
        elif datatype == 'date':
            column['tests'].append('schema_check_date')
        elif datatype == 'boolean':
            column['tests'].append('schema_check_boolean')

# Write out the YAML file with the tests
with open(output_file, mode='w') as f_out:
    yaml_out = yaml.dump(list(models.values()), sort_keys=False)
    f_out.write(yaml_out)
