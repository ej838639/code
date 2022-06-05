"""
Before and after analysis for every 56min geo-bin
Data is in per geo-bin per day format, so need to calculate before and after for every geo-bin instead of only the cluster
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
change_date = pd.to_datetime('12/7/2017')
cell = 'L1NC3603A21'
coverage_category = 'Offender'
results_filename = 'Freqbin bins Top95 L1NC3603A21 Nov 16 to Dec 21 no thx'
category_filename = 'Coverage KPIs GeoBin'
path=r"C:\Users\ejohnso43\Documents\1_2017\Tools\Python\Before After Geo Bin"
os.chdir(path)

### Load and prepare the KPI results ###
files = glob.glob(path + '\*.xls*')

for file_ in files:
    if results_filename in file_:
        df = pd.read_excel(file_, parse_dates = ['DATE_PART'])
        
# Import file to categorize every KPI to indicate if an increase is good or a decrease is good
for file_ in files:
    if category_filename in file_:
        improvement_type = pd.read_excel(file_, index_col = 'KPI')

# Create table to store the lat/Long per Hex so we can use it later
hex_lat_long = df[['HEX56_ID','HEX56_CENTER_LAT','HEX56_CENTER_LON']].groupby('HEX56_ID').first()

# No need for Lat/Long columns
df = df.drop('HEX56_CENTER_LAT', axis = 'columns')
df = df.drop('HEX56_CENTER_LON', axis = 'columns')

# Add the day of the week to the dataframe
df = df.assign(weekday = df['DATE_PART'].dt.weekday)

# Add columns for eRAB/VoLTE DCR (and avoid error from divide by zero)
df = df.assign(ERAB_ATTEMPTS = df['ERAB_ATTEMPTS'].replace([0], [None]))
df = df.assign(ERAB_DCR = df['ERAB_DROPS']/df['ERAB_ATTEMPTS'])
df = df.assign(VOLTE_ERAB_ATTEMPTS = df['VOLTE_ERAB_ATTEMPTS'].replace([0], [None]))
df = df.assign(VOLTE_DCR = df['VOLTE_ERAB_DROPS']/df['VOLTE_ERAB_ATTEMPTS'])

# Add before/after columns for % SINR < 2, % RSRP < -114 dBm, % RSRP > -114 dBm and SINR >=2 (and avoid divide per zero)
df = df.assign(CNT_PUSCH_SINR = df['CNT_PUSCH_SINR'].replace([0], [None]))
df = df.assign(PER_PUSCH_SINR_2 = df['CNT_PUSCH_SINR_2']/df['CNT_PUSCH_SINR'])
df = df.assign(SUM_RSRP_140_44 = df['SUM_RSRP_140_44'].replace([0], [None]))
df = df.assign(PER_RSRP_140_114 = df['SUM_RSRP_140_114']/df['SUM_RSRP_140_44'])
df = df.assign(CNT_RSRP_PUSCH_SINR = df['CNT_RSRP_PUSCH_SINR'].replace([0], [None]))
df = df.assign(PER_RSRP_PUSCH_SINR_GT114_GT2 = df['CNT_RSRP_PUSCH_SINR_GT114_GT2']/df['CNT_RSRP_PUSCH_SINR'])

# Ensure all the data columns are numeric instead of object
cols = df.columns.drop({'DATE_PART', 'MARKET_NAME', 'CELL_NAME', 'HEX56_ID', 'weekday'})
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

# Export data to Excel
df.to_csv('Results Bin Daily - ' + cell + '.csv', index = False)

# Split the dataframe into two dataframes: one before and one after the change
df_before_bin = df[df['DATE_PART'] < change_date]
df_after_bin = df[df['DATE_PART'] >= change_date]

# Aggregate per bins and date (since there are multiple 56m bins per day in the file)
df_before_bin = df_before_bin.groupby(['HEX56_ID','DATE_PART','weekday']).sum()
df_after_bin = df_after_bin.groupby(['HEX56_ID','DATE_PART','weekday']).sum()

# Re-calculate percentages
df_before_bin['ERAB_DCR'] = df_before_bin['ERAB_DROPS']/df_before_bin['ERAB_ATTEMPTS']
df_before_bin['VOLTE_DCR'] = df_before_bin['VOLTE_ERAB_DROPS']/df_before_bin['VOLTE_ERAB_ATTEMPTS']
df_before_bin['PER_PUSCH_SINR_2'] = df_before_bin['CNT_PUSCH_SINR_2']/df_before_bin['CNT_PUSCH_SINR']
df_before_bin['PER_RSRP_140_114'] = df_before_bin['SUM_RSRP_140_114']/df_before_bin['SUM_RSRP_140_44']
df_before_bin['PER_RSRP_PUSCH_SINR_GT114_GT2'] = df_before_bin['CNT_RSRP_PUSCH_SINR_GT114_GT2']/df_before_bin['CNT_RSRP_PUSCH_SINR']

df_after_bin['ERAB_DCR'] = df_after_bin['ERAB_DROPS']/df_after_bin['ERAB_ATTEMPTS']
df_after_bin['VOLTE_DCR'] = df_after_bin['VOLTE_ERAB_DROPS']/df_after_bin['VOLTE_ERAB_ATTEMPTS']
df_after_bin['PER_PUSCH_SINR_2'] = df_after_bin['CNT_PUSCH_SINR_2']/df_after_bin['CNT_PUSCH_SINR']
df_after_bin['PER_RSRP_140_114'] = df_after_bin['SUM_RSRP_140_114']/df_after_bin['SUM_RSRP_140_44']
df_after_bin['PER_RSRP_PUSCH_SINR_GT114_GT2'] = df_after_bin['CNT_RSRP_PUSCH_SINR_GT114_GT2']/df_after_bin['CNT_RSRP_PUSCH_SINR']

### Bin-level and weekday (wd): Determine if there is a significant increase or decrease ###

# Median after/after
df_before_bin_wd_med = df_before_bin.groupby(['HEX56_ID','weekday']).median()
df_after_bin_wd_med = df_after_bin.groupby(['HEX56_ID','weekday']).median()

# Lower/upper quartile before
df_before_bin_wd_lower = df_before_bin.groupby(['HEX56_ID','weekday']).quantile(q = 0.25)
df_before_bin_wd_upper = df_before_bin.groupby(['HEX56_ID','weekday']).quantile(q = 0.75)

# Lower/upper quartile after
df_after_bin_wd_lower = df_after_bin.groupby(['HEX56_ID','weekday']).quantile(q = 0.25)
df_after_bin_wd_upper = df_after_bin.groupby(['HEX56_ID','weekday']).quantile(q = 0.75)

# Significant increase if lower quartile after is above the upper quartile from before (boolean)
df_after_bin_wd_incr = df_after_bin_wd_lower > df_before_bin_wd_upper
# Significant decrease if upper quartile after is below the lower quartile from before (boolean)
df_after_bin_wd_decr = df_after_bin_wd_upper < df_before_bin_wd_lower

# Add up the number of days of significant increase/decrease (this creates a series from the dataframe)
df_after_incr_bin_wd_sum = df_after_bin_wd_incr.groupby('HEX56_ID').sum()
df_after_decr_bin_wd_sum = df_after_bin_wd_decr.groupby('HEX56_ID').sum()

# For all bin-level calculations, add up the number of days of significant increase/decrease
s_after_incr_bin_wd_sum_all = df_after_incr_bin_wd_sum.sum()
s_after_decr_bin_wd_sum_all = df_after_decr_bin_wd_sum.sum()

# Update Index Names
df_after_incr_bin_wd_sum.index.names = ['KPI']
df_after_decr_bin_wd_sum.index.names = ['KPI']
s_after_incr_bin_wd_sum_all.index.names = ['KPI']
s_after_decr_bin_wd_sum_all.index.names = ['KPI']

# Significant increase/decrease if 5 or more weekday-to-weedays have a change
df_after_incr_bin_wd_category = df_after_incr_bin_wd_sum >= 5 # Boolean: True if increase is 5 or more
df_after_decr_bin_wd_category = df_after_decr_bin_wd_sum >= 5 # Boolean: True if increase is 5 or more

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
df_assessment_bin.index = df_assessment_bin.index.rename('HEX56_ID')
df_assessment_bin.update(df_degr_a) # Combine the improvement and degraded dataframes

# Add lat/longs and order them to the front
df_assessment_bin = pd.concat([df_assessment_bin, hex_lat_long], axis = 1)
cols = df_assessment_bin.columns.tolist()
cols = cols[-2:] + cols[:-2]
df_assessment_bin = df_assessment_bin[cols]
df_assessment_bin.to_csv('Results Bin - ' + cell + '.csv')

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

### Per Weekday (wd): Determine if there is a significant increase or decrease ###

# Sum all the bins per day and weekday
df_before_daily = df_before_bin.groupby('DATE_PART').sum()
df_after_daily = df_after_bin.groupby('DATE_PART').sum()

# Re-calculate percentages
df_before_daily['ERAB_DCR'] = df_before_daily['ERAB_DROPS']/df_before_daily['ERAB_ATTEMPTS']
df_before_daily['VOLTE_DCR'] = df_before_daily['VOLTE_ERAB_DROPS']/df_before_daily['VOLTE_ERAB_ATTEMPTS']
df_before_daily['PER_PUSCH_SINR_2'] = df_before_daily['CNT_PUSCH_SINR_2']/df_before_daily['CNT_PUSCH_SINR']
df_before_daily['PER_RSRP_140_114'] = df_before_daily['SUM_RSRP_140_114']/df_before_daily['SUM_RSRP_140_44']
df_before_daily['PER_RSRP_PUSCH_SINR_GT114_GT2'] = df_before_daily['CNT_RSRP_PUSCH_SINR_GT114_GT2']/df_before_daily['CNT_RSRP_PUSCH_SINR']

df_after_daily['ERAB_DCR'] = df_after_daily['ERAB_DROPS']/df_after_daily['ERAB_ATTEMPTS']
df_after_daily['VOLTE_DCR'] = df_after_daily['VOLTE_ERAB_DROPS']/df_after_daily['VOLTE_ERAB_ATTEMPTS']
df_after_daily['PER_PUSCH_SINR_2'] = df_after_daily['CNT_PUSCH_SINR_2']/df_after_daily['CNT_PUSCH_SINR']
df_after_daily['PER_RSRP_140_114'] = df_after_daily['SUM_RSRP_140_114']/df_after_daily['SUM_RSRP_140_44']
df_after_daily['PER_RSRP_PUSCH_SINR_GT114_GT2'] = df_after_daily['CNT_RSRP_PUSCH_SINR_GT114_GT2']/df_after_daily['CNT_RSRP_PUSCH_SINR']

# Add back weekday
df_before_daily['weekday'] = df_before_daily.index.weekday
df_after_daily['weekday'] = df_after_daily.index.weekday

# Median before/after Bin-level
df_before_wd_med = df_before_daily.groupby('weekday').median()
df_after_wd_med = df_after_daily.groupby('weekday').median()

# Lower/upper quartile before
df_before_wd_lower = df_before_daily.groupby('weekday').quantile(q = 0.25)
df_before_wd_upper = df_before_daily.groupby('weekday').quantile(q = 0.75)

# Lower/upper quartile after
df_after_wd_lower = df_after_daily.groupby('weekday').quantile(q = 0.25)
df_after_wd_upper = df_after_daily.groupby('weekday').quantile(q = 0.75)

# Significant increase if lower quartile after is above the upper quartile from before (boolean)
df_after_wd_incr = df_after_wd_lower > df_before_wd_upper
# Significant decrease if upper quartile after is below the lower quartile from before (boolean)
df_after_wd_decr = df_after_wd_upper < df_before_wd_lower

# Add up the number of days of significant increase/decrease (this creates a series from the dataframe)
s_after_incr_wd_sum = df_after_wd_incr.sum()
s_after_decr_wd_sum = df_after_wd_decr.sum()

# Update Index Names
s_after_incr_wd_sum.index.names = ['KPI']
s_after_decr_wd_sum.index.names = ['KPI']

# Significant increase/decrease if 5 or more weekday-to-weedays have a change
s_after_incr_wd_category = s_after_incr_wd_sum >= 5 # Boolean: True if increase is 5 or more
s_after_decr_wd_category = s_after_decr_wd_sum >= 5 # Boolean: True if increase is 5 or more

s_after_incr_wd_cnt = s_after_incr_wd_category.sum()
s_after_decr_wd_cnt = s_after_decr_wd_category.sum()

# Change incr from True/False to be Increase/No-change
s_after_incr_wd_category = s_after_incr_wd_category.replace([True, False], ['Increase','No change'])

# Change decr from True/False to be Increase/[blank] (blank instead of 'No change' so can merge)
s_after_decr_wd_category = s_after_decr_wd_category.replace([True, False], ['Decrease', None])

# Merge incr and decr
s_after_incr_wd_category.update(s_after_decr_wd_category)

df_after_category = pd.DataFrame(s_after_incr_wd_category, columns = ['Change'])
df_after_category['Improvement Type'] = improvement_type['Improvement Type']
df_after_temp = df_after_category.copy()

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
s_after_overall_med = df_after_daily.median()
s_before_overall_med = df_before_daily.median()

# No need for "Weekday" 
s_after_overall_med = s_after_overall_med.drop('weekday')
s_before_overall_med = s_before_overall_med.drop('weekday')

s_overall_bps_change = (s_after_overall_med - s_before_overall_med)*100

# Convert zeros to NaN to avoid divide by zero
s_before_overall_med = s_before_overall_med.replace([0], [None])

# Percentage (%) change
s_overall_percent_change = (s_after_overall_med - s_before_overall_med)/s_before_overall_med

# Add analytics to dataframe
df_after_category['Days of Significant Increase'] = s_after_incr_wd_sum
df_after_category['Days of Significant Decrease'] = s_after_decr_wd_sum
df_after_category['Before Median'] = s_before_overall_med
df_after_category['After Median'] = s_after_overall_med
df_after_category['% Change'] = s_overall_percent_change
df_after_category['bps change'] = s_overall_bps_change
df_after_category['KPI Category'] = improvement_type['KPI Category']
df_after_category['% Area Improved'] = df_impr_per
df_after_category['% Area Degraded'] = df_degr_per

# Reorder dataframe columns and format date
df_after_category = df_after_category[['Cell', 'Change Date', 'Coverage Category', 'Change', 'Improvement Type', 'Assessment', 'KPI Category', 'Days of Significant Increase', 'Days of Significant Decrease', 'Before Median', 'After Median', '% Change', 'bps change', '% Area Improved', '% Area Degraded']]
df_after_category['Change Date'] = df_after_category['Change Date'].dt.strftime('%m/%d/%Y')

# Export results to Excel
df_after_category.to_csv('Results Overall - ' + cell + '.csv')