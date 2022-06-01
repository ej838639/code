"""
Identify the cells that had a significant change in timing advance and find the associated RET
Eric Johnson
Jan 2019
"""
import glob
import pandas as pd
import os

print('Folder with inputs')
path = input()
os.chdir(path)
from cco_inputs import *

### Inputs ###
target_cells_filename = 'CurrentSelection'

if duplicate_1_C == True:
    date_1_C_v1 = pd.DateOffset(date_1_C_v1_str)
    date_1_C_v2 = pd.DateOffset(date_1_C_v2_str)
    date_1_C_v1 = date_1_C.strftime('%m/%d/%Y')
    date_1_C_v2 = date_1_C.strftime('%m/%d/%Y')

date_1_C =   pd.to_datetime(date_1_C_str)
date_1_FT1 = pd.to_datetime(date_1_FT1_str)
date_1_FT2 = pd.to_datetime(date_1_FT2_str)
date_2_C = pd.to_datetime(date_2_C_str)
date_2_FT1 = pd.to_datetime(date_2_FT1_str)
date_2_FT2 = pd.to_datetime(date_2_FT2_str)

date_1_C = date_1_C.strftime('%m/%d/%Y')
date_1_FT1 = date_1_FT1.strftime('%m/%d/%Y')
date_1_FT2 = date_1_FT2.strftime('%m/%d/%Y')
date_2_C = date_2_C.strftime('%m/%d/%Y')
date_2_FT1 = date_2_FT1.strftime('%m/%d/%Y')
date_2_FT2 = date_2_FT2.strftime('%m/%d/%Y')

tilts1_C_filename = '1_Coarse'
tilts1_FT1_filename = '1_Fine_Tune_1'
tilts1_FT2_filename = '1_Fine_Tune_2'
tilts2_C_filename = '2_Coarse'
tilts2_FT1_filename = '2_Fine_Tune_1'
tilts2_FT2_filename = '2_Fine_Tune_2'

### Functions

# Update end values in cell_summary if there are non-blank values.
# If only use end values for last file, it may have blanks. This populates value with the last non-blank value
def updateEndValue(stage_str):
    try: # Nokia: Include Timing Advance
        cell_summary2 = cell_summary_start.merge(score_summary[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Timing_Advance Score','LTE_Coverage_Hole Score','LTE_Capacity Score']][(score_summary['Stage'] == stage_str)], left_on = 'Cell', right_on = 'Cell', how = 'left')
    except: # Ericsson: Exclude Timing Advance
        cell_summary2 = cell_summary_start.merge(score_summary[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Hole Score','LTE_Capacity Score']][(score_summary['Stage'] == stage_str)], left_on = 'Cell', right_on = 'Cell', how = 'left')
    cell_summary2 = cell_summary2.rename(index=str, columns={'Individual Cell C-CCO Score': 'Overall Score End', 'LTE_Coverage_Standard Score': 'Cov Std Score End', 'LTE_Coverage_Timing_Advance Score': 'Cov TA Score End', 'LTE_Coverage_Hole Score': 'Cov Hole Score End', 'LTE_Capacity Score': 'Cap Score End'})

    # If the scores are currently blank, then update it with the score from this stage
    cell_summary.loc[cell_summary[cell_summary.isnull()['Overall Score Start'] == True].index, 'Overall Score Start'] = cell_summary2.loc[cell_summary[cell_summary.isnull()['Overall Score Start'] == True].index, 'Overall Score End']
    cell_summary.loc[cell_summary[cell_summary.isnull()['Cov Std Score Start'] == True].index, 'Cov Std Score Start'] = cell_summary2.loc[cell_summary[cell_summary.isnull()['Cov Std Score Start'] == True].index, 'Cov Std Score End']
    try:
        cell_summary.loc[cell_summary[cell_summary.isnull()['Cov TA Score Start'] == True].index, 'Cov TA Score Start'] = cell_summary2.loc[cell_summary[cell_summary.isnull()['Cov TA Score Start'] == True].index, 'Cov TA Score End']
    except:
        pass
    cell_summary.loc[cell_summary[cell_summary.isnull()['Cov Hole Score Start'] == True].index, 'Cov Hole Score Start'] = cell_summary2.loc[cell_summary[cell_summary.isnull()['Cov Hole Score Start'] == True].index, 'Cov Hole Score End']
    cell_summary.loc[cell_summary[cell_summary.isnull()['Cap Score Start'] == True].index, 'Cap Score Start'] = cell_summary2.loc[cell_summary[cell_summary.isnull()['Cap Score Start'] == True].index, 'Cap Score End']

    # Update the end value the current stage is non-blank
    cell_summary.loc[cell_summary2[cell_summary2.isnull()['Overall Score End'] == False].index, 'Overall Score End'] = cell_summary2.loc[cell_summary2[cell_summary2.isnull()['Overall Score End'] == False].index, 'Overall Score End']
    cell_summary.loc[cell_summary2[cell_summary2.isnull()['Cov Std Score End'] == False].index, 'Cov Std Score End'] = cell_summary2.loc[cell_summary2[cell_summary2.isnull()['Cov Std Score End'] == False].index, 'Cov Std Score End']
    try:
        cell_summary.loc[cell_summary2[cell_summary2.isnull()['Cov TA Score End'] == False].index, 'Cov TA Score End'] = cell_summary2.loc[cell_summary2[cell_summary2.isnull()['Cov TA Score End'] == False].index, 'Cov TA Score End']
    except:
        pass
    cell_summary.loc[cell_summary2[cell_summary2.isnull()['Cov Hole Score End'] == False].index, 'Cov Hole Score End'] = cell_summary2.loc[cell_summary2[cell_summary2.isnull()['Cov Hole Score End'] == False].index, 'Cov Hole Score End']
    cell_summary.loc[cell_summary2[cell_summary2.isnull()['Cap Score End'] == False].index, 'Cap Score End'] = cell_summary2.loc[cell_summary2[cell_summary2.isnull()['Cap Score End'] == False].index, 'Cap Score End']

#def setTiltEnd(stage_str):
#    cell_summary['Tilt End'] = cell_summary.merge(tilt_summary[['Cell','Recommended E Tilt']][tilt_summary['Stage'] == stage_str], left_on = 'Cell', right_on = 'Cell', how = 'left')

### Load Files ###
files_csv = glob.glob(path + '\*.csv')
files = glob.glob(path + '\*.xls*')

# Load Target Cells
for file_ in files_csv:
    if target_cells_filename in file_:
        target_cells = pd.read_csv(file_)

# Load Parameters
for file_ in files:
    if duplicate_1_C == False:
        if tilts1_C_filename in file_:
            parameters = pd.read_excel(file_, sheetname = 'C-CCO Parameters')
    else:
        if tilts1_C_v1_filename in file_:
            parameters_v1 = pd.read_excel(file_, sheetname = 'C-CCO Parameters')
        if tilts1_C_v2_filename in file_:
            parameters_v2 = pd.read_excel(file_, sheetname = 'C-CCO Parameters')

# Load 1_Coarse
if duplicate_1_C == False:
    for file_ in files:
        if tilts1_C_filename in file_:
            tilts1_C = pd.read_excel(file_, sheetname = 'LTE Cells Recommendation')
            score1_C = pd.read_excel(file_, sheetname = 'LTE Cells Score Summary')
            exclusions1_C = pd.read_excel(file_, sheetname = 'LTE Cells Excluded')
else:
    for file_ in files:
        if tilts1_C_v1_filename in file_:
            tilts1_C_v1 = pd.read_excel(file_, sheetname = 'LTE Cells Recommendation')
            score1_C_v1 = pd.read_excel(file_, sheetname = 'LTE Cells Score Summary')
            exclusions1_C_v1 = pd.read_excel(file_, sheetname = 'LTE Cells Excluded')
    
        if tilts1_C_v2_filename in file_:
            tilts1_C_v2 = pd.read_excel(file_, sheetname = 'LTE Cells Recommendation')
            score1_C_v2 = pd.read_excel(file_, sheetname = 'LTE Cells Score Summary')
            exclusions1_C_v2 = pd.read_excel(file_, sheetname = 'LTE Cells Excluded')

### Consolidate tilt and score recommendations from all the spreadsheets
if duplicate_1_C == False:
    tilt_summary = tilts1_C[['Cell','Action','Current Electrical Tilt','Increment','Recommended E Tilt','Verified E Tilt']]
    tilt_summary['Date'] = date_1_C
    tilt_summary['Stage'] = '1_Coarse'
    
    try: # Nokia: include Timing Advance
        score_summary = score1_C[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Timing_Advance Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    except: # Ericsson: exclude Timing Advance
        score_summary = score1_C[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    
    score_summary['Date'] = date_1_C
    score_summary['Stage'] = '1_Coarse'
    
    exclusion_cells = exclusions1_C[['Cell','Cause']]
    exclusion_cells['Date'] = date_1_C
    exclusion_cells['Stage'] = '1_Coarse'

else:
    # 1_Coarse_v1
    tilt_summary = tilts1_C_v1[['Cell','Action','Current Electrical Tilt','Increment','Recommended E Tilt','Verified E Tilt']]
    tilt_summary['Date'] = date_1_C_v1
    tilt_summary['Stage'] = '1_Coarse_v1'
    
    try: # Nokia: include Timing Advance
        score_summary = score1_C_v1[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Timing_Advance Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    except: # Ericsson: exclude Timing Advance
        score_summary = score1_C_v1[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    
    score_summary['Date'] = date_1_C_v1
    score_summary['Stage'] = '1_Coarse_v1'
    
    exclusion_cells = exclusions1_C_v1[['Cell','Cause']]
    exclusion_cells['Date'] = date_1_C_v1
    exclusion_cells['Stage'] = '1_Coarse_v1'

    # 1_Coarse_v2
    tilt_summary_add = tilts1_C_v2[['Cell','Action','Current Electrical Tilt','Increment','Recommended E Tilt','Verified E Tilt']]
    tilt_summary_add['Date'] = date_1_C_v2
    tilt_summary_add['Stage'] = '1_Coarse_v2'
    tilt_summary = tilt_summary.append(tilt_summary_add)
    
    try: # Nokia: Include Timing Advance
        score_summary_add = score1_C_v2[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Timing_Advance Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    except: # Ericsson: Exclude Timing Advance
        score_summary_add = score1_C_v2[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    score_summary_add['Date'] = date_1_C_v2
    score_summary_add['Stage'] = '1_Coarse_v2'
    score_summary = score_summary.append(score_summary_add)
    
    exclusion_cells_add = exclusions1_C_v2[['Cell','Cause']]
    exclusion_cells_add['Date'] = date_1_C_v2
    exclusion_cells_add['Stage'] = '1_Coarse_v2'
    exclusion_cells = exclusion_cells.append(exclusion_cells_add)

if file_count >= 2:
# Load 1_FT1
    for file_ in files:
        if tilts1_FT1_filename in file_:
            try:
                tilts1_FT1 = pd.read_excel(file_, sheetname = 'LTE Cells Recommendation')
                score1_FT1 = pd.read_excel(file_, sheetname = 'LTE Cells Score Summary')
                exclusions1_FT1 = pd.read_excel(file_, sheetname = 'LTE Cells Excluded')
            except: # load blank table if a worksheet is missing
                if duplicate_1_C == False:
                    tilts1_FT1 = tilts1_C.iloc[0:0]
                    score1_FT1 = score1_C.iloc[0:0]
                    exclusions1_FT1 = exclusions1_C.iloc[0:0]
                if duplicate_1_C == True:
                    tilts1_FT1 = tilts1_C_v1.iloc[0:0]
                    score1_FT1 = score1_C_v1.iloc[0:0]
                    exclusions1_FT1 = exclusions1_C_v1.iloc[0:0]

    tilt_summary_add = tilts1_FT1[['Cell','Action','Current Electrical Tilt','Increment','Recommended E Tilt','Verified E Tilt']]
    tilt_summary_add['Date'] = date_1_FT1
    tilt_summary_add['Stage'] = '1_Fine_Tune_1'
    tilt_summary = tilt_summary.append(tilt_summary_add)
    
    try: # Nokia: Include Timing Advance
        score_summary_add = score1_FT1[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Timing_Advance Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    except: # Ericsson: Exclude Timing Advance
        score_summary_add = score1_FT1[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    score_summary_add['Date'] = date_1_FT1
    score_summary_add['Stage'] = '1_Fine_Tune_1'
    score_summary = score_summary.append(score_summary_add)
    
    exclusion_cells_add = exclusions1_FT1[['Cell','Cause']]
    exclusion_cells_add['Date'] = date_1_FT1
    exclusion_cells_add['Stage'] = '1_Fine_Tune_1'
    exclusion_cells = exclusion_cells.append(exclusion_cells_add)

if file_count >= 3:
# Load 1_FT2
    for file_ in files:
        if tilts1_FT2_filename in file_:
            try:
                tilts1_FT2 = pd.read_excel(file_, sheetname = 'LTE Cells Recommendation')
                score1_FT2 = pd.read_excel(file_, sheetname = 'LTE Cells Score Summary')
                exclusions1_FT2 = pd.read_excel(file_, sheetname = 'LTE Cells Excluded')
            except: # load blank table if a worksheet is missing
                if duplicate_1_C == False:
                    tilts1_FT1 = tilts1_C.iloc[0:0]
                    score1_FT1 = score1_C.iloc[0:0]
                    exclusions1_FT1 = exclusions1_C.iloc[0:0]
                if duplicate_1_C == True:
                    tilts1_FT1 = tilts1_C_v1.iloc[0:0]
                    score1_FT1 = score1_C_v1.iloc[0:0]
                    exclusions1_FT1 = exclusions1_C_v1.iloc[0:0]               

    tilt_summary_add = tilts1_FT2[['Cell','Action','Current Electrical Tilt','Increment','Recommended E Tilt','Verified E Tilt']]
    tilt_summary_add['Date'] = date_1_FT2
    tilt_summary_add['Stage'] = '1_Fine_Tune_2'
    tilt_summary = tilt_summary.append(tilt_summary_add)

    try: # Nokia: Include Timing Advance
        score_summary_add = score1_FT2[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Timing_Advance Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    except: # Ericsson: Exclude Timing Advance
        score_summary_add = score1_FT2[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    score_summary_add['Date'] = date_1_FT2
    score_summary_add['Stage'] = '1_Fine_Tune_2'
    score_summary = score_summary.append(score_summary_add)

    exclusion_cells_add = exclusions1_FT2[['Cell','Cause']]
    exclusion_cells_add['Date'] = date_1_FT2
    exclusion_cells_add['Stage'] = '1_Fine_Tune_2'
    exclusion_cells = exclusion_cells.append(exclusion_cells_add)

if file_count >= 4:
# Load 2_Coarse
    for file_ in files:
        try:
            if tilts2_C_filename in file_:
                tilts2_C = pd.read_excel(file_, sheetname = 'LTE Cells Recommendation')
                score2_C = pd.read_excel(file_, sheetname = 'LTE Cells Score Summary')
                exclusions2_C = pd.read_excel(file_, sheetname = 'LTE Cells Excluded')
        except: # load blank table if a worksheet is missing
                if duplicate_1_C == False:
                    tilts1_FT1 = tilts1_C.iloc[0:0]
                    score1_FT1 = score1_C.iloc[0:0]
                    exclusions1_FT1 = exclusions1_C.iloc[0:0]
                if duplicate_1_C == True:
                    tilts1_FT1 = tilts1_C_v1.iloc[0:0]
                    score1_FT1 = score1_C_v1.iloc[0:0]
                    exclusions1_FT1 = exclusions1_C_v1.iloc[0:0]

    tilt_summary_add = tilts2_C[['Cell','Action','Current Electrical Tilt','Increment','Recommended E Tilt','Verified E Tilt']]
    tilt_summary_add['Date'] = date_2_C
    tilt_summary_add['Stage'] = '2_Coarse'
    tilt_summary = tilt_summary.append(tilt_summary_add)

    try: # Nokia: Include Timing Advance
        score_summary_add = score2_C[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Timing_Advance Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    except: # Ericsson: Exclude Timing Advance
        score_summary_add = score2_C[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    score_summary_add['Date'] = date_2_C
    score_summary_add['Stage'] = '2_Coarse'
    score_summary = score_summary.append(score_summary_add)

    exclusion_cells_add = exclusions2_C[['Cell','Cause']]
    exclusion_cells_add['Date'] = date_2_C
    exclusion_cells_add['Stage'] = '2_Coarse'
    exclusion_cells = exclusion_cells.append(exclusion_cells_add)

if file_count >= 5:
# Load 2_FT1
    for file_ in files:
        if tilts2_FT1_filename in file_:
            try:
                tilts2_FT1 = pd.read_excel(file_, sheetname = 'LTE Cells Recommendation')
                score2_FT1 = pd.read_excel(file_, sheetname = 'LTE Cells Score Summary')
                exclusions2_FT1 = pd.read_excel(file_, sheetname = 'LTE Cells Excluded')
            except: # load blank table if a worksheet is missing
                if duplicate_1_C == False:
                    tilts1_FT1 = tilts1_C.iloc[0:0]
                    score1_FT1 = score1_C.iloc[0:0]
                    exclusions1_FT1 = exclusions1_C.iloc[0:0]
                if duplicate_1_C == True:
                    tilts1_FT1 = tilts1_C_v1.iloc[0:0]
                    score1_FT1 = score1_C_v1.iloc[0:0]
                    exclusions1_FT1 = exclusions1_C_v1.iloc[0:0]
    
    tilt_summary_add = tilts2_FT1[['Cell','Action','Current Electrical Tilt','Increment','Recommended E Tilt','Verified E Tilt']]
    tilt_summary_add['Date'] = date_2_FT1
    tilt_summary_add['Stage'] = '2_Fine_Tune_1'
    tilt_summary = tilt_summary.append(tilt_summary_add)

    try: # Nokia: Include Timing Advance
        score_summary_add = score2_FT1[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Timing_Advance Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    except: # Ericsson: Exclude Timing Advance
        score_summary_add = score2_FT1[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    score_summary_add['Date'] = date_2_FT1
    score_summary_add['Stage'] = '2_Fine_Tune_1'
    score_summary = score_summary.append(score_summary_add)

    exclusion_cells_add = exclusions2_FT1[['Cell','Cause']]
    exclusion_cells_add['Date'] = date_2_FT1
    exclusion_cells_add['Stage'] = '2_Fine_Tune_1'
    exclusion_cells = exclusion_cells.append(exclusion_cells_add)

if file_count >= 6:
# Load 2_FT2
    for file_ in files:
        if tilts2_FT2_filename in file_:
            try:
                tilts2_FT2 = pd.read_excel(file_, sheetname = 'LTE Cells Recommendation')
                score2_FT2 = pd.read_excel(file_, sheetname = 'LTE Cells Score Summary')
                exclusions2_FT2 = pd.read_excel(file_, sheetname = 'LTE Cells Excluded')
            except: # load blank table if a worksheet is missing
                if duplicate_1_C == False:
                    tilts1_FT1 = tilts1_C.iloc[0:0]
                    score1_FT1 = score1_C.iloc[0:0]
                    exclusions1_FT1 = exclusions1_C.iloc[0:0]
                if duplicate_1_C == True:
                    tilts1_FT1 = tilts1_C_v1.iloc[0:0]
                    score1_FT1 = score1_C_v1.iloc[0:0]
                    exclusions1_FT1 = exclusions1_C_v1.iloc[0:0]

    tilt_summary_add = tilts2_FT2[['Cell','Action','Current Electrical Tilt','Increment','Recommended E Tilt','Verified E Tilt']]
    tilt_summary_add['Date'] = date_2_FT2
    tilt_summary_add['Stage'] = '2_Fine_Tune_2'
    tilt_summary = tilt_summary.append(tilt_summary_add)

    try: # Nokia: Include Timing Advance
        score_summary_add = score2_FT2[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Timing_Advance Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    except: # Ericsson: Exclude Timing Advance
        score_summary_add = score2_FT2[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
    score_summary_add['Date'] = date_2_FT2
    score_summary_add['Stage'] = '2_Fine_Tune_2'
    score_summary = score_summary.append(score_summary_add)

    exclusion_cells_add = exclusions2_FT2[['Cell','Cause']]
    exclusion_cells_add['Date'] = date_2_FT2
    exclusion_cells_add['Stage'] = '2_Fine_Tune_2'
    exclusion_cells = exclusion_cells.append(exclusion_cells_add)

### Create view with one row per cell
# Group by on some of the columns
cell_summary = pd.DataFrame()
cell_summary['Tilts'] = tilt_summary.groupby(['Cell']).count()['Current Electrical Tilt']
cell_summary['Downtilts'] = tilt_summary[tilt_summary['Action'] == 'RET_Downtilt'].groupby(['Cell']).count()['Current Electrical Tilt']
cell_summary['Uptilts'] = tilt_summary[tilt_summary['Action'] == 'RET_Uptilt'].groupby(['Cell']).count()['Current Electrical Tilt']
cell_summary['Downtilts'] = cell_summary['Downtilts'].fillna(0)
cell_summary['Uptilts'] = cell_summary['Uptilts'].fillna(0)
cell_summary['Tilt Before Min'] =  tilt_summary.groupby(['Cell']).min()['Current Electrical Tilt']
cell_summary['Tilt Before Max'] =  tilt_summary.groupby(['Cell']).max()['Current Electrical Tilt']
cell_summary['Tilt After Min'] =  tilt_summary.groupby(['Cell']).min()['Recommended E Tilt']
cell_summary['Tilt After Max'] =  tilt_summary.groupby(['Cell']).max()['Recommended E Tilt']

cell_summary = cell_summary.reset_index()

# Find the starting and ending tilts: depends on downtilts/uptilt
cell_summary['Tilt Start'] = ''
cell_summary['Tilt End'] = ''
cell_summary['Tilt Start'][(cell_summary['Downtilts'] > 0) & (cell_summary['Uptilts'] == 0)] = cell_summary['Tilt Before Min']
cell_summary['Tilt End'][(cell_summary['Downtilts'] > 0) & (cell_summary['Uptilts'] == 0)] = cell_summary['Tilt After Max']
cell_summary['Tilt Start'][(cell_summary['Downtilts']== 0) & (cell_summary['Uptilts'] > 0)] = cell_summary['Tilt Before Max']
cell_summary['Tilt End'][(cell_summary['Downtilts']== 0) & (cell_summary['Uptilts'] > 0)] = cell_summary['Tilt After Min']
cell_summary['Tilt Start'][(cell_summary['Downtilts'] > 0) & (cell_summary['Uptilts'] > 0)] = 99
cell_summary['Tilt End'][(cell_summary['Downtilts'] > 0) & (cell_summary['Uptilts'] > 0)] = 99
cell_summary['Tilt Increment Sum'] = cell_summary['Tilt End'] - cell_summary['Tilt Start']

#if duplicate_1_C == False:
#    cell_summary = cell_summary.merge(tilt_summary[['Cell','Current Electrical Tilt']][tilt_summary['Stage'] == '1_Coarse'], left_on = 'Cell', right_on = 'Cell', how = 'left')
#
#if duplicate_1_C == True:
#    test = tilt_summary[['Cell','Current Electrical Tilt']][tilt_summary['Stage'] == '1_Coarse_v1'].groupby(['Cell']).first()
#    cell_summary = cell_summary.merge(test, left_on = 'Cell', right_on = 'Cell', how = 'left')
#    #cell_summary = cell_summary.merge(tilt_summary[['Cell','Current Electrical Tilt']][tilt_summary['Stage'] == '1_Coarse_v1'].groupby(['Cell']).first(), left_on = 'Cell', right_on = 'Cell', how = 'left')
#
#if file_count == 1 & duplicate_1_C == True:
#    cell_summary['Tilt End'] = cell_summary.merge(tilt_summary[['Cell','Recommended E Tilt']][tilt_summary['Stage'] == '1_Coarse_v2'], left_on = 'Cell', right_on = 'Cell', how = 'left')
#
#if file_count == 2:
#    setTiltEnd('1_Fine_Tune_1')
#
#if file_count == 3:
#    setTiltEnd('1_Fine_Tune_2')
#
#if file_count == 4:
#    setTiltEnd('2_Coarse')
#
#if file_count == 5:
#    setTiltEnd('2_Fine_Tune_1')
#
#if file_count == 6:
#    setTiltEnd('2_Fine_Tune_2')

# Add Band and Technology based on filter
cell_summary['Band'] = cell_summary['Cell'].str[:1]
cell_summary['Technology'] = ''
cell_summary['Technology'][cell_summary['Band'] == 'L'] = 'LTE'
cell_summary['Technology'][cell_summary['Band'] == 'B'] = 'LTE'
cell_summary['Technology'][cell_summary['Band'] == 'D'] = 'LTE'
cell_summary['Technology'][cell_summary['Band'] == 'E'] = 'LTE'
cell_summary['Technology'][cell_summary['Band'] == 'F'] = 'LTE'
cell_summary['Technology'][cell_summary['Band'] == 'U'] = 'UMTS'
cell_summary['Technology'][cell_summary['Band'] == 'P'] = 'UMTS'
cell_summary['Technology'][cell_summary['Band'] == 'G'] = 'GSM'

# Add the starting and ending scores
if duplicate_1_C == False: # Use 1_Coarse as start
    try: # Nokia: Include Timing Advance
        cell_summary = cell_summary.merge(score_summary[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Timing_Advance Score','LTE_Coverage_Hole Score','LTE_Capacity Score']][(score_summary['Stage'] == '1_Coarse')], left_on = 'Cell', right_on = 'Cell', how = 'left')
    except: # Ericsson: Exclude Timing Advance
        cell_summary = cell_summary.merge(score_summary[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Hole Score','LTE_Capacity Score']][(score_summary['Stage'] == '1_Coarse')], left_on = 'Cell', right_on = 'Cell', how = 'left')
    cell_summary = cell_summary.rename(index=str, columns={'Individual Cell C-CCO Score': 'Overall Score Start', 'LTE_Coverage_Standard Score': 'Cov Std Score Start', 'LTE_Coverage_Timing_Advance Score': 'Cov TA Score Start', 'LTE_Coverage_Hole Score': 'Cov Hole Score Start', 'LTE_Capacity Score': 'Cap Score Start'})

else: # Use 1_Coarse_v1 as start
    try: # Nokia: Include Timing Advance
        cell_summary = cell_summary.merge(score_summary[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Timing_Advance Score','LTE_Coverage_Hole Score','LTE_Capacity Score']][(score_summary['Stage'] == '1_Coarse_v1')], left_on = 'Cell', right_on = 'Cell', how = 'left')
    except: # Ericsson: Exclude Timing Advance
        cell_summary = cell_summary.merge(score_summary[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Hole Score','LTE_Capacity Score']][(score_summary['Stage'] == '1_Coarse_v1')], left_on = 'Cell', right_on = 'Cell', how = 'left')
    cell_summary = cell_summary.rename(index=str, columns={'Individual Cell C-CCO Score': 'Overall Score Start', 'LTE_Coverage_Standard Score': 'Cov Std Score Start', 'LTE_Coverage_Timing_Advance Score': 'Cov TA Score Start', 'LTE_Coverage_Hole Score': 'Cov Hole Score Start', 'LTE_Capacity Score': 'Cap Score Start'})

# Create a dataframe with only the start values
cell_summary_start = cell_summary

# Set End 
if file_count >= 1 & duplicate_1_C == False:
    # Set End same as Start to populate values in case there is only 1_Coarse
    try: # Nokia: Include Timing Advance
        cell_summary = cell_summary.merge(score_summary[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Timing_Advance Score','LTE_Coverage_Hole Score','LTE_Capacity Score']][(score_summary['Stage'] == '1_Coarse')], left_on = 'Cell', right_on = 'Cell', how = 'left')
    except: # Ericsson: Exclude Timing Advance
        cell_summary = cell_summary.merge(score_summary[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Hole Score','LTE_Capacity Score']][(score_summary['Stage'] == '1_Coarse')], left_on = 'Cell', right_on = 'Cell', how = 'left')
    cell_summary = cell_summary.rename(index=str, columns={'Individual Cell C-CCO Score': 'Overall Score End', 'LTE_Coverage_Standard Score': 'Cov Std Score End', 'LTE_Coverage_Timing_Advance Score': 'Cov TA Score End', 'LTE_Coverage_Hole Score': 'Cov Hole Score End', 'LTE_Capacity Score': 'Cap Score End'})

if file_count >= 1 & duplicate_1_C == True:
    # Set End to 1_Coarse_v2
    try: # Nokia: Include Timing Advance
        cell_summary = cell_summary.merge(score_summary[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Timing_Advance Score','LTE_Coverage_Hole Score','LTE_Capacity Score']][(score_summary['Stage'] == '1_Coarse_v2')], left_on = 'Cell', right_on = 'Cell', how = 'left')
    except: # Ericsson: Exclude Timing Advance
        cell_summary = cell_summary.merge(score_summary[['Cell','Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Hole Score','LTE_Capacity Score']][(score_summary['Stage'] == '1_Coarse_v2')], left_on = 'Cell', right_on = 'Cell', how = 'left')
    cell_summary = cell_summary.rename(index=str, columns={'Individual Cell C-CCO Score': 'Overall Score End', 'LTE_Coverage_Standard Score': 'Cov Std Score End', 'LTE_Coverage_Timing_Advance Score': 'Cov TA Score End', 'LTE_Coverage_Hole Score': 'Cov Hole Score End', 'LTE_Capacity Score': 'Cap Score End'})

# Set End same as the value for the last file in the group
if file_count >= 2:    
    ### Replace current end value with new end value if new end value is not null
    updateEndValue('1_Fine_Tune_1')

if file_count >= 3:
    ### Replace current end value with new end value if new end value is not null
    updateEndValue('1_Fine_Tune_2')

if file_count >= 4:
    ### Replace current end value with new end value if new end value is not null
    updateEndValue('2_Coarse')

if file_count >= 5:
    ### Replace current end value with new end value if new end value is not null
    updateEndValue('2_Fine_Tune_1')

if file_count >= 6:
    ### Replace current end value with new end value if new end value is not null
    updateEndValue('2_Fine_Tune_2')

# Re-arrange the columns
try: # Nokia: Include Timing Advance
    cell_summary = cell_summary[['Cell','Band','Technology','Downtilts','Uptilts','Tilt Start','Tilt End','Tilt Increment Sum','Tilts','Overall Score Start','Overall Score End','Cov Std Score Start','Cov Std Score End','Cov TA Score Start','Cov TA Score End','Cov Hole Score Start','Cov Hole Score End','Cap Score Start','Cap Score End']]
except: # Ericsson: Exluding Timing Advance
    cell_summary = cell_summary[['Cell','Band','Technology','Downtilts','Uptilts','Tilt Start','Tilt End','Tilt Increment Sum','Tilts','Overall Score Start','Overall Score End','Cov Std Score Start','Cov Std Score End','Cov Hole Score Start','Cov Hole Score End','Cap Score Start','Cap Score End']]

### Add band and technology to Target Cells tables
target_cells['Band'] = target_cells['Cell'].str[:1]
target_cells['Technology'] = ''
target_cells['Technology'][target_cells['Band'] == 'L'] = 'LTE'
target_cells['Technology'][target_cells['Band'] == 'B'] = 'LTE'
target_cells['Technology'][target_cells['Band'] == 'D'] = 'LTE'
target_cells['Technology'][target_cells['Band'] == 'E'] = 'LTE'
target_cells['Technology'][target_cells['Band'] == 'F'] = 'LTE'
target_cells['Technology'][target_cells['Band'] == 'U'] = 'UMTS'
target_cells['Technology'][target_cells['Band'] == 'P'] = 'UMTS'

### Summarize the results
# Target cells
summary = pd.Series(name = 'Count')
summary_col2 = pd.Series(name = 'Percentage')

summary['Target Cell'] = target_cells['Cell'].nunique()
summary_col2['Target Cell'] = ''
summary['Target LTE Cell'] = target_cells['Cell'][target_cells['Technology'] == 'LTE'].count()
summary_col2['Target LTE Cell'] = (100*summary['Target LTE Cell'] / summary['Target Cell']).round(0)
summary['Target LTE AWS Cell'] = target_cells['Cell'][target_cells['Band'] == 'L'].count()
summary_col2['Target LTE AWS Cell'] = (100*summary['Target LTE AWS Cell'] / summary['Target LTE Cell']).round(0)
summary['Target LTE PCS Cell'] = target_cells['Cell'][target_cells['Band'] == 'B'].count()
summary_col2['Target LTE PCS Cell'] = (100*summary['Target LTE PCS Cell'] / summary['Target LTE Cell']).round(0)
summary['Target LTE 700 Cell'] = target_cells['Cell'][target_cells['Band'] == 'D'].count()
summary_col2['Target LTE 700 Cell'] = (100*summary['Target LTE 700 Cell'] / summary['Target LTE Cell']).round(0)
summary['Target LTE 600 Cell'] = target_cells['Cell'][target_cells['Band'] == 'E'].count()
summary_col2['Target LTE 600 Cell'] = (100*summary['Target LTE 600 Cell'] / summary['Target LTE Cell']).round(0)
summary['Target LTE AWS3 Cell'] = target_cells['Cell'][target_cells['Band'] == 'F'].count()
summary_col2['Target LTE AWS3 Cell'] = (100*summary['Target LTE AWS3 Cell'] / summary['Target LTE Cell']).round(0)
summary['Target UMTS Cell'] = target_cells['Cell'][target_cells['Technology'] == 'UMTS'].count()
summary_col2['Target UMTS Cell'] = (100*summary['Target UMTS Cell'] / summary['Target Cell']).round(0)
summary['Target UMTS AWS Cell'] = target_cells['Cell'][target_cells['Band'] == 'U'].count()
try:
    summary_col2['Target UMTS AWS Cell'] = (100*summary['Target UMTS AWS Cell'] / summary['Target UMTS Cell']).round(0)
except:
    summary_col2['Target UMTS AWS Cell'] = 0
try:
    summary['Target UMTS PCS Cell'] = target_cells['Cell'][target_cells['Band'] == 'P'].count()
except:
    summary['Target UMTS PCS Cell'] = 0
try:
    summary_col2['Target UMTS PCS Cell'] = (100*summary['Target UMTS PCS Cell'] / summary['Target UMTS Cell']).round(0)
except:
    summary_col2['Target UMTS PCS Cell']
# Tilted cells
summary['Tilted Cell'] = tilt_summary['Cell'].nunique()
summary_col2['Tilted Cell'] = (100*summary['Tilted Cell'] / summary['Target Cell']).round(0)
summary['Tilted LTE Cell'] = cell_summary['Cell'][cell_summary['Technology'] == 'LTE'].count()
summary_col2['Tilted LTE Cell'] = (100*summary['Tilted LTE Cell'] / summary['Tilted Cell']).round(0)
summary['Tilted LTE AWS Cell'] = cell_summary['Cell'][cell_summary['Band'] == 'L'].count()
summary_col2['Tilted LTE AWS Cell'] = (100*summary['Tilted LTE AWS Cell'] / summary['Tilted LTE Cell']).round(0)
summary['Tilted LTE PCS Cell'] = cell_summary['Cell'][cell_summary['Band'] == 'B'].count()
summary_col2['Tilted LTE PCS Cell'] = (100*summary['Tilted LTE PCS Cell'] / summary['Tilted LTE Cell']).round(0)
summary['Tilted LTE 700 Cell'] = cell_summary['Cell'][cell_summary['Band'] == 'D'].count()
summary_col2['Tilted LTE 700 Cell'] = (100*summary['Tilted LTE 700 Cell'] / summary['Tilted LTE Cell']).round(0)
summary['Tilted LTE 600 Cell'] = cell_summary['Cell'][cell_summary['Band'] == 'E'].count()
summary_col2['Tilted LTE 600 Cell'] = (100*summary['Tilted LTE 600 Cell'] / summary['Tilted LTE Cell']).round(0)
summary['Tilted LTE AWS3 Cell'] = cell_summary['Cell'][cell_summary['Band'] == 'F'].count()
summary_col2['Tilted LTE AWS3 Cell'] = (100*summary['Tilted LTE AWS3 Cell'] / summary['Tilted LTE Cell']).round(0)
summary['Tilted UMTS Cell'] = cell_summary['Cell'][cell_summary['Technology'] == 'UMTS'].count()
summary_col2['Tilted UMTS Cell'] = (100*summary['Tilted UMTS Cell'] / summary['Tilted Cell']).round(0)
summary['Tilted UMTS AWS Cell'] = cell_summary['Cell'][cell_summary['Band'] == 'U'].count()
summary_col2['Tilted UMTS AWS Cell'] = (100*summary['Tilted UMTS AWS Cell'] / summary['Tilted UMTS Cell']).round(0)
summary['Tilted UMTS PCS Cell'] = cell_summary['Cell'][cell_summary['Band'] == 'P'].count()
summary_col2['Tilted UMTS PCS Cell'] = (100*summary['Tilted UMTS PCS Cell'] / summary['Tilted UMTS Cell']).round(0)
summary['Tilt'] = tilt_summary['Cell'].count()
summary_col2['Tilt'] = ''
summary['Downtilt'] = tilt_summary['Cell'][tilt_summary['Action']=='RET_Downtilt'].count()
summary_col2['Downtilt'] = (100*summary['Downtilt'] / summary['Tilt']).round(0)
summary['Uptilt'] = tilt_summary['Cell'][tilt_summary['Action']=='RET_Uptilt'].count()
summary_col2['Uptilt'] = (100*summary['Uptilt'] / summary['Tilt']).round(0)

# Convert series to dataframe and add percentages
summary_df = summary.to_frame()
summary_df.loc[:,'Percentage'] = summary_col2
summary_df = summary_df.fillna(value=0)

## Summary per stage
cell_stage = pd.DataFrame()
cell_stage_score = pd.DataFrame()
cell_stage = tilt_summary.groupby(['Cell','Action','Date','Stage']).first()[['Current Electrical Tilt','Recommended E Tilt','Increment']]
try: # Nokia: Including Timing Advance
    cell_stage_score = score_summary.groupby(['Cell','Date','Stage']).first()[['Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Timing_Advance Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
except: # Ericsson: Exluding Timing Advance
    cell_stage_score = score_summary.groupby(['Cell','Date','Stage']).first()[['Individual Cell C-CCO Score','LTE_Coverage_Standard Score','LTE_Coverage_Hole Score','LTE_Capacity Score']]
cell_stage_score = cell_stage_score.rename(index=str, columns={'Individual Cell C-CCO Score': 'Overall Score', 'LTE_Coverage_Standard Score': 'Cov Std Score', 'LTE_Coverage_Timing_Advance Score': 'Cov TA Score', 'LTE_Coverage_Hole Score': 'Cov Hole Score', 'LTE_Capacity Score': 'Cap Score'})
cell_stage = cell_stage.reset_index()
cell_stage_score = cell_stage_score.reset_index()
cell_stage = cell_stage.merge(cell_stage_score, left_on=['Cell','Date','Stage'], right_on=['Cell','Date','Stage'], how='left')
cell_stage = cell_stage.sort_values(by=['Cell', 'Stage'])

# Convert series to dataframe and add percentages
summary_df = summary.to_frame()
summary_df.loc[:,'Percentage'] = summary_col2
summary_df = summary_df.fillna(value=0)

### Summarize the exclusions
# Overall
exclusion_summary = pd.DataFrame()
exclusion_summary['Count'] = exclusion_cells.groupby(['Cause']).count()['Cell']

# per stage
exclusion_stage = pd.DataFrame()
exclusion_stage['Count'] = exclusion_cells.groupby(['Cause','Stage']).count()['Cell']

# Order tilt and score
tilt_summary = tilt_summary.sort_values(by=['Cell', 'Stage'])
score_summary = score_summary.sort_values(by=['Cell', 'Stage'])

### Export
with pd.ExcelWriter(cluster_name + ' Results.xlsx') as writer:
    summary_df.to_excel(writer, sheet_name='Summary')
    cell_summary.to_excel(writer, sheet_name='Cell Summary', index = False)
    cell_stage.to_excel(writer, sheet_name='Cell Stage', index = False)
    #tilt_summary.to_excel(writer, sheet_name='Tilt Summary', index = False)
    #score_summary.to_excel(writer, sheet_name='Score Summary', index = False)
    exclusion_summary.to_excel(writer, sheet_name='Exclusion Cause Summary')
    exclusion_stage.to_excel(writer, sheet_name='Exclusion Cause Stages')
    exclusion_cells.to_excel(writer, sheet_name='Exclusion Cause Cells', index = False)
    target_cells.to_excel(writer, sheet_name='Target Cells', index = False)
    if duplicate_1_C == False:
        parameters.to_excel(writer, sheet_name='Parameters', index = False)
    else:
        parameters_v1.to_excel(writer, sheet_name='Parameters 1_Coarse v1', index = False)
        parameters_v2.to_excel(writer, sheet_name='Parameters 1_Coarse v2', index = False)
        
#print('Results file exported to current directory. Hit enter to exit')
#path = input()
