### Bin-level and weekday (wd): Determine if there is a significant increase or decrease ###

# Median before/after
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
df_assessment_bin.to_excel('Results Bin - ' + cell + '.xlsx')

# Count improved/degraded bins
df_impr_bool = df_impr_a == 'Improved' # Boolean of improved bins
df_degr_bool = df_degr_a == 'Degraded' # Boolean of degraded bins
df_impr_cnt = df_impr_bool.sum()
df_degr_cnt = df_degr_bool.sum()
