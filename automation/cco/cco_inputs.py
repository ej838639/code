"""
Inputs for the cco exe to consolidate CCO spreadsheet exports
Eric Johnson
Jan 2019
"""

# Enter a name to use for the results
cluster_name = 'CCO Los Angeles WELAC18 97cells Nov 29'

# Enter the number of CCO spreadsheets that have been generated. Ex: 5 means that 2_FT1 has been generated
file_count = 5

# If you ran CCO in closed loop, stopped it before 1_FT1, and then started it again, change to True and enter details
duplicate_1_C = False
tilts1_C_v1_filename = '1_Coarse_2018-10-05T15.36.03'
tilts1_C_v2_filename = '1_Coarse_2018-10-09T14.24.58'
date_1_C_v1_str = '10/5/2018'
date_1_C_v2_str = '10/9/2018'

# Enter the dates for as many files as you have
date_1_C_str = '11/29/2018'
date_1_FT1_str = '11/30/2018'
date_1_FT2_str = '12/3/2018'
date_2_C_str = '12/6/2018'
date_2_FT1_str = '12/7/2018'
date_2_FT2_str = '12/10/2018'