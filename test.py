import os
import glob
import csv

current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths to the folders containing CSV files
folders = ['Algeria', 'Morocco', 'Tunisia']

# Dictionary to store CSV files for each country
csv_files = {}

# Loop through each folder
for folder in folders:
    # Construct the path to the current folder
    folder_path = os.path.join(current_dir, '..', 'data', folder)
    # Get a list of CSV files in the folder
    csv_files[folder] = glob.glob(os.path.join(folder_path, '*.csv'))

# Function to read CSV file
def read_csv_file(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)  # Do whatever processing you need here

# Iterate over CSV files and read their contents
for folder, files in csv_files.items():
    print(f"Files in {folder} folder:")
    for file_path in files:
        read_csv_file(file_path)
