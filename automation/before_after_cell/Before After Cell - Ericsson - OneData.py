"""
Before and after analysis
Determine if there is a significant change in KPIs related to a network change (Ex: Downtilt)
Compare weekdays between after weekdays and previous same weekdays
(Ex: Compare Monday to the previous 3 Mondays)
Significant increase if lower quartile after is above the upper quartile from before
Significant decrease if upper quartile after is below the lower quartile from before
Eric Johnson
Jan 2017
"""
import glob
import pandas as pd
import os


### Inputs ###
change_date = pd.to_datetime('4/19/2018')
cell = 'LA_CCO_Test2'
coverage_category = 'Offender'
results_filename = 'Coverage - ' + cell
category_filename = 'Coverage KPIs Ericsson v1'
path=r"C:\Users\ejohnso43\Documents\1_2018\SON\Nokia Modules\C-CCO\Los Angeles"
os.chdir(path)

### Determine if there is a significant increase or decrease ###

# Load the KPI results
files = glob.glob(path + '\*.xls*')

for file_ in files:
    if results_filename in file_:
        df = pd.read_excel(file_, parse_dates = ['Period start time'], index_col = 'Period start time')

# Add the day of the week to the dataframe
df['weekday'] = df.index.weekday

# Split the dataframe into two dataframes: one before and one after the change
df_after = df[df.index >= change_date]
df_before = df[df.index < change_date]

# Lower/upper quartile before
df_before_lower = df_before.groupby('weekday').quantile(q = 0.25)
df_before_upper = df_before.groupby('weekday').quantile(q = 0.75)

# Lower/upper quartile after
df_after_lower = df_after.groupby('weekday').quantile(q = 0.25)
df_after_upper = df_after.groupby('weekday').quantile(q = 0.75)

# Boolean: True if lower quartile after is above the upper quartile from before (boolean)
df_after_incr = df_after_lower > df_before_upper
# Boolean: True if  if upper quartile after is below the lower quartile from before (boolean)
df_after_decr = df_after_upper < df_before_lower

# Add up the number of days of significant increase/decrease (this creates a series from the dataframe)
s_after_incr_sum = df_after_incr.sum()
s_after_decr_sum = df_after_decr.sum()

# Update Index Names
s_after_incr_sum.index.names = ['KPI']
s_after_decr_sum.index.names = ['KPI']

### Assess every KPI to indicate if an increase is good or a decrease is good ###

# Import file to categorize every KPI to indicate if an increase is good or a decrease is good
for file_ in files:
    if category_filename in file_:
        improvement_type = pd.read_excel(file_, index_col = 'KPI')

# Significant increase/decrease if 5 or more weekday-to-weedays have a change
s_after_incr_category = s_after_incr_sum >= 5 # Boolean: True if increase is 5 or more
s_after_decr_category = s_after_decr_sum >= 5 # Boolean: True if decrease is 5 or more

s_after_incr_category = s_after_incr_category.replace([True, False], ['Increase','No change'])
s_after_decr_category = s_after_decr_category.replace([True, False], ['Decrease', None])
s_after_incr_category.update(s_after_decr_category)

df_after_category = pd.DataFrame(s_after_incr_category, columns = ['Change'])
df_after_category['Improvement Type'] = improvement_type['Improvement Type']
df_after_temp = df_after_category.copy()
# df_after_temp = pd.DataFrame(s_after_incr_category, columns = ['Change'])
# df_after_temp['Improvement Type'] = improvement_type['Improvement Type']

# Boolean for when Change/Improvement is Increase/Decrease. 
df_after_temp['Change Incr'] = df_after_temp['Change'] == 'Increase'
df_after_temp['Change Decr'] = df_after_temp['Change'] == 'Decrease'
df_after_temp['Improvment Incr'] = df_after_temp['Improvement Type'] == 'Increase'
df_after_temp['Improvment Decr'] = df_after_temp['Improvement Type'] == 'Decrease'

# Avoid "True" in Boolean comparison when both Change and Improvement Type are False
df_after_temp['Improvment Incr'] = df_after_temp['Improvment Incr'].replace([False], [None]) 
df_after_temp['Improvment Decr'] = df_after_temp['Improvment Decr'].replace([False], [None])

# Boolean for when Improved/Degraded
df_after_temp['Improved A'] = df_after_temp['Change Incr'] == df_after_temp['Improvment Incr']
df_after_temp['Improved A'] = df_after_temp['Improved A'].replace([True, False], ['Improved', 'No change'])
df_after_temp['Improved B'] = df_after_temp['Change Decr'] == df_after_temp['Improvment Decr']
df_after_temp['Improved B'] = df_after_temp['Improved B'].replace([True, False], ['Improved', None])
df_after_temp['Degraded A'] = df_after_temp['Change Incr'] == df_after_temp['Improvment Decr']
df_after_temp['Degraded A'] = df_after_temp['Degraded A'].replace([True, False], ['Degraded', 'No change'])
df_after_temp['Degraded B'] = df_after_temp['Change Decr'] == df_after_temp['Improvment Incr']
df_after_temp['Degraded B'] = df_after_temp['Degraded B'].replace([True, False], ['Degraded', None])

# Combine into one column for Assessment
df_after_temp['Improved A'].update(df_after_temp['Improved B'])
df_after_temp['Degraded A'].update(df_after_temp['Degraded B'])
df_after_temp['Degraded A'] = df_after_temp['Degraded A'].replace(['No change'], [None])
df_after_category['Assessment'] = df_after_temp['Improved A'].copy()
df_after_category['Assessment'].update(df_after_temp['Degraded A'])

df_after_category['Cell'] = cell
df_after_category['Change Date'] = change_date
df_after_category['Coverage Category'] = coverage_category

### Analytics on results ###

# Calcualte the medians and basis points (bps) change
s_after_med = df_after.median()
s_before_med = df_before.median()

# No need for "Weekday" columns
s_after_med = s_after_med.drop('weekday')
s_before_med = s_before_med.drop('weekday')

# Basis Points change
s_bps_change = (s_after_med - s_before_med)*100

# Convert zeros to NaN to avoid divide by zero
s_before_med = s_before_med.replace([0], [None])

# Percentage (%) change
s_percent_change = (s_after_med - s_before_med)/s_before_med

# Add analytics to dataframe
df_after_category['Days of Significant Increase'] = s_after_incr_sum
df_after_category['Days of Significant Decrease'] = s_after_decr_sum
df_after_category['Before Median'] = s_before_med
df_after_category['After Median'] = s_after_med
df_after_category['% Change'] = s_percent_change
df_after_category['bps change'] = s_bps_change
df_after_category['KPI Category'] = improvement_type['KPI Category']

# Reorder dataframe columns and format date
df_after_category = df_after_category[['Cell', 'Change Date', 'Coverage Category', 'Change', 'Improvement Type', 'Assessment', 'KPI Category', 'Days of Significant Increase', 'Days of Significant Decrease', 'Before Median', 'After Median', '% Change', 'bps change']]
df_after_category['Change Date'] = df_after_category['Change Date'].dt.strftime('%m/%d/%Y')

# Export results to Excel
df_after_category.to_excel('Results - ' + cell + '.xlsx')