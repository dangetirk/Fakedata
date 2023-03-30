import csv
from faker import Faker

# Initialize Faker with the 'en_GB' locale for UK-specific data
fake = Faker('en_GB')

# Define a function to mask the address and comments fields
def mask_data(row):
    row['Name'] = fake.name()
    row['Address'] = fake.address()
    row['Comments'] = fake.text(max_nb_chars=50)

    return row

# Open the input and output CSV files
with open('input.csv', 'r') as input_file, open('output.csv', 'w', newline='') as output_file:
    # Use the Sniffer class to detect the dialect of the input CSV file
    dialect = csv.Sniffer().sniff(input_file.read(1024))
    input_file.seek(0)

    # Create a CSV reader and writer with the detected dialect
    reader = csv.DictReader(input_file, dialect=dialect)
    writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames, dialect=dialect)
    
    # Write a new row with masked data for each row in the input CSV
    writer.writeheader()
    for row in reader:
        masked_row = mask_data(row)
        writer.writerow(masked_row)
