import argparse
import csv
from faker import Faker

# Initialize Faker with the 'en_GB' locale for UK-specific data
fake = Faker('en_GB')

# Define a function to mask the specified columns in a row
def mask_data(row, columns):
    for column in columns:
        if column == 'Name':
            row[column] = fake.name()
        elif column == 'Address1':
            row[column] = fake.building_number() + ' ' + fake.street_name()
        elif column == 'Address2':
            row[column] = fake.secondary_address()
        elif column == 'City':
            row[column] = fake.city()
        elif column == 'Postcode':
            row[column] = fake.postcode()
        elif column == 'FullAddress':
            row[column] = fake.building_number() + ' ' + fake.street_name() + ' ' + fake.secondary_address() + ', ' + fake.city() + ' ' + fake.postcode()
        elif column == 'Comments':
            row[column] = fake.text(max_nb_chars=50)
        else:
            row[column] = fake.text(max_nb_chars=50)            
    return row

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Mask specified columns in a CSV file using fake data')
parser.add_argument('input_file', help='path to the input CSV file')
parser.add_argument('-c', '--columns', nargs='+', help='names of columns to mask')
args = parser.parse_args()

# Open the input and output CSV files
with open(args.input_file, 'r') as input_file, open('output.csv', 'w', newline='') as output_file:
    # Use the Sniffer class to detect the dialect of the input CSV file
    dialect = csv.Sniffer().sniff(input_file.read(1024))
    input_file.seek(0)

    # Create a CSV reader and writer with the detected dialect
    reader = csv.DictReader(input_file, dialect=dialect)
    writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames, dialect=dialect)
    
    # Write a new row with masked data for each row in the input CSV
    writer.writeheader()
    for row in reader:
        masked_row = mask_data(row, args.columns)
        writer.writerow(masked_row)
