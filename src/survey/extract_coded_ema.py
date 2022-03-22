from __future__ import print_function

import os
import sys

###########################################################
# Change to your own library path
###########################################################
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

from dateutil.parser import parse
import pytz

# date_time format
date_time_format = '%Y-%m-%dT%H:%M:%S.%f'
date_format = '%Y-%m-%d'

ema_col = ['id', 'survey_type', 'delivered_ts', 'completed_ts', 'activity', 'location', 'atypical', 'stress',
           'stressor_partner', 'stressor_fam', 'stressor_breakdown', 'stressor_money', 'stressor_selfcare', 'stressor_health',
           'stressor_otherhealth', 'stressor_household', 'stressor_child', 'stressor_discrimination', 'stressor_none',
           'moststressful', 'moststressful_time', 'work_location', 'attend_fidam', 'attend_fidpm', 'attend_hasp',
           'attend_pgy1did', 'attend_pgy2did', 'attend_pgy3did', 'attend_none', 'work_start', 'work_end',
           'jobperformance', 'jobperformance_best', 'jobsatisfaction', 'sleepquant', 'sleepqual', 'alcoholuse',
           'alcohol_total', 'tobaccouse', 'tobacco_total', 'physactivity', 'physactivity_total',
           'workstressor_computer', 'workstressor_patientint', 'workstressor_conflict', 'workstressor_census',
           'workstressor_late', 'workstressor_paged', 'workstressor_supervise', 'workstressor_admin',
           'workstressor_diffcases', 'workstressor_death', 'charting', 'charting_total', 'coworkertrust',
           'work_inperson', 'work_digital', 'support_inperson', 'support_digital', 'socialevents', 'hangouts', 'wellness']


pt = pytz.timezone('US/Pacific')


def make_dir(data_path):
    if os.path.exists(data_path) is False:
        os.mkdir(data_path)


def check_micu_data_valid(data_time, start_date1, end_date1, start_date2, end_date2):
    cond1 = (pd.to_datetime(data_time) - pd.to_datetime(start_date1)).total_seconds() >= 0
    cond2 = (pd.to_datetime(end_date1) + timedelta(days=1) - pd.to_datetime(data_time)).total_seconds() >= 0

    cond3 = False
    cond4 = False
    if start_date2 != 'nan':
        cond3 = (pd.to_datetime(data_time) - pd.to_datetime(start_date2)).total_seconds() >= 0
        cond4 = (pd.to_datetime(end_date2) + timedelta(days=1) - pd.to_datetime(data_time)).total_seconds() >= 0

    if (cond1 and cond2):
        return True
    elif  (cond3 and cond4):
        return True
    else:
        return False


if __name__ == '__main__':

    # Read data root path
    participant_info_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, 'participant-info'))
    saving_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, 'tiles-phase2-opendataset'))

    # id,started_ts,completed_ts,duration,weekcompleted,gender,traininglevel
    # Phase1Training_IGTB.csv

    save_igtb_df = pd.DataFrame()
    study_period = pd.read_csv(os.path.join(participant_info_path, 'study-periods.csv'), index_col=0)
    ema_df = pd.read_csv(os.path.join(saving_path, 'surveys', 'p2_ema_public_5.21.csv'))

    stress_coded_df = pd.read_csv(os.path.join(saving_path, 'surveys', 'MostStressful_SDLS.csv'))
    best_coded_df = pd.read_csv(os.path.join(saving_path, 'surveys', 'PerformBest_SDLS.csv'))
    atypical_coded_df = pd.read_csv(os.path.join(saving_path, 'surveys', 'Atypical_SDLS.csv'))

    participant_list = list(study_period.index)
    participant_list.sort()

    micu_df = pd.read_csv(os.path.join(participant_info_path, 'p2_micuschedules_public_5.21.csv'), index_col=0)
    micu_df = micu_df.dropna(subset=['MICU Start Date 1'])

    final_ema_df = pd.DataFrame()

    for id in participant_list:

        participant_df = ema_df.loc[ema_df['id'] == id]
        micu_start1 = pd.to_datetime(micu_df.loc[id, 'MICU Start Date 1']).strftime(date_time_format)[:-3]
        micu_end1 = pd.to_datetime(micu_df.loc[id, 'MICU End Date 1']).strftime(date_time_format)[:-3]

        micu_start2 = str(micu_df.loc[id, 'MICU Start Date 2'])
        micu_end2 = str(micu_df.loc[id, 'MICU End Date 2'])

        if 'e7dc' in id:
            print()

        if str(micu_start2) != 'nan':

            micu_start2 = pd.to_datetime(micu_start2).strftime(date_time_format)[:-3]
            number_of_days1 = int((pd.to_datetime(micu_end1) - pd.to_datetime(micu_start1)).total_seconds() / (24 * 3600)) + 1
            number_of_days2 = int((pd.to_datetime(micu_end2) - pd.to_datetime(micu_start2)).total_seconds() / (24 * 3600))

            left_days = 21 - number_of_days1
            if left_days:
                micu_end2 = (pd.to_datetime(micu_start2) + timedelta(days=left_days)).strftime(date_time_format)[:-3]
            else:
                micu_end1 = (pd.to_datetime(micu_start1) + timedelta(days=21)).strftime(date_time_format)[:-3]
                micu_start2, micu_end2 = 'nan', 'nan'
        else:
            micu_end1 = (pd.to_datetime(micu_start1) + timedelta(days=21)).strftime(date_time_format)[:-3]


        for i in range(len(participant_df)):
            participant_row_df = participant_df.iloc[i, :]
            if len(participant_row_df['completed_ts']) < 10:
                continue

            completed_str = pd.to_datetime(participant_row_df['completed_ts'][:-6]).strftime(date_time_format)[:-3]
            if participant_row_df['survey_type'] is 'endofweek':
                print()

            if check_micu_data_valid(completed_str, micu_start1, micu_end1, micu_start2, micu_end2) == True:
                participant_row_df = participant_row_df.to_frame().T
                most_stressful = participant_row_df['moststressful'].values[0]
                best_performance = participant_row_df['jobperformance_best'].values[0]
                atypical = participant_row_df['atypical'].values[0]
                index = participant_row_df.index[0]

                tmp_stressful = ''
                if len(most_stressful) != 0:
                    most_stressful_df = stress_coded_df.loc[stress_coded_df['Most stressful event of day'] == most_stressful]
                    if len(most_stressful_df) != 0:
                        if str(most_stressful_df['category 1'].values[0]) != 'nan':
                            tmp_stressful += str(most_stressful_df['category 1'].values[0])
                        if str(most_stressful_df['category 2'].values[0]) != 'nan':
                            tmp_stressful += ';' + str(most_stressful_df['category 2'].values[0])
                        if str(most_stressful_df['category 3'].values[0]) != 'nan':
                            tmp_stressful += ';' + str(most_stressful_df['category 3'].values[0])

                tmp_best = ''
                if len(best_performance) != 0:
                    best_df = best_coded_df.loc[best_coded_df['Aspect of Job Perform Best'] == best_performance]
                    if len(best_df) != 0:
                        if str(best_df['category 1'].values[0]) != 'nan':
                            tmp_best += str(best_df['category 1'].values[0])
                        if str(best_df['category 2'].values[0]) != 'nan':
                            tmp_best += ';' + str(best_df['category 2'].values[0])
                        if str(best_df['category 3'].values[0]) != 'nan':
                            tmp_best += ';' + str(best_df['category 3'].values[0])

                tmp_atypical = ''
                if len(atypical) != 0:
                    atypical_df = atypical_coded_df.loc[atypical_coded_df['Atypical Event (before, or expected)'] == atypical]
                    if len(atypical_df) != 0:
                        if str(atypical_df['category1'].values[0]) != 'nan' and str(atypical_df['category1'].values[0]) != '0':
                            tmp_atypical += str(atypical_df['category1'].values[0])
                        if str(atypical_df['category2'].values[0]) != 'nan' and str(atypical_df['category2'].values[0]) != '0':
                            tmp_atypical += ';' + str(atypical_df['category2'].values[0])
                        if str(atypical_df['category3'].values[0]) != 'nan' and str(atypical_df['category3'].values[0]) != '0':
                            tmp_atypical += ';' + str(atypical_df['category3'].values[0])


                participant_row_df.loc[index, 'moststressful'] = tmp_stressful
                participant_row_df.loc[index, 'jobperformance_best'] = tmp_best
                participant_row_df.loc[index, 'atypical'] = tmp_atypical
                final_ema_df = final_ema_df.append(participant_row_df)

    drop_cols = ['alcoholuse', 'alcohol_total', 'tobaccouse', 'tobacco_total', 'physactivity', 'physactivity_total',
                 'workstressor_computer', 'workstressor_patientint', 'workstressor_conflict', 'workstressor_census',
                 'workstressor_late', 'workstressor_paged', 'workstressor_supervise', 'workstressor_admin',
                 'workstressor_diffcases', 'workstressor_death', 'charting', 'charting_total', 'coworkertrust',
                 'work_inperson', 'work_digital', 'support_inperson', 'support_digital', 'socialevents', 'hangouts', 'wellness']


    # daily_ema_df = final_ema_df.loc[final_ema_df['survey_type'] != 'endofweek']
    daily_ema_df = final_ema_df.drop(columns=drop_cols)
    for daily_index in list(daily_ema_df.index):
        if daily_ema_df.loc[daily_index, 'survey_type'] == 'endofweek':
            daily_ema_df.loc[daily_index, 'survey_type'] = 'endofday'

    tmp_daily_ema_df = daily_ema_df.copy()
    for daily_index in list(tmp_daily_ema_df.index):
        tmp_daily_ema_df.loc[daily_index, 'tmp_date'] = pd.to_datetime(tmp_daily_ema_df.loc[daily_index, 'delivered_ts'][:-6]).strftime(date_time_format)[:-3]
    tmp_daily_ema_df = tmp_daily_ema_df.set_index('tmp_date')

    weekly_ema_df = final_ema_df.loc[final_ema_df['survey_type'] == 'endofweek']
    weekly_ema_df = weekly_ema_df[['id', 'survey_type', 'delivered_ts', 'completed_ts']+drop_cols]

    final_ema_df.to_csv(os.path.join(saving_path, 'surveys', 'ema.csv'), index=False)
    daily_ema_df.to_csv(os.path.join(saving_path, 'surveys', 'daily_ema.csv'), index=False)
    tmp_daily_ema_df.to_csv(os.path.join(saving_path, 'surveys', 'tmp_daily_ema.csv'))
    weekly_ema_df.to_csv(os.path.join(saving_path, 'surveys', 'weekly_ema.csv'), index=False)





