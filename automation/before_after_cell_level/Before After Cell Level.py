"""
Before and after analysis for every cell in a cluster (adapted from bin-level)
Data is in per geo-bin per day format, so need to calculate before and after for every geo-bin instead of only the cluster
Determine if there is a significant change in KPIs related to a network change (Ex: Downtilt)
Compare weekdays between after weekdays and previous same weekdays
(Ex: Compare Monday to the previous 3 Mondays)
Significant increase if lower quartile after is above the upper quartile from before
Significant decrease if upper quartile after is below the lower quartile from before
Eric Johnson
May 2018
"""
import glob
import pandas as pd
import os


### Inputs ###
change_date = pd.to_datetime('5/17/2018')
cell = 'L18 Primary Check`'
days_of_change = 7
results_filename = 'Market TAC Primary'
category_filename = 'KPIs Primary TAC'
path=r"C:\Users\ejohnso43\Documents\1_2018\Nokia\L18\FOA\Drop 9 KPIs"
os.chdir(path)

### Load and prepare the KPI results ###
files = glob.glob(path + '\*.xls*')

for file_ in files:
    if results_filename in file_:
        df = pd.read_excel(file_)

df['Period start time'] = pd.to_datetime(df['Period start time'])
        
# Import file to categorize every KPI to indicate if an increase is good or a decrease is good
for file_ in files:
    if category_filename in file_:
        improvement_type = pd.read_excel(file_, index_col = 'KPI')

# Add the day of the week to the dataframe
df = df.assign(weekday = df['Period start time'].dt.weekday)

# Ensure all the data columns are numeric instead of object
#cols = df.columns.drop({'Period start time', 'REGION', 'MARKET', 'TAC', 'SITE', 'ENODEB', 'CELL', 'weekday'})
cols = df.columns.drop({'Period start time', 'REGION', 'MARKET', 'TAC', 'weekday'})
#cols = df.columns.drop({'Period start time', 'REGION', 'AREA', 'CELL', 'weekday'})
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

# Export data to Excel
#df.to_csv('Results - ' + cell + '.csv', index = False)

# No need for TAC
df = df.drop(['TAC'], axis=1)

# Only analyze Thursday (weekday 3)
#df = df[df['weekday'] == 3]

# Split the dataframe into two dataframes: one before and one after the change
df_before_bin = df[df['Period start time'] < change_date]
df_after_bin = df[df['Period start time'] >= change_date]

# Drop cells that are in after, but missing from before
df_before_cells = df_before_bin.groupby(['CELL','weekday']).median()
df_after_cells = df_after_bin.groupby(['CELL','weekday']).median()
cells_to_drop = df_after_cells.index.difference(df_before_cells.index)
df_after_cells = df_after_cells.drop(cells_to_drop)

# Aggregate per bins and date (since there are multiple 56m bins per day in the file)
#df_before_bin = df_before_bin.groupby(['CELL','Period start time','weekday']).sum()
#df_after_bin = df_after_bin.groupby(['CELL','Period start time','weekday']).sum()
#df_after_bin = df_after_bin.drop(cells_to_drop)

### Bin-level (i.e. cell-level) and weekday (wd): Determine if there is a significant increase or decrease ###

# Median after/after
df_before_bin_wd_med = df_before_bin.groupby(['CELL']).median()
df_after_bin_wd_med = df_after_bin.groupby(['CELL']).median()

# Drops cells that are missing between before and after
cells_to_drop2a = df_before_bin_wd_med.index.difference(df_after_bin_wd_med.index)
cells_to_drop2b = df_after_bin_wd_med.index.difference(df_before_bin_wd_med.index)
df_before_bin_wd_med = df_before_bin_wd_med.drop(cells_to_drop2a)
df_after_bin_wd_med = df_after_bin_wd_med.drop(cells_to_drop2b)

# Percentage (%) change
df_bin_percent_change = (df_after_bin_wd_med - df_before_bin_wd_med)/df_before_bin_wd_med

# Lower/upper quartile before
df_before_bin_wd_lower = df_before_bin.groupby(['CELL','weekday']).quantile(q = 0.25)
df_before_bin_wd_upper = df_before_bin.groupby(['CELL','weekday']).quantile(q = 0.75)

# Lower/upper quartile after
df_after_bin_wd_lower = df_after_bin.groupby(['CELL','weekday']).quantile(q = 0.25)
df_after_bin_wd_upper = df_after_bin.groupby(['CELL','weekday']).quantile(q = 0.75)

# Drops cells that are missing between before and after
cells_to_drop3a = df_after_bin_wd_lower.index.difference(df_before_bin_wd_upper.index)
cells_to_drop3b = df_before_bin_wd_upper.index.difference(df_after_bin_wd_lower.index)
cells_to_drop4a = df_after_bin_wd_upper.index.difference(df_before_bin_wd_lower.index)
cells_to_drop4b = df_before_bin_wd_lower.index.difference(df_after_bin_wd_upper.index)

df_after_bin_wd_lower = df_after_bin_wd_lower.drop(cells_to_drop3a)
df_before_bin_wd_upper = df_before_bin_wd_upper.drop(cells_to_drop3b)
df_after_bin_wd_upper = df_after_bin_wd_upper.drop(cells_to_drop4a)
df_before_bin_wd_lower = df_before_bin_wd_lower.drop(cells_to_drop4b)

# Significant increase if lower quartile after is above the upper quartile from before (boolean)
df_after_bin_wd_incr = df_after_bin_wd_lower > df_before_bin_wd_upper
# Significant decrease if upper quartile after is below the lower quartile from before (boolean)
df_after_bin_wd_decr = df_after_bin_wd_upper < df_before_bin_wd_lower

# Add up the number of days of significant increase/decrease (this creates a series from the dataframe)
df_after_incr_bin_wd_sum = df_after_bin_wd_incr.groupby('CELL').sum()
df_after_decr_bin_wd_sum = df_after_bin_wd_decr.groupby('CELL').sum()

# For all bin-level calculations, add up the number of days of significant increase/decrease
s_after_incr_bin_wd_sum_all = df_after_incr_bin_wd_sum.sum()
s_after_decr_bin_wd_sum_all = df_after_decr_bin_wd_sum.sum()

# Update Index Names
df_after_incr_bin_wd_sum.index.names = ['KPI']
df_after_decr_bin_wd_sum.index.names = ['KPI']
s_after_incr_bin_wd_sum_all.index.names = ['KPI']
s_after_decr_bin_wd_sum_all.index.names = ['KPI']

# Significant increase/decrease if 5 or more weekday-to-weedays have a change
df_after_incr_bin_wd_category = df_after_incr_bin_wd_sum >= days_of_change # Boolean: True if increase is every day
df_after_decr_bin_wd_category = df_after_decr_bin_wd_sum >= days_of_change # Boolean: True if increase is every day

df_after_incr_bin_wd_cnt = df_after_incr_bin_wd_category.sum()
df_after_decr_bin_wd_cnt = df_after_decr_bin_wd_category.sum()

# Create a dataframe with the improvement type duplicated in all the rows (i.e. bins) of the KPI
df_improvement_type = df_after_incr_bin_wd_category.copy()
df_improvement_type_kpi = list(df_improvement_type)
kpis = range(len(df_improvement_type.columns))
for kpi in kpis:
    df_improvement_type[df_improvement_type_kpi[kpi]] = df_improvement_type[df_improvement_type_kpi[kpi]].replace([True, False], improvement_type['Improvement Type'][df_improvement_type_kpi[kpi]])

# Boolean for when Improvement is Increase/Decrease
df_improvement_type_incr = df_improvement_type == 'Increase'
df_improvement_type_decr = df_improvement_type == 'Decrease'

# Avoid "True" in Boolean comparison when both Change and Improvement Type are False
df_improvement_type_incr = df_improvement_type_incr.replace([False], [None])
df_improvement_type_decr = df_improvement_type_decr.replace([False], [None]) 

# Boolean for when Improved/Degraded
df_impr_a = df_after_incr_bin_wd_category == df_improvement_type_incr
df_impr_a = df_impr_a.replace([True, False], ['Improved', 'No change'])
df_impr_b = df_after_decr_bin_wd_category == df_improvement_type_decr
df_impr_b = df_impr_b.replace([True, False], ['Improved', None])
df_degr_a = df_after_incr_bin_wd_category == df_improvement_type_decr
df_degr_a = df_degr_a.replace([True, False], ['Degraded', 'No change'])
df_degr_b = df_after_decr_bin_wd_category == df_improvement_type_incr
df_degr_b = df_degr_b.replace([True, False], ['Degraded', None])

# Combine into one table for Assessment
df_impr_a.update(df_impr_b) # Combine both improvement dataframes
df_degr_a.update(df_degr_b) # Combine both degraded dataframes
df_degr_a = df_degr_a.replace(['No change'], [None])
df_assessment_bin = df_impr_a.copy() 
df_assessment_bin.index = df_assessment_bin.index.rename('CELL')
df_assessment_bin.update(df_degr_a) # Combine the improvement and degraded dataframes

# Count/Percentage improved/degraded bins
df_impr_bool = df_impr_a == 'Improved' # Boolean of improved bins
df_degr_bool = df_degr_a == 'Degraded' # Boolean of degraded bins
df_impr_cnt = df_impr_bool.sum()
df_degr_cnt = df_degr_bool.sum()

# Sort ascending by KPI
df_impr_cnt = df_impr_cnt.groupby('KPI').sum()
df_degr_cnt = df_degr_cnt.groupby('KPI').sum()

bin_cnt = len(df_assessment_bin.index)
df_impr_per = df_impr_cnt/bin_cnt
df_degr_per = df_degr_cnt/bin_cnt

df_assessment_bin.to_csv('Assessment Cell - ' + cell + '.csv')
df_bin_percent_change.to_csv('Per Change Overall - ' + cell + '.csv')
df_impr_cnt.to_csv('Improvement Count Overall - ' + cell + '.csv')
df_degr_cnt.to_csv('Degraded Count Overall - ' + cell + '.csv')
df_impr_per.to_csv('Improvement Per Overall - ' + cell + '.csv')
df_degr_per.to_csv('Degraded Per Overall - ' + cell + '.csv')

