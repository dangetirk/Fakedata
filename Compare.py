import pandas as pd
import os
import sys

def compare_csv_files(file1_path, file2_path):
    # Read in the two CSV files
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)

    # Check if the number of columns in both files is the same
    if len(df1.columns) != len(df2.columns):
        print('Number of columns in both files is not the same')
        print(f'File 1 has {len(df1.columns)} columns, while file 2 has {len(df2.columns)} columns')
        #return None, None
        sys.exit(0)

    # Merge the two dataframes and keep only the rows that are different
    merged = pd.merge(df1, df2, on=list(df1.columns), how='outer', indicator=True)
    diff = merged[merged['_merge'] != 'both']

    # Check if there are any differences
    if len(diff) == 0:
        print('Files are identical')
        sys.exit(0)
    else:
        print('Files are different')
        # Get the file names and remove the file extension
        file1_name = os.path.splitext(os.path.basename(file1_path))[0]
        file2_name = os.path.splitext(os.path.basename(file2_path))[0]

        # Add a new column with the input file names
        diff.insert(0, 'Filename', [file1_name if row['_merge'] == 'left_only' else file2_name for index, row in diff.iterrows()])

        # Drop the _merge column
        diff = diff.drop(columns=['_merge'])

        # Sort the rows by the second column before writing to the output file
        diff = diff.sort_values(by=[diff.columns[1]])

        # Write the differences to an Excel file
        diff.to_excel(f'{file1_name}_{file2_name}_diff.xlsx', index=False)
        if os.path.exists(f'{file1_name}_{file2_name}_diff.xlsx'):
            print('Refer the output file for differences')
            #print(f'File differences written to {file1_name}_{file2_name}_diff.xlsx')
        else:
            print('Error: Output file not created')

    # Print record counts for both files
    print(f"{file1_name} has {len(df1.index)} records")
    print(f"{file2_name} has {len(df2.index)} records")
    #sys.exit(1)

    return file1_name, file2_name
    

# Example usage
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python compare_csv_files.py <file1_path> <file2_path>")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]

    file1_name, file2_name = compare_csv_files(file1_path, file2_path)

    if file1_name is not None and file2_name is not None:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(f'{file1_name}_{file2_name}_diff.xlsx', sheet_name='Sheet1')

        # Get the non-repeating column values based on the second column
        non_repeating = df.drop_duplicates(subset=df.columns[1], keep=False)

        # Get the repeating rows based on the second column
        repeating = df[df.duplicated(subset=df.columns[1], keep=False)]

        # Write the non-repeating column values to one sheet and the repeating rows to another sheet in a new
# Get the non-repeating column values based on the second column
non_repeating = df.drop_duplicates(subset=df.columns[1], keep=False)

# Get the repeating rows based on the second column
repeating = df[df.duplicated(subset=df.columns[1], keep=False)]

# Write the non-repeating column values to one sheet and the repeating rows to another sheet in a new Excel file
with pd.ExcelWriter('output_file.xlsx') as writer:
    non_repeating.to_excel(writer, sheet_name='Non-Repeating Column Values', index=False, header=df.columns)
    repeating.to_excel(writer, sheet_name='Repeating Rows', index=False, header=df.columns)

# Delete the file1_file2_diff.xlsx file
    os.remove(f'{file1_name}_{file2_name}_diff.xlsx')

