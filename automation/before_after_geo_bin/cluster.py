### Per Weekday (wd): Determine if there is a significant increase or decrease ###

# Median before/after Bin-level
df_before_wd_med = df_before_bin.groupby('weekday').median()
df_after_wd_med = df_after_bin.groupby('weekday').median()

# Lower/upper quartile before
df_before_wd_lower = df_before_bin.groupby('weekday').quantile(q = 0.25)
df_before_wd_upper = df_before_bin.groupby('weekday').quantile(q = 0.75)

# Lower/upper quartile after
df_after_wd_lower = df_after_bin.groupby('weekday').quantile(q = 0.25)
df_after_wd_upper = df_after_bin.groupby('weekday').quantile(q = 0.75)

# Significant increase if lower quartile after is above the upper quartile from before (boolean)
df_after_wd_incr = df_after_wd_lower > df_before_wd_upper
# Significant decrease if upper quartile after is below the lower quartile from before (boolean)
df_after_wd_decr = df_after_wd_upper < df_before_wd_lower

# Add up the number of days of significant increase/decrease (this creates a series from the dataframe)
s_after_wd_incr_sum = df_after_wd_incr.sum()
s_after_wd_decr_sum = df_after_wd_decr.sum()

# Update Index Names
s_after_wd_incr_sum.index.names = ['KPI']
s_after_wd_decr_sum.index.names = ['KPI']

# 5-7 weekdays with significant change to be considered overall as a signficant change
increase_list = {0:'No change', 1:'No change', 2:'No change', 3:'No change', 4:'No change', 5:'Increase', 6:'Increase', 7:'Increase'}
decrease_list = {0:'No change', 1:'No change', 2:'No change', 3:'No change', 4:'No change', 5:'Decrease', 6:'Decrease', 7:'Decrease'}

# Categorize every KPI as having an increase/decrease or no change
s_after_wd_incr_category = s_after_wd_incr_sum.replace(increase_list)
s_after_wd_decr_category = s_after_wd_decr_sum.replace(decrease_list)

### Categorize every KPI to indicate if an increase is good or a decrease is good ###

# Create a new series with the same KPIs by copying an existing series into it
s_after_wd_category = s_after_wd_incr_category

# Combine the increase and decrease assessments into the new series
# Count the number of KPIs
KPIs = range(s_after_wd_category.shape[0])

for KPI in KPIs:
    if s_after_wd_incr_category[KPI] == 'Increase':
        s_after_wd_category[KPI] = 'Increase'
    elif s_after_wd_decr_category[KPI] == 'Decrease':
        s_after_wd_category[KPI] = 'Decrease'

# Put change (s_after_category) in a dataframe, and create placeholders for other details
df_after_category = pd.DataFrame(s_after_category) # cell
df_after_category[1] = change_date
df_after_category[2] = coverage_category
df_after_category[3] = df_after_category[0] # change, i.e. s_after_category (Ex: Increase/Decrease)
df_after_category[4] = improvement_type['Improvement Type']
df_after_category[5] = df_after_category[3] # assessment (Ex: Improved/Degraded) --- placeholder
df_after_category[0] = cell

# Create an Assessment based on the Change and Improvment Type
for KPI in KPIs:
    if df_after_category[3][KPI] == 'Increase': # change
        if df_after_category[4][KPI] == 'Increase': # improvement_type
            df_after_category[5][KPI] = 'Improved' # assessment
        else:
            df_after_category[5][KPI] = 'Degraded'
    elif df_after_category[3][KPI] == 'Decrease':
        if df_after_category[4][KPI] == 'Decrease':
            df_after_category[5][KPI] = 'Improved'
        else:
            df_after_category[5][KPI] = 'Degraded'
    else:
        df_after_category[5][KPI] = 'No change'
