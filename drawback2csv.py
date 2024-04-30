import re

def parse_document(input_file, output_file):
    # Initialize variables
    entries = []

    # Read the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Process lines to extract entries
    current_name = ""
    current_description = []
    for line in lines:
        # Check if line is a new entry
        if line.strip() == "" or line.startswith("Your record:") or line.strip() == "EasyHard":
            # End of the current entry, save it
            if current_name and current_description:
                entries.append((current_name, " ".join(current_description)))
                current_name = ""
                current_description = []
        elif re.match("^[A-Za-z ]+$", line.strip()) and current_name == "":
            current_name = line.strip()
        else:
            # Part of the current entry's description
            current_description.append(line.strip())

    # Write to output file
    with open(output_file, 'w') as file:
        file.write("Name,Description\n")
        for name, description in entries:
            file.write(f'"{name}","{description}"\n')

# Call the function with your file paths
parse_document('drawbacks.txt', 'drawbacks.csv')
