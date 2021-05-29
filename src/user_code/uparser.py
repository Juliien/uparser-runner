import json
import csv
import os


def run(source_pathname, destination_pathname):

    with open(source_pathname) as json_file:
        employee_data = json.load(json_file)

    # now we will open a file for writing
    data_file = open(destination_pathname, 'w')

    # create the csv writer object
    csv_writer = csv.writer(data_file)

    # Counter variable used for writing
    # headers to the CSV file
    count = 0

    for emp in employee_data:
        if count == 0:
            # Writing headers of CSV file
            header = emp.keys()
            csv_writer.writerow(header)
            count += 1

        # Writing data of CSV file
        csv_writer.writerow(emp.values())

    print("lmao parsing")
    data_file.close()
