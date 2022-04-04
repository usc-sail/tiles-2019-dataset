from __future__ import print_function

import os
import pandas as pd
import pdb
from datetime import timedelta

date_time_format = '%Y-%m-%dT%H:%M:%S.%f'
date_format = '%Y-%m-%d'


save_type_dict = {'_Fitbit_SleepData': 'sleep-data',
                  '_Fitbit_StepCount': 'step-count',
                  '_Fitbit_HeartRate': 'heart-rate',
                  '_Fitbit_Sync': 'sync',
                  '_Fitbit_DailySummary': 'daily-summary',
                  '_Fitbit_SleepMetadata': 'sleep-metadata'}


def make_dir(data_path):
    if os.path.exists(data_path) is False:
        os.mkdir(data_path)

def extract_fitbit_data(id, delevery_root_path, output_path, by_col, file_type):
    if os.path.exists(os.path.join(delevery_root_path, id[:8], 'Fitbit', id[:8] + file_type + '.csv')) is True:
        data_df = pd.read_csv(os.path.join(delevery_root_path, id[:8], 'Fitbit', id[:8] + file_type + '.csv'))
        data_df = data_df.sort_values(by=[by_col])
        
        micu_start1 = pd.to_datetime(micu_df.loc[id, 'MICU Start Date 1']).strftime(date_time_format)[:-3]
        micu_end1 = (pd.to_datetime(micu_df.loc[id, 'MICU End Date 1'])+timedelta(days=1, minutes=-1)).strftime(date_time_format)[:-3]
        micu_start2 = str(micu_df.loc[id, 'MICU Start Date 2'])
        
        if str(micu_start2) == 'nan':
            save_df = data_df[data_df[by_col].between(micu_start1, micu_end1, inclusive=False)]
        else:
            micu_start2 = pd.to_datetime(micu_start2).strftime(date_time_format)[:-3]
            number_of_days1 = int((pd.to_datetime(micu_end1) - pd.to_datetime(micu_start1)).total_seconds() / (24 * 3600)) + 1
            left_days = 21 - number_of_days1
            if left_days:
                micu_end2 = (pd.to_datetime(micu_start2) + timedelta(days=left_days, minutes=-1)).strftime(date_time_format)[:-3]
                tmp_df1 = data_df[data_df[by_col].between(micu_start1, micu_end1, inclusive=False)]
                tmp_df2 = data_df[data_df[by_col].between(micu_start2, micu_end2, inclusive=False)]
                save_df = tmp_df1.append(tmp_df2)
            else:
                save_df = data_df[data_df[by_col].between(micu_start1, micu_end1, inclusive=False)]
        
        make_dir(os.path.join(output_path))
        make_dir(os.path.join(output_path, 'fitbit'))
        make_dir(os.path.join(output_path, 'fitbit', save_type_dict[file_type]))
        
        print('save %s, %s' % (id[:8], id[:8] + file_type + '.csv'))
        save_df.to_csv(os.path.join(output_path, 'fitbit', save_type_dict[file_type], id + '.csv.gz'), index=False, compression='gzip')


if __name__ == '__main__':

    # Read data root path
    root_dir = '/media/data/tiles-processed/tiles-phase2-delivery'
    output_dir = '/media/data/tiles-opendataset/tiles-phase2-opendataset'
    delevery_root_path = os.path.abspath(os.path.join(root_dir, 'delivery_data'))
    setup_root_path = os.path.abspath(os.path.join(root_dir, 'setup_data'))
    participant_info_path = os.path.abspath(os.path.join(root_dir, 'participant-info'))

    # read study period data frame
    study_period = pd.read_csv(os.path.join(participant_info_path, 'study-periods.csv'), index_col=0)
    micu_df = pd.read_csv(os.path.join(participant_info_path, 'p2_micuschedules_public_5.21.csv'), index_col=0)
    micu_df = micu_df.dropna(subset=['MICU Start Date 1'])

    participant_list = list(study_period.index)
    participant_list.sort()
    
    for id in participant_list:

        # sleep data
        extract_fitbit_data(id, delevery_root_path, output_dir, by_col='dateTime', file_type='_Fitbit_SleepData')

        # sleep meta
        extract_fitbit_data(id, delevery_root_path, output_dir, by_col='startTime', file_type='_Fitbit_SleepMetadata')

        # sync
        extract_fitbit_data(id, delevery_root_path, output_dir, by_col='sync_time', file_type='_Fitbit_Sync')

        # heart rate
        extract_fitbit_data(id, delevery_root_path, output_dir, by_col='Timestamp', file_type='_Fitbit_HeartRate')

        # step count
        extract_fitbit_data(id, delevery_root_path, output_dir, by_col='Timestamp', file_type='_Fitbit_StepCount')

        # summary
        extract_fitbit_data(id, delevery_root_path, output_dir, by_col='Timestamp', file_type='_Fitbit_DailySummary')
