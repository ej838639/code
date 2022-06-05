"""
Identify the cells that had a significant change in timing advance and find the associated RET
Eric Johnson
Oct 2018
"""
import glob
import pandas as pd
import os
import numpy as np

### Inputs ###
second_carrier = False
change_date = pd.to_datetime('12/19/2018')
site_name = 'West Virginia Oct 8'
ta_filename = 'LSR Distance Indianapolis Oct 8'
ret_filename = 'Indianapolis Labels - Oct 8'
path=r"C:\Users\ejohnso43\Documents\1_2018\SON\Nokia Modules\C-CCO\Deployment\West Virginia"
os.chdir(path)

### Load Files ###
files = glob.glob(path + '\*.xls*')

# Load Formulas
for file_ in files:
    if ta_filename in file_:
        ta = pd.read_excel(file_)

# Load Counter Lookup
for file_ in files:
    if ret_filename in file_:
        ret = pd.read_excel(file_)
        
# Split the dataframe into two dataframes: one normal and one for the change period
# Filter the dataset to only include hours from mighnight to 5am, i.e. hours from the maintenance window (MW)
ta = ta[ta['hour'] < 5]
ta_normal = ta[ta['date'] < change_date]
ta_change = ta[ta['date'] == change_date]

# Find the median and standard deviation for the normal dates per hour during the MW
ta_normal_med = ta_normal.groupby(['cell_name','hour']).median()
ta_normal_sdev = ta_normal.groupby(['cell_name','hour']).std()
ta_change_med = ta_change.groupby(['cell_name','hour']).median()

# Find the median and standard deviation for the normal dates overall during the MW
ta_normal_med_overall = ta_normal.groupby(['cell_name']).median()
ta_normal_sdev_overall = ta_normal.groupby(['cell_name']).std()
ta_change_med_overall = ta_change.groupby(['cell_name']).median()

# Find if the change is significantly different than normal per hour 
ta_diff = ta_normal_med - ta_change_med
ta_diff = ta_diff.abs()
ta_check = ta_diff > 3*ta_normal_sdev # 3 times the standard deviation is a significant change
ta_mult = ta_diff / ta_normal_sdev

# Find if the change is significantly different than normal per hour 
ta_diff_overall = ta_normal_med_overall - ta_change_med_overall
ta_diff_overall = ta_diff_overall.abs()
ta_check_overall = ta_diff_overall > 3*ta_normal_sdev_overall # 3 times the standard deviation is a significant change
ta_mult_overall = (ta_diff_overall / ta_normal_sdev_overall).round(2)
ta_mult_overall = ta_mult_overall.reset_index()
ta_mult_overall = ta_mult_overall.drop(['hour'], axis=1)
ta_mult_overall = ta_mult_overall.rename(index=str, columns={"avg_ta_distance": "Multiple of Std Dev"})

# Count number of significant changes per MW and filter for cells with 4 or 5 hours of significant change
ta_check_sum = ta_check.groupby(['cell_name']).sum()
ta_check_sum = ta_check_sum.rename(index=str, columns={"avg_ta_distance": "Hours Changed"})
ta_check_sum = ta_check_sum.reset_index()
#ta_check_sum = ta_check_sum[ta_check_sum['Hours Changed'] > 3]
#cells_changed = ta_check_sum
#cells_changed = cells_changed.reset_index()

# Convert RET Labels to cell name
ret['site_id'] = ret['Label'].str[:8]
ret_sector = ret['Label'].str[9:10]
sector_dict = {"A":"1", "B":"2", "C":"3", "D":"4", "E":"5", "F":"6"}
ret_sector.replace(sector_dict, inplace=True, regex=True)


ret['Label Length'] = ret['Label'].str.len()
ret['cell_name_1'] = np.nan
ret['cell_name_2'] = np.nan
ret['cell_name_3'] = np.nan
ret['cell_name_4'] = np.nan

ret['cell_name_1'][ret['Label Length'] == 13] = ret['Label'].str[-1:] + ret['site_id'] + ret_sector + '1'

ret['cell_name_1'][ret['Label Length'] == 14] = ret['Label'].str[-2:-1] + ret['site_id'] + ret_sector + '1'
ret['cell_name_2'][ret['Label Length'] == 14] = ret['Label'].str[-1:] + ret['site_id'] + ret_sector + '1'

ret['cell_name_1'][ret['Label Length'] == 15] = ret['Label'].str[-3:-2] + ret['site_id'] + ret_sector + '1'
ret['cell_name_2'][ret['Label Length'] == 15] = ret['Label'].str[-2:-1] + ret['site_id'] + ret_sector + '1'
ret['cell_name_3'][ret['Label Length'] == 15] = ret['Label'].str[-1:] + ret['site_id'] + ret_sector + '1'

ret['cell_name_1'][ret['Label Length'] == 16] = ret['Label'].str[-4:-3] + ret['site_id'] + ret_sector + '1'
ret['cell_name_2'][ret['Label Length'] == 16] = ret['Label'].str[-3:-2] + ret['site_id'] + ret_sector + '1'
ret['cell_name_3'][ret['Label Length'] == 16] = ret['Label'].str[-2:-1] + ret['site_id'] + ret_sector + '1'
ret['cell_name_4'][ret['Label Length'] == 16] = ret['Label'].str[-1:] + ret['site_id'] + ret_sector + '1'

if second_carrier == True:
    ret['cell_name_5'] = np.nan
    ret['cell_name_5'][(ret['Label Length'] == 13) & (ret['Label'].str[-1:] == 'L')] = ret['Label'].str[-1:] + ret['site_id'] + ret_sector + '2'
    ret['cell_name_5'][(ret['Label Length'] == 14) & (ret['Label'].str[-2:-1] == 'L')] = ret['Label'].str[-2:-1] + ret['site_id'] + ret_sector + '2'
    ret['cell_name_5'][(ret['Label Length'] == 14) & (ret['Label'].str[-1:] == 'L')] = ret['Label'].str[-1:] + ret['site_id'] + ret_sector + '2'
    ret['cell_name_5'][(ret['Label Length'] == 15) & (ret['Label'].str[-3:-2] == 'L')] = ret['Label'].str[-3:-2] + ret['site_id'] + ret_sector + '2'
    ret['cell_name_5'][(ret['Label Length'] == 15) & (ret['Label'].str[-2:-1] == 'L')] = ret['Label'].str[-2:-1] + ret['site_id'] + ret_sector + '2'
    ret['cell_name_5'][(ret['Label Length'] == 15) & (ret['Label'].str[-1:] == 'L')] = ret['Label'].str[-1:] + ret['site_id'] + ret_sector + '2'
    ret['cell_name_5'][(ret['Label Length'] == 16) & (ret['Label'].str[-4:-3] == 'L')] = ret['Label'].str[-4:-3] + ret['site_id'] + ret_sector + '2'
    ret['cell_name_5'][(ret['Label Length'] == 16) & (ret['Label'].str[-3:-2] == 'L')] = ret['Label'].str[-3:-2] + ret['site_id'] + ret_sector + '2'
    ret['cell_name_5'][(ret['Label Length'] == 16) & (ret['Label'].str[-2:-1] == 'L')] = ret['Label'].str[-2:-1] + ret['site_id'] + ret_sector + '2'
    ret['cell_name_5'][(ret['Label Length'] == 16) & (ret['Label'].str[-1:] == 'L')] = ret['Label'].str[-1:] + ret['site_id'] + ret_sector + '2'


# reorder columns
if second_carrier == True:
    ret = ret[['site_id','Label','Tilt Pre','Tilt Post','Tilt Change','Label Length','cell_name_1','cell_name_2','cell_name_3','cell_name_4','cell_name_5']]
else:
    ret = ret[['site_id','Label','Tilt Pre','Tilt Post','Tilt Change','Label Length','cell_name_1','cell_name_2','cell_name_3','cell_name_4']]
    
# Create dataframe with the list of cells from the ret dataframe
cells = pd.DataFrame()
cells2 = pd.DataFrame()
cells3 = pd.DataFrame()
cells4 = pd.DataFrame()
cells5 = pd.DataFrame()

cells[['site_id','cell_name','Label','Tilt Pre','Tilt Post','Tilt Change']] = ret[['site_id','cell_name_1','Label','Tilt Pre','Tilt Post','Tilt Change']]

cells2[['site_id','cell_name','Label','Tilt Pre','Tilt Post','Tilt Change']] = ret.dropna(subset=['cell_name_2'])[['site_id','cell_name_2','Label','Tilt Pre','Tilt Post','Tilt Change']]
cells = cells.append(cells2)

cells3[['site_id','cell_name','Label','Tilt Pre','Tilt Post','Tilt Change']] = ret.dropna(subset=['cell_name_3'])[['site_id','cell_name_3','Label','Tilt Pre','Tilt Post','Tilt Change']]
cells = cells.append(cells3)

cells4[['site_id','cell_name','Label','Tilt Pre','Tilt Post','Tilt Change']] = ret.dropna(subset=['cell_name_4'])[['site_id','cell_name_4','Label','Tilt Pre','Tilt Post','Tilt Change']]
cells = cells.append(cells4)

if second_carrier == True:
    cells5[['site_id','cell_name','Label','Tilt Pre','Tilt Post','Tilt Change']] = ret.dropna(subset=['cell_name_5'])[['site_id','cell_name_5','Label','Tilt Pre','Tilt Post','Tilt Change']]
    cells = cells.append(cells5)

# Unique cells derived from RET Labels
cells_unique = cells.groupby(['cell_name']).count()
cells_unique = cells_unique.reset_index()
cells_unique['cell_name'] = cells_unique['cell_name']
cells_unique['site_id'] = cells_unique['cell_name'].str[1:9]

# Find only LTE cells
cells_unique['Band'] = cells_unique['cell_name'].str[:1]
cells_unique = cells_unique[(cells_unique['Band'] == 'L') | (cells_unique['Band'] == 'B')| (cells_unique['Band'] == 'D') | (cells_unique['Band'] == 'E') | (cells_unique['Band'] == 'F')]
cells_unique = cells_unique[['site_id','cell_name','Band']]

site = cells_unique.groupby(['site_id']).count()
site = site.reset_index()
site = site[['site_id','cell_name']]
site = site.rename(index=str, columns={"cell_name": "Cells Changed per Site"})

# Create dataframe for all cells with data collected
cells_on_site = ta_mult_overall
cells_on_site['site_id'] = cells_on_site['cell_name'].str[1:9]

# Add column for multiple of standard deviation
cells_on_site = cells_on_site.merge(ta_check_sum, on=['cell_name'], how='left')
cells_on_site['Matches RET Label'] = cells_on_site['cell_name'].isin(cells['cell_name'])
cells_on_site = cells_on_site[['site_id','cell_name','Multiple of Std Dev','Hours Changed']] # Do not include mathces RET Label
cells_on_site = cells_on_site.sort_values(['site_id','Multiple of Std Dev'], ascending=[True,False])
cells_on_site['Matches RET Label'] = cells_on_site['cell_name'].isin(cells['cell_name'])
cells_on_site = cells_on_site.merge(site, on=['site_id'], how='left')
cells_on_site['rank'] = cells_on_site.groupby(['site_id']).rank(method='dense', ascending=False)['Multiple of Std Dev']
cells_on_site['Top Changes'] = cells_on_site['rank'] <= cells_on_site['Cells Changed per Site']
cells_on_site['Multiple of Std Dev > 2'] = cells_on_site['Multiple of Std Dev'] > 2
cells_on_site['Top & > 2'] = cells_on_site['Top Changes'] & cells_on_site['Multiple of Std Dev > 2']
cells_on_site = cells_on_site[['site_id','cell_name','Matches RET Label','Top & > 2','Multiple of Std Dev','Hours Changed','Multiple of Std Dev > 2','Top Changes','rank','Cells Changed per Site']]

# Check for matches in changed cells
cells_changed = pd.DataFrame()
cells_changed['cell_name'] = cells_on_site[cells_on_site['Top & > 2'] == True]['cell_name']
cells_changed['Matches RET Label'] = cells_changed['cell_name'].isin(cells['cell_name'])
cells['Matches Changed Cell'] = cells['cell_name'].isin(cells_changed['cell_name'])
cells = cells.sort_values(['site_id','Label','cell_name'], ascending=[True,True,True])

# Summarize results
summary = pd.Series(name = 'Count')
summary_per = pd.Series(name = 'Percentage')
summary['LTE Cells Changed'] = cells_unique['cell_name'].count()
summary_per['LTE Cells Changed'] = ''
summary['Detected Matches Changes'] = cells_on_site[(cells_on_site['Top & > 2'] == True) & (cells_on_site['Matches RET Label'] == True)]['cell_name'].count()
summary_per['Detected Matches Changes'] = (100*summary['Detected Matches Changes'] / summary['LTE Cells Changed'] ).round(0)
summary['Changes Not Detected'] = cells_on_site[(cells_on_site['Top & > 2'] == False) & (cells_on_site['Matches RET Label'] == True)]['cell_name'].count()
summary_per['Changes Not Detected'] = (100*summary['Changes Not Detected'] / summary['LTE Cells Changed']).round(0)
summary['Cells on Sites'] = cells_on_site.count()['cell_name']
summary_per['Cells on Sites'] = ''
summary['False Positives'] = cells_on_site[(cells_on_site['Top & > 2'] == True) & (cells_on_site['Matches RET Label'] == False)]['cell_name'].count()
summary_per['False Positives'] = (100*summary['False Positives'] / summary['Cells on Sites']).round(0)

# Convert series to dataframe and add percentages
summary_df = summary.to_frame()
summary_df.loc[:,'Percentage'] = summary_per
summary_df = summary_df.fillna(value=0)

# export to excel
#ta_check.to_excel(site_name + ' Hourly Check.xlsx')

with pd.ExcelWriter(site_name + ' Results.xlsx') as writer:
    summary_df.to_excel(writer, sheet_name='Summary')
    cells_on_site.to_excel(writer, sheet_name='Cells on Site', index = False)
    cells_changed.to_excel(writer, sheet_name='Cells Changed', index = False)
    ret.to_excel(writer, sheet_name='RET Labels', index = False)
    cells.to_excel(writer, sheet_name='Cells from RET', index = False)
    cells_unique.to_excel(writer, sheet_name='Unique LTE Cells from RET', index = False)

