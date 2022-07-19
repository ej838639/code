"""
Find Top 95% Neighbors and create a csv to create a TPIM cluster
Eric Johnson
Feb 2018
"""

import glob
import pandas as pd
import os


### Inputs ###
cell = 'MW_CCO_Test2'
neighbors_filename = 'LTE_Handover_Attempts - ' + cell
region = 'Central'
market = 'Indianapolis'
cluster = cell + '_neigh'
path=r"C:\Users\ejohnso43\Documents\1_2018\SON\Nokia Modules\C-CCO\Indianapolis"
os.chdir(path)

# Load the neighbor KPIs
files = glob.glob(path + '\*.xls*')

for file_ in files:
    if neighbors_filename in file_:
        df = pd.read_excel(file_, parse_dates = ['Period start time'])

# Find the Top 95% neighbors
df = df.sort_values(by=['eNB HO Execution Attempts'], ascending = False)
df['Cumulative Handover %'] = df['eNB HO Execution Attempts'].cumsum()/df['eNB HO Execution Attempts'].sum()
# df['Cumulative Handover %'] = pd.Series(["{0:.1f}%".format(val * 100) for val in df['Cumulative Handover %']], index = df.index)
# df = df[df['Cumulative Handover %'] < .95][['Target LNCEL name','eNB HO Execution Attempts','Cumulative Handover %']]

# Create a list of source cells
df_source = df['CELL'].drop_duplicates()
df_source = pd.DataFrame(df_source)

# Add columns needed to create TPIM cluster
df_source = df_source.rename(columns={'CELL': 'Cell'})

# Filter for only the Top 95% neighbors and only include the target cells
s = df[df['Cumulative Handover %'] < .95]['NEIGHBOR_CELL']

# We only included one column, so it create a series, so convert back to a dataframe
df = pd.DataFrame(s)
df = df.rename(columns={'NEIGHBOR_CELL': 'Cell'})

# Add the source cells to the list (otherwise we would only have the neighbor cells)
df = df.append(df_source)

# Add columns needed for TPIM cluster
df = df.assign(**{'Site':''})

# Re-order to move CELL_NAME to the correct position
df = df[['Site','Cell']]

# Wuala
df.to_excel(cluster + '.xlsx', index = False)