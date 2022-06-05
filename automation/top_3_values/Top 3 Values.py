"""
Create the Top 3 highest values from the distribution of values PCE export
Eric Johnson
Dec 2021
"""

import glob
import pandas as pd
import os
import numpy as np
from datetime import datetime

path = r'C:\Users\ejohnso43\Documents\1_2021\Audit Enforce\Data Integrity\Discrepancy Analyze'
os.chdir(path)

# datetime object containing current date and time
current_date_time = datetime.now()
current_date_time_str = current_date_time.strftime("%Y-%m-%d %H%M")

### Load Files ###
files = glob.glob(path + '\*.csv')
distr_values_file = 'Distribution of Values - Dec 1'
for file_ in files:
    if distr_values_file in file_:
        distr_values = pd.read_csv(file_)

# Group parameters nationally from market data and recalculate the sum and % of total
distr_values_group = distr_values.groupby(['vendor','tech','Abbreviated_Name','MO_Class','Value_Read_from_OSS']).agg({'Value_Usage_Count': ['sum']})
distr_values_group_per = distr_values_group.groupby(['vendor','tech','Abbreviated_Name','MO_Class']).apply(lambda x: x / float(x.sum()))
distr_values_group.columns = ['Value Count']
distr_values_group_per.columns = ['Value % of Total']
distr_values_group = distr_values_group.join(distr_values_group_per)
distr_values_group = distr_values_group.reset_index()
distr_values_group.rename(columns={'vendor': 'Vendor', 'tech': 'Tech', 'Abbreviated_Name': 'Abbreviated Name', 'MO_Class': 'MO Class', 'Value_Read_from_OSS': 'Value', 'Value_Usage_Count': 'Value Count'}, inplace=True)

# Sort to have the most common parameter values first, and rank them
distr_values_group = distr_values_group.sort_values(by=['Vendor','Tech','Abbreviated Name','MO Class','Value Count'], ascending=[True,True,True,True,False])
distr_values_group['Rank'] = distr_values_group.groupby(['Vendor','Tech','Abbreviated Name','MO Class']).cumcount()+1

# Transform the data to have the Top 3 most common values as columns instead of rows

# Create a new dataframe with the highest rank value
top3 = distr_values_group[distr_values_group['Rank']==1]
top3 = top3.drop(top3.columns[-1], axis=1)
top3.rename(columns={'Value': 'Primary Value', 'Value Count': 'Primary Value Count', 'Value % of Total': 'Primary Value % of Total'}, inplace=True)
top3_index = top3['Vendor'] + '_' + top3['Tech'] + '_' + top3['Abbreviated Name'] + '_' + top3['MO Class']
top3 = top3.set_index(top3_index)

# Put the second highest rank data as additional columns
top3_2nd = distr_values_group[distr_values_group['Rank']==2]
top3_2nd = top3_2nd.drop(top3_2nd.columns[-1], axis=1)
top3_2nd.rename(columns={'Value': 'Secondary Value', 'Value Count': 'Secondary Value Count', 'Value % of Total': 'Secondary Value % of Total'}, inplace=True)
top3_2nd_index = top3_2nd['Vendor'] + '_' + top3_2nd['Tech'] + '_' + top3_2nd['Abbreviated Name'] + '_' + top3_2nd['MO Class']
top3_2nd = top3_2nd.set_index(top3_2nd_index)
top3_2nd = top3_2nd.drop(top3_2nd.columns[:4], axis=1)

# Put the third highest rank data as additional columns
top3_3rd = distr_values_group[distr_values_group['Rank']==3]
top3_3rd = top3_3rd.drop(top3_3rd.columns[-1], axis=1)
top3_3rd.rename(columns={'Value': 'Tertiary Value', 'Value Count': 'Tertiary Value Count', 'Value % of Total': 'Tertiary Value % of Total'}, inplace=True)
top3_3rd_index = top3_3rd['Vendor'] + '_' + top3_3rd['Tech'] + '_' + top3_3rd['Abbreviated Name'] + '_' + top3_3rd['MO Class']
top3_3rd = top3_3rd.set_index(top3_3rd_index)
top3_3rd = top3_3rd.drop(top3_3rd.columns[:4], axis=1)

# Add Secondary and Tertiary to the Primary dataframe
top3 = pd.concat([top3, top3_2nd, top3_3rd], axis = 'columns')

# Export
with pd.ExcelWriter('PCE Top 3 Values - Oct 9 - ' + current_date_time_str + '.xlsx') as writer:
    top3.to_excel(writer, sheet_name='Main', index = True)

print('Done')