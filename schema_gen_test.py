import csv
import yaml

source_file = 'table.csv'
output_file = 'dbt_tests.yml'

models = []
with open(source_file, mode='r') as f_in:
    reader = csv.DictReader(f_in)
    for row in reader:
        model_name = row['table_name']
        column_name = row['column_name']
        datatype = row['datatype']
        size = row['size']
        column = {'name': column_name, 'tests': []}
        if datatype == 'integer':
            column['tests'].append('schema_check_integer')
        elif datatype == 'string':
            column['tests'].append({'test_length': {'max_length': int(size)}})
        elif datatype == 'date':
            column['tests'].append('schema_check_date')
        elif datatype == 'boolean':
            column['tests'].append('schema_check_boolean')
        model = next((m for m in models if m['name'] == model_name), None)
        if model is None:
            model = {'name': model_name, 'columns': []}
            models.append(model)
        model['columns'].append(column)

with open(output_file, mode='w') as f_out:
    yaml_out = yaml.dump({'models': models}, sort_keys=False)
    f_out.write(yaml_out)
