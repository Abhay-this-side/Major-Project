import csv

# File name of the CSV containing interview questions
csv_filename = 'interview_questions.csv'

def count_rows(file_name):
    try:
        with open(file_name, mode='r', encoding='utf-8') as file:
            # Count each row, then subtract 1 to exclude the header
            row_count = sum(1 for row in file) - 1
        print(f"Total number of questions saved: {row_count}")
    except FileNotFoundError:
        print(f"File '{file_name}' not found. Please make sure the file exists.")

# Call the function
count_rows(csv_filename)
