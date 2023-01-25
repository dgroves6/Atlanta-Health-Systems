#!/usr/bin/env python3
import os
import csv
from pdfminer.high_level import extract_text
import time

start_time = time.time()
#results_foldername = 'ahs_jan_7'#''.join('ahs_'+datetime.date.today().strftime("%b-%d-%Y").lower().replace('-','_')[0:6])

def extract_pdf(filename):
    """Take in a PDF covid result, return a dict of relevant information."""
    text = extract_text(filename).split('\n')
    new_text = [item for item in text if len(item) < 75 and len(item)]
    info_dict = {}
    for i,v in enumerate(new_text):
        if v == 'Accession #:':
            info_dict['Accession #'] = new_text[i+1]
        if v == 'Phone:':
            info_dict['First Name'] = new_text[i+1].split(',')[1].strip().replace(' Ref Physician:', '')
            info_dict['Last Name'] = new_text[i+1].split(',')[0].strip()
            if not isphone(new_text[i+2]) and new_text[i+2] not in ('DOB (Age) / Sex:','Ref Physician:'):
                info_dict['First Name'] = ' '.join([info_dict['First Name'], new_text[i+2]]).strip()
        if v.startswith('DOB'):
            info_dict['DOB'] = new_text[i+1].split()[0]
        if 'Result:' in v:
            info_dict['Result'] = v.split('Result:', 1)[1].strip()
    return info_dict
    
def extract_covid_results(results_foldername):
    """Take in foldername containing PDF results, output Excel sheet with detailed results for everyone."""
    path = r'C:\Users\dangr\Downloads'
    path = os.path.join(path, results_foldername)
    os.chdir(path)
    info_array = []
    for i, file in enumerate(os.listdir()):
        if file.endswith('.pdf'):
            info_array.append(extract_pdf(file))
            print(f'File {i} Completed')
    fields = ['Accession #', 'First Name', 'Last Name', 'DOB', 'Result']
    filename = os.path.basename(path) + '.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writeheader()
        writer.writerows(info_array)

def main():
    extract_covid_results('ahs_11_3')
    
    
if __name__ == '__main__':
    main()
    