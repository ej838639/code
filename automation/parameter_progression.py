"""
Compare the parameters audited and enforced for two different PBL baselines
Eric Johnson
Sept 2021
"""
import glob
import pandas as pd
import os
import numpy as np
from datetime import datetime

detailed_export = input('Do you want the detailed exports? (y/n): ')

# path = input()
path = r'C:\Users\ejohnso43\Documents\dev\python\Parameter Progression'
os.chdir(path)

# datetime object containing current date and time
current_date_time = datetime.now()
current_date_time_str = current_date_time.strftime("%Y-%m-%d %H%M")

### Run the following for every file in the default folder
### Load Files ###
files = glob.glob(path + '\*.xls*')
first_run_flag = True

for file_ in files:
    file_split = file_.split('_')
    try:
        # If try of file_split[2] has an error, then this is not the right type of file
        if file_split[1] == 'Baseline':
            vendor = file_split[2]
            tech = file_split[3]
            date_1_str = file_split[4]
            time_1_str = file_split[5][:5]
            date_1 = pd.to_datetime(date_1_str)
            date_1_C = date_1.strftime('%m/%d/%Y')
            baseline_1 = pd.read_excel(file_, sheet_name='Parameters')

            if 'erc' in vendor:
                baseline_1_features = pd.read_excel(file_, sheet_name='Feature Activations')

            ### New dataframe with only desired columns
            if 'nsn' in vendor:
                baseline_1_working = baseline_1[['ID Current', 'Abbreviated MO', 'T Mobile Recommended Value User Value', 'Modification', 'SON Audit Rule', 'SON Enforce this Parameter']]

            elif 'erc' in vendor:
                baseline_1_working = baseline_1[['Parameter MO', 'T Mobile Recommended Value User Value', 'Change Take Effect', 'SON Audit Rule', 'SON Enforce this Parameter']]
                baseline_1_working_features = baseline_1_features[['Parameter MO', 'T Mobile Recommended Value User Value', 'SON Audit Rule', 'SON Enforce this Parameter']]
                baseline_1_working = baseline_1_working.append(baseline_1_working_features)
                baseline_1_working.loc[:,'SON Enforce this Parameter'] = baseline_1_working['SON Enforce this Parameter'].replace({True: 'TRUE', 'True':'TRUE', False: 'FALSE'})

            baseline_1_working = baseline_1_working.fillna('N/A')

            # Add Recommended Value Category: User Value is defined vs not defined
            baseline_1_working['Recommended Value Category'] = np.where(baseline_1_working['T Mobile Recommended Value User Value'].isin(['CIQ','N/A','NA','Not modifiable','IRRELEVANT','TBD','"None"']) == True, 'Not defined','Defined')

            # Add Parameter Category: Audit Rule, Single Value, Range of Values, Defined but not PCE Audited
            baseline_1_working['SON Audit Category'] = np.where(baseline_1_working['SON Audit Rule'].str.contains('test') == True, 'Not defined',
                                                       np.where(baseline_1_working['SON Audit Rule'].str.startswith('if') == True, 'Audit Rule',
                                                       np.where(baseline_1_working['SON Audit Rule'].str.contains(' to ') == True, 'Range of Values',
                                                       np.where(baseline_1_working['SON Audit Rule'].str.contains(',') == True, 'Range of Values',
                                                       np.where(baseline_1_working['Recommended Value Category'].str.contains('Not defined') == True, 'Not defined',
                                                       np.where(baseline_1_working['SON Audit Rule'].str.contains('N/A') == True, 'Defined but not PCE Audited', 'Single Value'))))))

            #baseline_1_working.loc[:,'SON Audit Category'] = baseline_1_working[baseline_1_working['Recommended Value Category'].str.contains('Not defined') == True]['Recommended Value Category']
            #baseline_1_working[['SON Audit Category']] = baseline_1_working[baseline_1_working['Recommended Value Category'].str.contains('Not defined') == True][['Recommended Value Category']]

            # Add Impact column to indicate if it is online or service impacting
            if 'nsn' in vendor:
                baseline_1_working['Impact'] = np.where(baseline_1_working['Modification'].str.contains('On-line') == True, 'Online',
                                               np.where(baseline_1_working['Modification'].str.contains('BTS restart needed') == True, 'Service Impacting',
                                               np.where(baseline_1_working['Modification'].str.contains('Conditional BTS restart') == True, 'Service Impacting',
                                               np.where(baseline_1_working['Modification'].str.contains('Requires object locking') == True, 'Service Impacting','Not modifiable'))))

            elif 'erc' in vendor:
                baseline_1_working['Impact'] = np.where(baseline_1_working['Change Take Effect'].str.contains('restart') == True, 'Service Impacting',
                                               np.where(baseline_1_working['Change Take Effect'].str.contains('Restart') == True, 'Service Impacting',
                                               np.where(baseline_1_working['Change Take Effect'].str.contains('lock') == True, 'Service Impacting','Online')))

            ### Parameters in PBL ###
            baseline_1_count = len(baseline_1_working.index)
            baseline_1_count_per_category = baseline_1_working['SON Audit Category'].value_counts()

            ### Defined Value ###
            baseline_1_defined_value_count = len(baseline_1_working[baseline_1_working['Recommended Value Category'].isin(['Defined']) == True].index)
            baseline_1_defined_value_count_per_category = baseline_1_working['SON Audit Category'][baseline_1_working['Recommended Value Category'].isin(['Defined']) ].value_counts()

            ### Defined Value and Online Change ###
            baseline_1_defined_value_online_count = len(baseline_1_working[baseline_1_working['Recommended Value Category'].isin(['Defined']) &
                                                                           baseline_1_working['Impact'].isin(['Online']) == True].index)

            baseline_1_defined_value_online_count_per_category = baseline_1_working['SON Audit Category'][baseline_1_working['Recommended Value Category'].isin(['Defined']) &
                                                                                                          baseline_1_working['Impact'].isin(['Online']) == True].value_counts()

            ### Defined Value and Service Impacting ###
            baseline_1_defined_value_service_impacting_count = len(baseline_1_working[baseline_1_working['Recommended Value Category'].isin(['Defined']) &
                                                                            baseline_1_working['Impact'].isin(['Service Impacting']) == True].index)
            baseline_1_defined_value_service_impacting_count_per_category = baseline_1_working['SON Audit Category'][baseline_1_working['Recommended Value Category'].isin(['Defined']) &
                                                                            baseline_1_working['Impact'].isin(['Service Impacting']) == True].value_counts()

            ### PCE Audited ###
            baseline_1_pce_audited_count = len(baseline_1_working[baseline_1_working['SON Audit Category'].isin(['Single Value','Range of Values','Audit Rule']) == True].index)
            baseline_1_pce_audited_count_per_category = baseline_1_working['SON Audit Category'][baseline_1_working['SON Audit Category'].isin(['Single Value','Range of Values','Audit Rule'])].value_counts()

            ### PCE Audited and Online Change ###
            baseline_1_pce_audited_online_count = len(baseline_1_working[baseline_1_working['SON Audit Category'].isin(['Single Value','Range of Values','Audit Rule']) &
                                                                         baseline_1_working['Impact'].isin(['Online'])  == True].index)
            baseline_1_pce_audited_online_count_per_category = baseline_1_working['SON Audit Category'][baseline_1_working['SON Audit Category'].isin(['Single Value','Range of Values','Audit Rule']) &
                                                                                                        baseline_1_working['Impact'].isin(['Online']) == True].value_counts()

            ### PCE Enforced and Online Change ###

            baseline_1_pce_enforced_online_count = len(baseline_1_working[baseline_1_working['SON Audit Category'].isin(['Single Value','Range of Values','Audit Rule']) &
                                                                          baseline_1_working['Impact'].isin(['Online']) &
                                                                          baseline_1_working['SON Enforce this Parameter'].isin(['TRUE','Enforce on NA']) == True].index)

            baseline_1_pce_enforced_online_count_per_category = baseline_1_working['SON Audit Category'][baseline_1_working['SON Audit Category'].isin(['Single Value','Range of Values','Audit Rule']) &
                                                                                                         baseline_1_working['Impact'].isin(['Online']) &
                                                                                                         baseline_1_working['SON Enforce this Parameter'].isin(['TRUE','True','Enforce on NA']) == True].value_counts()

            ### % PCE Enforced and Online Change vs Defined Value ###
            baseline_1_pce_enforced_vs_defined_value_online_per = baseline_1_pce_enforced_online_count / baseline_1_defined_value_online_count
            baseline_1_pce_enforced_vs_defined_value_online_per = round(baseline_1_pce_enforced_vs_defined_value_online_per,2)
            #baseline_1_pce_enforced_vs_defined_value_online_per = "{:.0%}".format(baseline_1_pce_enforced_vs_defined_value_online_per)

            ### % Defined Value and Online Change Enforced ###
            baseline_1_pce_enforced_vs_all_per = baseline_1_pce_enforced_online_count / baseline_1_defined_value_count
            baseline_1_pce_enforced_vs_all_per = round(baseline_1_pce_enforced_vs_all_per,2)
            #baseline_1_pce_enforced_vs_all_per = "{:.0%}".format(baseline_1_pce_enforced_vs_all_per)
            #baseline_1_pce_enforced_vs_all_per = baseline_1_pce_enforced_vs_all_per.apply(lambda x: '%.0f' % x)

            baseline_1_pce_enforced_online_count_per_category_per = baseline_1_pce_enforced_online_count_per_category / baseline_1_defined_value_online_count_per_category
            baseline_1_pce_enforced_online_count_per_category_per = round(baseline_1_pce_enforced_online_count_per_category_per,2)
            baseline_1_pce_enforced_online_count_per_category_per = baseline_1_pce_enforced_online_count_per_category_per.fillna(0.0)

            ##################
            # Create dataframe of summary and export
            ##################

            ### Summary of Baseline 1
            baseline_1_summary = baseline_1_count_per_category.to_frame()
            baseline_1_summary = baseline_1_summary.rename(columns={'SON Audit Category': 'Parameters in PBL'})
            baseline_1_summary.loc[:,'Defined Value'] = baseline_1_defined_value_count_per_category
            baseline_1_summary.loc[:,'Defined Value Online Change'] = baseline_1_defined_value_online_count_per_category
            baseline_1_summary.loc[:,'Defined Value Service Impacting'] = baseline_1_defined_value_service_impacting_count_per_category
            baseline_1_summary.loc[:,'PCE Audited'] = baseline_1_pce_audited_count_per_category
            baseline_1_summary.loc[:,'PCE Audited Online Change'] = baseline_1_pce_audited_online_count_per_category
            baseline_1_summary.loc[:,'PCE Enforced Online Change'] = baseline_1_pce_enforced_online_count_per_category
            baseline_1_summary = baseline_1_summary.fillna(0)
            baseline_1_summary = baseline_1_summary.astype('int64')
            baseline_1_summary = baseline_1_summary.reindex(['Single Value','Range of Values','Audit Rule', 'Defined but not PCE Audited', 'Not defined'])

            baseline_1_totals = pd.DataFrame(data={"Parameters in PBL": [baseline_1_count],
                                                   "Defined Value": [baseline_1_defined_value_count],
                                                   "Defined Value Online Change": [baseline_1_defined_value_online_count],
                                                   "Defined Value Service Impacting": [baseline_1_defined_value_service_impacting_count],
                                                   "PCE Audited": [baseline_1_pce_audited_count],
                                                   "PCE Audited Online Change": [baseline_1_pce_audited_online_count],
                                                   "PCE Enforced Online Change": [baseline_1_pce_enforced_online_count]})

            baseline_1_totals.index = ['Total']

            baseline_1_summary = baseline_1_summary.append(baseline_1_totals)

            ##################
            # Create one row output of results
            ##################

            # Create a dataframe with key fields for the first columns
            baseline_1_key = pd.DataFrame(data=[[date_1_C, time_1_str, vendor, tech, '']])
            baseline_1_key = baseline_1_key.rename(columns={0: 'Date', 1: 'Time', 2: 'Vendor', 3: 'Tech', 4: 'Parameters'})

            # Create dataframe starting with the totals, but do not include the PCE Audited column
            baseline_1_totals_p1 = baseline_1_totals.drop(columns = ['PCE Audited'])
            baseline_1_totals_p1 = baseline_1_totals_p1.rename(index={'Total': 0})

            # Create dataframe for percentages of totals
            baseline_1_totals_p2 = pd.DataFrame(data=[[baseline_1_pce_enforced_vs_defined_value_online_per, baseline_1_pce_enforced_vs_all_per]])
            baseline_1_totals_p2 = baseline_1_totals_p2.rename(columns={0: '% PCE Enforced Online vs Defined Value', 1: '% PCE Enforced vs Defined Value'})

            # Create dataframe for percentages of SON Audit Category
            baseline_1_pce_enforced_online_count_per_category_per_df = pd.DataFrame(data=[baseline_1_pce_enforced_online_count_per_category_per])
            baseline_1_pce_enforced_online_count_per_category_per_df = baseline_1_pce_enforced_online_count_per_category_per_df.rename(index={'SON Audit Category': 0})
            #baseline_1_pce_enforced_online_count_per_category_per_df = round(baseline_1_pce_enforced_online_count_per_category_per_df,2)
            baseline_1_pce_enforced_online_count_per_category_per_df = baseline_1_pce_enforced_online_count_per_category_per_df.rename(columns={'Single Value': '% PCE Enforced Online vs Defined Value - Single Value',
                                                                              'Range of Values': '% PCE Enforced Online vs Defined Value - Range of Values',
                                                                              'Audit Rule': '% PCE Enforced Online vs Defined Value - Audit Rule',
                                                                              'Defined but not PCE Audited': '% PCE Enforced Online vs Defined Value - Defined but not PCE Audited'})

            # Create dataframes for Single Value, Range of Values, Audit Rule, and Defined but not PCE Audited and only keep 4 of the 7 columns
            # Append "Single Value" to the end of the column names for baseline_1_single_value. Do the same for the other dataframes
            # Single Value
            baseline_1_single_value = baseline_1_summary.iloc[[0]].copy()
            baseline_1_single_value = baseline_1_single_value.drop(columns = ['Parameters in PBL','Defined Value','PCE Audited'])
            baseline_1_single_value = baseline_1_single_value.rename(index={'Single Value': 0})
            baseline_1_single_value = baseline_1_single_value.rename(columns={'Defined Value Online Change': 'Defined Value Online Change - Single Value',
                                                                              'Defined Value Service Impacting': 'Defined Value Service Impacting - Single Value',
                                                                              'PCE Audited Online Change': 'PCE Audited Online Change - Single Value',
                                                                              'PCE Enforced Online Change': 'PCE Enforced Online Change - Single Value'})

            # Range of Values
            baseline_1_range_of_values = baseline_1_summary.iloc[[1]].copy()
            baseline_1_range_of_values = baseline_1_range_of_values.drop(columns = ['Parameters in PBL','Defined Value','PCE Audited'])
            baseline_1_range_of_values = baseline_1_range_of_values.rename(index={'Range of Values': 0})
            baseline_1_range_of_values = baseline_1_range_of_values.rename(columns={'Defined Value Online Change': 'Defined Value Online Change - Range of Values',
                                                                              'Defined Value Service Impacting': 'Defined Value Service Impacting - Range of Values',
                                                                              'PCE Audited Online Change': 'PCE Audited Online Change - Range of Values',
                                                                              'PCE Enforced Online Change': 'PCE Enforced Online Change - Range of Values'})

            # Audit Rule
            baseline_1_audit_rule = baseline_1_summary.iloc[[2]].copy()
            baseline_1_audit_rule = baseline_1_audit_rule.drop(columns = ['Parameters in PBL','Defined Value','PCE Audited'])
            baseline_1_audit_rule = baseline_1_audit_rule.rename(index={'Audit Rule': 0})
            baseline_1_audit_rule = baseline_1_audit_rule.rename(columns={'Defined Value Online Change': 'Defined Value Online Change - Audit Rule',
                                                                              'Defined Value Service Impacting': 'Defined Value Service Impacting - Audit Rule',
                                                                              'PCE Audited Online Change': 'PCE Audited Online Change - Audit Rule',
                                                                              'PCE Enforced Online Change': 'PCE Enforced Online Change - Audit Rule'})

            # Defined but not PCE Audited
            baseline_1_defined_but_not_pce_audited = baseline_1_summary.iloc[[3]].copy()
            baseline_1_defined_but_not_pce_audited = baseline_1_defined_but_not_pce_audited.drop(columns = ['Parameters in PBL','Defined Value','PCE Audited','PCE Audited Online Change','PCE Enforced Online Change'])
            baseline_1_defined_but_not_pce_audited = baseline_1_defined_but_not_pce_audited.rename(index={'Defined but not PCE Audited': 0})
            baseline_1_defined_but_not_pce_audited = baseline_1_defined_but_not_pce_audited.rename(columns={'Defined Value Online Change': 'Defined Value Online Change - Defined but not PCE Audited',
                                                                              'Defined Value Service Impacting': 'Defined Value Service Impacting - Defined but not PCE Audited'})

            # Combined the dataframes into one row
            baseline_1_row = pd.concat([baseline_1_key, baseline_1_totals_p1, baseline_1_totals_p2,
                                        baseline_1_single_value, baseline_1_pce_enforced_online_count_per_category_per_df['% PCE Enforced Online vs Defined Value - Single Value'],
                                        baseline_1_range_of_values, baseline_1_pce_enforced_online_count_per_category_per_df['% PCE Enforced Online vs Defined Value - Range of Values'],
                                        baseline_1_audit_rule, baseline_1_pce_enforced_online_count_per_category_per_df['% PCE Enforced Online vs Defined Value - Audit Rule'],
                                        baseline_1_defined_but_not_pce_audited], axis=1)

            if first_run_flag == True:
                baseline_1_output = baseline_1_row
                first_run_flag = False
            else:
                baseline_1_output = baseline_1_output.append(baseline_1_row)

            ### Export
            if 'y' in detailed_export:
                with pd.ExcelWriter(
                        'Details - ' + vendor + ' ' + tech + ' - ' + date_1_str + ' - ' + current_date_time_str + '.xlsx') as writer:
                    baseline_1_summary.to_excel(writer, sheet_name='Summary', index=True)
                    baseline_1_working.to_excel(writer, sheet_name='Working Table', index=False)

        # If file_ could be split but does not contain 'Baseline' then do not process the file
        else:
            print('Skip this file since it is not a baseline: ' + file_)

    # If try of file_ does not contain 'Baseline' then do not process the file
    except:
        print('Skip this file since it is not a baseline: ' + file_)

with pd.ExcelWriter('Parameter Compliance Progression - ' + current_date_time_str + '.xlsx') as writer:
    baseline_1_output.to_excel(writer, sheet_name='Main', index = False)

#with pd.ExcelWriter(baseline_1_filename + ' Test.xlsx') as writer:
#    test1.to_excel(writer, sheet_name='test1', index=True)
#    test2.to_excel(writer, sheet_name='test2', index=True)
#    test3.to_excel(writer, sheet_name='test3', index=True)
#    test4.to_excel(writer, sheet_name='test4', index=True)

print('Analysis Complete')