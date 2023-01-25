# Atlanta-Health-Systems
COVID Results Document Processing


## ahs_extract_results
Parse PDFs and extract name, email, DOB, and COVID-19 test results.
Output Excel spreadsheet with all relevant information.

Instructions for use:
1. Download all results in PDF format from your health portal.
2. Put all relevant results in one folder.
3. Run `ahs_extract_results.py` on the folder.
4. The output is an Excel spreadsheet of all test results.

## ahs_update_spreadsheet
Merge a spreadsheet for each new studio production into a master spreadsheet containing all previous productions.
