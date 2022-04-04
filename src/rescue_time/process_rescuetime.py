from __future__ import print_function

import os, sys, argparse
import pandas as pd
from datetime import timedelta
import pdb

# date_time format
date_time_format = '%Y-%m-%dT%H:%M:%S.%f'
date_format = '%Y-%m-%d'


def make_dir(data_path):
    if os.path.exists(data_path) is False:
        os.mkdir(data_path)
        

if __name__ == '__main__':

    # Read participant list
    root_dir = '/media/data/tiles-processed/tiles-phase2-delivery'
    output_dir = '/media/data/tiles-opendataset/tiles-phase2-opendataset'
    
    data_path = os.path.abspath(os.path.join(root_dir, 'tiles-phase2-evidation', 'rescuetime', 'rescuetime.csv'))
    setup_root_path = os.path.abspath(os.path.join(root_dir, 'setup_data'))
    participant_info_path = os.path.abspath(os.path.join(root_dir, 'participant-info'))

    # save path
    rescue_df = pd.read_csv(data_path)
    study_period = pd.read_csv(os.path.join(participant_info_path, 'study-periods.csv'), index_col=0)

    # participant id list
    participant_id_list = list(set(rescue_df['participant_id']))
    participant_id_list.sort()

    micu_df = pd.read_csv(os.path.join(participant_info_path, 'p2_micuschedules_public_5.21.csv'), index_col=0)
    micu_df = micu_df.dropna(subset=['MICU Start Date 1'])

    # iterate valid participant
    for id in participant_id_list:

        print('process: %s' % (id))
        raw_data_df = rescue_df.loc[rescue_df['participant_id'] == id]

        # iterate rows
        data_df = pd.DataFrame()
        for i in range(len(raw_data_df)):
            participant_row_df = raw_data_df.iloc[i, :]
            start_str = pd.to_datetime(participant_row_df['ts']).strftime(date_time_format)[:-3]

            # read row data
            row_df = pd.DataFrame(index=[start_str])
            row_df['TimestampStart'] = start_str
            row_df['TimestampEnd'] = (pd.to_datetime(participant_row_df['ts']) + timedelta(minutes=5)).strftime(date_time_format)[:-3]
            row_df['SecondsOnPhone'] = participant_row_df['seconds_on_device']
            data_df = pd.concat([data_df, row_df])

        data_df = data_df.sort_values(by=['TimestampStart'])
        
        # extract data in the study period and save
        micu_start1 = pd.to_datetime(micu_df.loc[id, 'MICU Start Date 1']).strftime(date_time_format)[:-3]
        micu_end1 = (pd.to_datetime(micu_df.loc[id, 'MICU End Date 1'])+timedelta(days=1, minutes=-1)).strftime(date_time_format)[:-3]

        micu_start2 = str(micu_df.loc[id, 'MICU Start Date 2'])
        micu_end2 = str(micu_df.loc[id, 'MICU End Date 2'])
        
        if str(micu_start2) == 'nan':
            save_df = data_df[data_df['TimestampStart'].between(micu_start1, micu_end1, inclusive=False)]
        else:
            micu_start2 = pd.to_datetime(micu_start2).strftime(date_time_format)[:-3]
            number_of_days1 = int((pd.to_datetime(micu_end1) - pd.to_datetime(micu_start1)).total_seconds() / (24 * 3600)) + 1
            left_days = 21 - number_of_days1
            if left_days:
                micu_end2 = (pd.to_datetime(micu_start2) + timedelta(days=left_days, minutes=-1)).strftime(date_time_format)[:-3]
                tmp_df1 = data_df[data_df['TimestampStart'].between(micu_start1, micu_end1, inclusive=False)]
                tmp_df2 = data_df[data_df['TimestampStart'].between(micu_start2, micu_end2, inclusive=False)]
                save_df = tmp_df1.append(tmp_df2)
            else:
                save_df = data_df[data_df['TimestampStart'].between(micu_start1, micu_end1, inclusive=False)]
        make_dir(os.path.join(output_dir))
        make_dir(os.path.join(output_dir, 'rescuetime'))
        save_df.to_csv(os.path.join(output_dir, 'rescuetime', id + '.csv.gz'), index=False, compression='gzip')


