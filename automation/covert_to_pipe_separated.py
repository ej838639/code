"""
Convert Excel to Pipe Separated Values
Eric Johnson
Dec 2021
"""

import glob
import os
import pandas as pd
from datetime import datetime

path = r'C:\Users\ejohnso43\Documents\1_2021\Docs Training Tools\Python\Convert to Pipe Separated'
os.chdir(path)

# datetime object containing current date and time
current_date_time = datetime.now()
current_date_time_str = current_date_time.strftime("%Y%m%d%H%M")

# Load File #
files = glob.glob(path + '\*.xlsx')
ericsson_file = 'Ericsson Reference Tables'
nokia_file = 'Reference Tables Nokia LTE'
for file_ in files:
    if ericsson_file in file_:
        field_alert_ericsson = pd.read_excel(file_, sheet_name='FieldAlertTracker')
        # Keep only necessary columns
        field_alert_ericsson = field_alert_ericsson[['Track in Dashboard', 'Description', 'MO_Class', 'Parameter_Name', 'Parameter_MO', 'Field_Alert_Date','Category', 'Vendor', 'Tech']]
        # Export
        field_alert_ericsson.to_csv('Ericsson_LTE_Field_Alert_Tracker_' + current_date_time_str + '.csv', index=False, sep='|')

        ericsson_flag = True
    if nokia_file in file_:
        field_alert_nokia = pd.read_excel(file_, sheet_name='FieldAlertTracker')
        # Keep only necessary columns
        field_alert_nokia = field_alert_nokia[['Description', 'MO_Class', 'Parameter_Name', 'Field_Alert_Date', 'Category', 'Vendor', 'Tech']]
        # Export
        field_alert_nokia.to_csv('Nokia_LTE_Field_Alert_Tracker_' + current_date_time_str + '.csv', index=False, sep='|')

print('Done')