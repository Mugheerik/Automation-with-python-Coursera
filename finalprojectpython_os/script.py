#!/usr/bin/env python3

import sys
import re
import csv
from collections import defaultdict

# Define patterns
patterninfo = re.compile(r'ticky: INFO (.*?) \[(?:#[^\]]*)\] \(([^)]+)\)')
patternerror = re.compile(r'ticky: ERROR (.*?) \(([^)]+)\)')

def getErrors_info(logfile):
    # Initialize dictionaries
    error_messages = defaultdict(int)
    user_stats = defaultdict(lambda: {'INFO': 0, 'ERROR': 0})
    
    # Open file using with statement
    with open(logfile, 'r') as file:
        for log in file:
            # Search for INFO patterns
            info_match = patterninfo.search(log)
            if info_match:
                message = info_match.group(1).strip()
                user = info_match.group(2)
                user_stats[user]['INFO'] += 1
                continue  # Skip to the next log line
            
            # Search for ERROR patterns
            error_match = patternerror.search(log)
            if error_match:
                message = error_match.group(1).strip()
                user = error_match.group(2)
                error_messages[message] += 1
                user_stats[user]['ERROR'] += 1


    # Print the results
    print("\nError Messages and Counts:")
    for error_type, count in error_messages.items():
        print(f"{error_type}: {count}")

    print("\nUser INFO and ERROR Counts:")
    for user, counts in user_stats.items():
        print(f"{user}: INFO={counts['INFO']}, ERROR={counts['ERROR']}")

    # Write error_messages to CSV
    with open('error_messages.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Error Message', 'Count'])
        for error_type, count in error_messages.items():
            writer.writerow([error_type, count])

    # Write user_stats to CSV
    with open('user_stats.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User', 'INFO Count', 'ERROR Count'])
        for user, counts in user_stats.items():
            writer.writerow([user, counts['INFO'], counts['ERROR']])

    print("CSV files created: 'error_messages.csv' and 'user_stats.csv'")

# Check if the script is run with a filename argument
if len(sys.argv) != 2:
    print("Usage: python script.py <logfile>")
else:
    getErrors_info(sys.argv[1])
