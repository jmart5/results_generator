import os
import pandas as pd
import re

def parse_names(directory):
    names = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_name, _ = os.path.splitext(file)
            parts = re.split(r'_', file_name)
            if len(parts) >= 2:
                part1 = parts[0]
                part2 = parts[1] 
                names.append([part1, part2])
    return names


def extract_contents(directory_path):
    file_text_content = [] 
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r') as file:
            text = file.read()
            file_text_content.append(text) 
    return file_text_content


def parse_results(strings_list):
    result_list = [] 
    for text in strings_list:
        match = re.search(r'Result: (\d+/100)', text)
        if match:
            result = match.group(1)
            mod_result = format_results(result)
            result_list.append(mod_result)
        else:
            result_list.append("No result found")
    return result_list

def format_results(input_string):
    try:
        number_str = input_string.split("/100")[0]
        number = int(number_str)
        return number
    except (ValueError, IndexError):
        return None


def parse_feedback(strings_list):
    extracted_list = []
    for text in strings_list:
        matches = re.findall(r'={15,}(.*?)={15,}', text, re.DOTALL)
        extracted_list.extend(matches)
    return extracted_list

# Request the directory path
directory_path = input("Please enter the results folder path: ")

# Parse required fields from files
file_info = parse_names(directory_path)
file_contents = extract_contents(directory_path)
results_info = parse_results(file_contents)
comments_info = parse_feedback(file_contents)

# Store results in a dataframe 
df = pd.DataFrame(file_info, columns=["Part1", "Part2"])
df['Grade']=results_info
df['Comments']=comments_info

# Create CSV
csv_file_path = "resutls_summary.csv"
df.to_csv(csv_file_path, index=False)