#!/usr/bin/env python3
import re
import pandas as pd
import numpy as np
import datetime
        
def isphone(item):
    # Phone isnumeric() or has format XXX-XXX-XXXX or other formats
    return type(item) == int or (isinstance(item,str) and re.sub("[-. +()]", "", item).isnumeric())
    
def isemail(item):
    return isinstance(item,str) and '@' in item
    
def isdob(item):
    return isinstance(item, datetime.datetime)
    
def isname(item):
    return isinstance(item,str) and not isemail(item) and not isphone(item) and re.sub("[' .-]", "", item).isalpha()
    # 376 names = 16 apostrophes + 90 hyphens + 240 spaces + 30 periods
    
def reformat_actor_info(filename):
    """Take Excel sheet with actor info in one column and return df with specific columns."""
    # First and Last Names are always present
    # Email contains '@' and maybe ellipses
    raw_data = iter(np.concatenate([prod.values for _, prod in pd.read_excel(filename).iteritems()]))
    info_dict = {'First Name':[], 'Last Name':[], 'Email Address':[], 'Date of Birth':[]}
    row = ['']*4
    actor_list = []
    for item in raw_data:
        if any(row) and isname(item):
            actor_list.append(row)
            row = ['']*4
        if isname(item):
            row[0] = item.strip()
            row[1] = str(next(raw_data)).strip()
        elif isemail(item):
            row[2] = item.split(chr(8230))[-1].strip() # 8230 is unicode for ellipses
        elif isdob(item):
            row[3] = str(item.date())
        elif isphone(item) or pd.isnull(item):
            continue
        else:
            print(f'Fix this item in {filename}: {item}.')
    return pd.DataFrame(data=actor_list, columns = info_dict.keys()) # Has 4664 people
    
def remove_background(df):
    """Remove any background actors from the Excel sheet."""
    pass
    
def remove_duplicates(master_df):
    """Remove any duplicate names from the master Excel sheet."""
    counts = master_df.value_counts(dropna=False).values
    master_df = master_df.drop_duplicates() # Reduced size of master list from 5426 to 3927
    master_df['Counts'] = counts
    master_df = master_df.sort_values(by=['Last Name', 'First Name'])
    print(master_df)
    master_df.to_excel('film_studios_master_list.xlsx', index=False)
    
def analyze_master_list(df):
    df = df.sort_values(by=['Last Name', 'First Name'])
    duplicates = df[df.duplicated(subset=['First Name', 'Last Name'], keep=False)]
    print(duplicates.head(30))
    
def count_accessions(sheet):
    data = pd.read_csv(sheet).iloc[:, 0].values
    curr_nums = [int(num.split('-')[1]) for num in data]
    nec_nums = [i for i in range(20261, 20448)]
    miss_nums = [i for i in nec_nums if i not in curr_nums]
    print(miss_nums)
    print(len(miss_nums))

def main():
    master_list = pd.read_excel('film_studios_master_list.xlsx')
    analyze_master_list(master_list)    
    
if __name__ == '__main__':
    main()
    