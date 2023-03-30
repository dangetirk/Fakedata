from faker import Faker
fake = Faker()

# Define the schema for the table
schema = {
    "id": "integer",
    "name": "string",
    "age": "integer",
    "email": "string",
    "address": "string"
}

# Create 10 insert statements with fake data based on the schema
table_name = "users"
columns = ", ".join(schema.keys())
insert_statements = []
for i in range(10):
    record = {}
    for field, datatype in schema.items():
        if datatype == "integer":
            record[field] = fake.random_int()
        elif datatype == "string":
            record[field] = fake.text(max_nb_chars=50).replace("'", "''")
    values = ", ".join([f"'{value}'" if isinstance(value, str) else str(value) for value in record.values()])
    insert_statement = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    insert_statements.append(insert_statement)

# Print the insert statements
for statement in insert_statements:
    print(statement)
