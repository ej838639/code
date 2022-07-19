"""
Find Top 95% of 56m bins where a cell has coverage
Eric Johnson
Jan 2018
"""

import glob
import pandas as pd
import os


### Inputs ###
cell = 'NC County Dominance'
freqbin_filename = 'FreqBin NC County Dec 7'
path=r"C:\Users\ejohnso43\Documents\1_2017\LSR\Dominance\Markets\Philadelphia\NC County"
os.chdir(path)

# Load the neighbor KPIs
files = glob.glob(path + '\*.xlsx')

for file_ in files:
    if freqbin_filename in file_:
        df = pd.read_excel(file_, parse_dates = ['DATE_PART'])

# Group by 56m bins
df = df[['HEX56_ID','SUM_RRC_ATTEMPTS_TC']].groupby('HEX56_ID').sum()

# Find the Top 95% neighbors
df = df.sort_values(by=['SUM_RRC_ATTEMPTS_TC'], ascending = False)
df['Cumulative Traffic %'] = df['SUM_RRC_ATTEMPTS_TC'].cumsum()/df['SUM_RRC_ATTEMPTS_TC'].sum()

# Filter for only the Top 95% neighbors and only include the target cells
df = df[df['Cumulative Traffic %'] < .95]

# Wuala
df.to_excel('Top 95% bins - ' + cell + '.xlsx', index = True)

# Create list of bins to use for a query
s = df.index.tolist()
