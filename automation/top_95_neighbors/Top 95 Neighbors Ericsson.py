"""
Find Top 95% Neighbors and create a csv to create a TPIM cluster
Eric Johnson
Jan 2018
"""

import glob
import pandas as pd
import os


### Inputs ###
cell = 'L1NC3708B21'
neighbors_filename = 'LTE_Handover_Attempts - ' + cell
region = 'NORTHEAST'
market = 'Philadelphia'
cluster = cell + ' neigh'
path=r"C:\Users\ejohnso43\Documents\1_2018\Dominance\Markets\Philadelphia\KPIs\Results"
os.chdir(path)

# Load the neighbor KPIs
files = glob.glob(path + '\*.xls*')

for file_ in files:
    if neighbors_filename in file_:
        df = pd.read_excel(file_, parse_dates = ['Period start time'])

# Find the Top 95% neighbors
df = df.sort_values(by=['pmHoExeAttLteIntraF (C2)'], ascending = False)
df['Cumulative Handover %'] = df['pmHoExeAttLteIntraF (C2)'].cumsum()/df['pmHoExeAttLteIntraF (C2)'].sum()

# Create a list of source cells
df_source = df['EUCL name'].drop_duplicates()
df_source = pd.DataFrame(df_source)

# Add columns needed to create TPIM cluster
df_source = df_source.rename(columns={'EUCL name': 'CELL_NAME'})

# Filter for only the Top 95% neighbors and only include the target cells
s = df[df['Cumulative Handover %'] < .95]['EUCR name']

# We only included one column, so it create a series, so convert back to a dataframe
df = pd.DataFrame(s)
df = df.rename(columns={'EUCR name': 'CELL_NAME'})

# Add the source cells to the list (otherwise we would only have the neighbor cells)
df = df.append(df_source)

# Add columns needed for TPIM cluster
df = df.assign(**{'REGION_ID':region, 'MARKET_ID':market, 'CLUSTER_ID':cluster, 'CELL_TYPE':'LTE', 'OPERATION_TYPE':'M', 'OBJECT_TYPE':'SECTOR', 'CLUSTER_TYPE':'UDC'})

# Re-order to move CELL_NAME to the correct position
df = df[['REGION_ID','MARKET_ID','CLUSTER_ID','CELL_TYPE','CELL_NAME','OPERATION_TYPE','OBJECT_TYPE','CLUSTER_TYPE']]

# Wuala
df.to_csv(cluster + '.csv', index = False)