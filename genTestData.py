import math
import os
from datetime import datetime, timedelta
from random import random, uniform
from typing import List
files_to_generate: int = 100
"""Total number of files to generate"""
file_error_percentage: float = 0.1
"""Percentage of files that should have errors (default is 10%)"""
individual_error_percentage: float = 0.25
"""Percentage that each error should appear in a file with errors (default is 25%)"""
number_of_entries: List[int] = [50, 100]
"""The range for the number of entries in a file (randomly selected in range)"""
from_date: datetime = datetime.now() - timedelta(days=60)
"""Date to start generating files from (default is 60 days ago)"""
to_date: datetime = datetime.now()
"""Date to generate files up to (default is now)"""

def generate_line(with_errors: bool, timestamp: datetime, force_error: bool = False, avoid_batch_ids=None):
    """Generate an individual line for the output file"""
    line = []
    line_has_errors = False
    # Compute the batch ID that this line should have. We'll just randomly generate one that hasn't already been used.
    if avoid_batch_ids is None:
        avoid_batch_ids = []
    batch_id = math.floor(10 * number_of_entries[1] * random())
    while batch_id in avoid_batch_ids and not with_errors:
        batch_id = math.floor(10 * number_of_entries[1] * random())
    if batch_id in avoid_batch_ids:
        line_has_errors = True
    line.append(str(batch_id))
    # Now add the timestamp for the line.
    line.append(timestamp.strftime('"%H:%M:%S"'))
    # Finally, generate the results.
    for i in range(0, 10):
        # If, as a fallback, we have to force an error, generate an invalid field.
        if i == 9 and force_error and not line_has_errors:
            line.append(format(10, '.3f'))
            line_has_errors = True
            break
        # Otherwise generate values.
        lower_boundary_error = with_errors and random() < individual_error_percentage
        upper_boundary_error = with_errors and random() < individual_error_percentage
        line.append(format(round(uniform(
            # Minimum is 0 if not error, otherwise -15.0.
            0 if lower_boundary_error else -15.0,
            # Maximum is 9.9 if not error, otherwise 15.0.
            # Assuming 9.9 rather than 9.999 due to document.
            9.9 if upper_boundary_error else 15.0
        ), 3), '.2f' if with_errors and random() < individual_error_percentage else '.3f'))
        if lower_boundary_error or upper_boundary_error:
            line_has_errors = True
    return line, line_has_errors

def generate_file(current_timestamp: datetime, with_errors: bool):
    """Generate an output file for the specified timestamp, this delegates to generate_line for individual lines"""
    # Determine how many lines to generate.
    line_count = int(number_of_entries[0] + (random() * (number_of_entries[1] - number_of_entries[0])))
    # Generate the header row
    if with_errors:
        header = [
            'batch' if random() < individual_error_percentage else 'batch_id',
            'timestamp',
            'reading1',
            'reading2',
            'reading3',
            'reading4',
            'reading5',
            'reading6',
            'reading7',
            'reading8',
            'reading9',
            'reading10'
        ]
    else:
        header = ['batch_id', 'timestamp', 'reading1', 'reading2', 'reading3', 'reading4', 'reading5', 'reading6',
                  'reading7', 'reading8', 'reading9', 'reading10']
    # Generate the required number of lines.
    data = []
    generated_batch_ids = []
    had_error = False
    for i in range(0, line_count):
        line, error = generate_line(
            with_errors=with_errors and (random() < individual_error_percentage),
            timestamp=current_timestamp,
            avoid_batch_ids=generated_batch_ids
        )
        if error:
            # Indicate that a line with an error has been generated.
            had_error = True
        else:
            # If we're on the last line and haven't had an error yet, force an error.
            if i > line_count - 1 and not had_error:
                line, error = generate_line(
                    with_errors=True,
                    timestamp=current_timestamp,
                    force_error=True,
                    avoid_batch_ids=generated_batch_ids
                )
        # Save the batch ID that was generated for that line, so it isn't generated again.
        generated_batch_ids.append(line[0])
        # Then append the line to the file.
        data.append(line)
    timestamp = current_timestamp.strftime('%Y%m%d%H%M%S')
    new_timestamp = current_timestamp + ((to_date - current_timestamp) / files_to_generate)
    return f'MED_DATA_{timestamp}.csv', header, data, new_timestamp

def main():
    current_timestamp: datetime = from_date
    """Current timestamp to generate (starts at from_date and increments towards to_date)"""
    files_with_errors: List[str] = []
    """The list of files that contained errors when generated"""
    if not os.path.isdir('./output'):
        os.mkdir('./output')
    else:
        print('The output directory (./output) already exists. Please delete it and re-run this script.')
        exit(1)
    if not os.path.isdir('./output/csv'):
        os.mkdir('./output/csv')
    # Generate the specified number of files.
    print('Please wait...')
    for i in range(0, files_to_generate):
        # Generate the file
        include_errors = random() < file_error_percentage
        filename, header, data, new_timestamp = generate_file(current_timestamp, with_errors=include_errors)
        # Add the file to the list of files with errors if it included an error.
        if include_errors:
            files_with_errors.append(filename)
        # Now write the data to a file.
        with open(f'./output/csv/{filename}', 'w') as target_csv:
            # Write the header row
            target_csv.write(",".join(header))
            target_csv.write('\n')
            # Write the data
            for line in data:
                target_csv.write(",".join(line))
                target_csv.write('\n')
            # target_csv_writer.writerows(data)
        current_timestamp = new_timestamp
    # Now write the invalid_files.txt
    with open('./output/invalid_files.txt', 'w') as invalid_files_summary:
        for file_with_errors in files_with_errors:
            invalid_files_summary.write(file_with_errors)
            invalid_files_summary.write('\n')
    print(f'Generated {files_to_generate} CSV file(s) in ./output/csv')
    print(f'\t-> There is/are {len(files_with_errors)} file(s) containing errors.')
    print(f'\t-> Refer to ./output/invalid_files.txt for a list of files containing errors (useful for unit testing)')

if __name__ == '__main__':
    main()