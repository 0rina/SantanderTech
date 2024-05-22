import os
import re
import json

"""
A function for analysing logs from the GC - Garbage Collector.
The function takes a log format file and extracts data, line by line, about the size of the
eden, survivors and heap memory spaces and writes them to a file in JSON format.

Function arguments:
file_name - the file to process.

Function output:
List of dictionaries containing the processed data.
"""
def parse_gc_log(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    data = []

    for line in lines:
        match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}\+\d{4})', line)

        #check if match for timestamp was found
        if match:
            timestamp = match.group(1)

        gc_name_match = re.search(r'(GC pause \(\w+ \w+ Pause\))', line)

        # check if match for gc_name was found
        if gc_name_match:
            gc_name = gc_name_match.group(1)

        #find line starts with Eden
        if line.startswith("   [Eden:"):
            match = re.search(r"Eden: (\d+\.\d+)M\(\d+\.\d+M\)->(\d+\.\d+)B", line)
            eden_size_before_gc_MB = float(match.group(1)) if match else None
            eden_size_after_gc_MB = float(match.group(2)) if match else None

            match = re.search(r"Survivors: (\d+\.\d+)K->(\d+\.\d+)K", line)
            surviors_size_before_gc_MB = float(match.group(1))/1024 if match else None
            surviors_size_after_gc_MB = float(match.group(2))/1024 if match else None

            match = re.search(r"Heap: (\d+\.\d+)M\(\d+\.\d+M\)->(\d+\.\d+)M", line)
            heap_size_before_gc_MB = float(match.group(1)) if match else None
            heap_size_after_gc_MB = float(match.group(2)) if match else None

            #writing data for faze before
            data.append({
                "timestamp": timestamp,
                "eden_size": eden_size_before_gc_MB,
                "survivors_size": surviors_size_before_gc_MB,
                "heap_size": heap_size_before_gc_MB,
                "GC_name": gc_name,
                "phase": "before",
            })

            #writing data for faze after
            data.append({
                "timestamp": timestamp,
                "eden_size": eden_size_after_gc_MB,
                "survivors_size": surviors_size_after_gc_MB,
                "heap_size": heap_size_after_gc_MB,
                "GC_name": gc_name,
                "phase": "after",
            })

    return data

"""
The function takes the data that is given as the first argument 
and writes this data to a file in JSON format, which is given as the second argument.
The arguments of the function:
data - processed data.
output_file - the input file into which the data is written.
"""

def write_data(data, output_file):
    with open(output_file, 'w') as json_file: #if the file does not exist, a new one is created
        for d in data:
            json.dump(d, json_file)
            json_file.write('\n')

"""
The function checks if the format of the input and output file is correct and if the input file exists, 
if it does,it parses the data from the log file and writes it to json.
"""

def parse():
    print("Write name of input file:")
    input_file = input()

    #check that file exists
    check_file = os.path.isfile(input_file)
    #file extension
    _, ext = os.path.splitext(input_file)

    # check is log file
    if ext.lower() != ".log":
        raise ValueError("It is not log file")

    if (check_file and (ext.lower() == ".log")):
        print("Write name of output file:")
        output_file = input()
        #file extension
        _, ext = os.path.splitext(output_file)
        # parsed data
        data = parse_gc_log(input_file)

        #check is json file
        if ext.lower() == ".json":
            # write parsed data to json
            write_data(data, output_file)
            print("The parsed data were entered into a file.")
        else:
            raise ValueError("It is not json file")

    else:
        raise FileNotFoundError("Input file doesnt exist. ")

if __name__ == '__main__':
    parse()

