import csv

def convert_levels_to_int(input_file_path: str, output_file_path: str):
    # Define the mapping from level strings to integer values
    level_mapping = {
        'Some knowledge': 1,
        'Knowledgable': 2,
        'Experienced': 3,
        'Highly experienced': 4,
        'Expert': 5
    }

    # Open the input CSV file and the output CSV file
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
        # Create a CSV DictReader for the input file
        reader = csv.DictReader(input_file)

        # Create a CSV DictWriter for the output file using the field names from the DictReader
        writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)

        # Write the header to the output file
        writer.writeheader()

        # Iterate over each row in the input file
        for row in reader:
            # Convert the 'Level' field to an integer value using the mapping
            row['Level'] = level_mapping.get(row['Level'], None)

            # Write the converted row to the output file
            writer.writerow(row)

def main():
    input_file_path = 'data/competencies.csv'
    output_file_path = 'data/competencies_converted.csv'
    convert_levels_to_int(input_file_path, output_file_path)

if __name__ == "__main__":
    main()