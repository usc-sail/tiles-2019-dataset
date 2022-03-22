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
import csv

# date_time format
date_time_format = '%Y-%m-%dT%H:%M:%S.%f'
date_format = '%Y-%m-%d'


pt = pytz.timezone('US/Pacific')


def make_dir(data_path):
    if os.path.exists(data_path) is False:
        os.mkdir(data_path)


def check_data_valid(data_time, start_date, end_date, start_skip_date, end_skip_date):
    cond1 = (pd.to_datetime(data_time) - start_date).total_seconds() >= 0
    cond2 = (end_date - pd.to_datetime(data_time)).total_seconds() >= 0
    if cond1 and cond2:
        if start_skip_date != '':
            cond3 = (pd.to_datetime(data_time) - start_skip_date).total_seconds() >= 0
            cond4 = (end_skip_date - pd.to_datetime(data_time)).total_seconds() >= 0
            if cond3 == True and cond4 == True:
                return False
            else:
                return True
        else:
            return True
    else:
        return False


def check_micu_data_valid(data_time, start_date1, end_date1, start_date2, end_date2):
    cond1 = (pd.to_datetime(data_time) - pd.to_datetime(start_date1)).total_seconds() >= 0
    cond2 = (pd.to_datetime(end_date1) - pd.to_datetime(data_time)).total_seconds() >= 0

    cond3 = False
    cond4 = False
    if start_date2 != 'nan':
        cond3 = (pd.to_datetime(data_time) - pd.to_datetime(start_date2)).total_seconds() >= 0
        cond4 = (pd.to_datetime(end_date2) - pd.to_datetime(data_time)).total_seconds() >= 0

    if (cond1 and cond2) or (cond3 and cond4):
        return True
    else:
        return False


if __name__ == '__main__':
    # Read data root path
    delevery_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, 'delivery_data'))
    setup_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, 'setup_data'))
    participant_info_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, 'participant-info'))
    saving_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, 'tiles-phase2-opendataset'))

    hash_df = pd.read_csv('hashed_phase2_minews.csv')
    study_period = pd.read_csv(os.path.join(participant_info_path, 'study-periods.csv'), index_col=0)

    # participant_list = os.listdir(os.path.join(delevery_root_path, 'Phase2'))
    participant_list = list(study_period.index)
    participant_list.sort()

    micu_df = pd.read_csv(os.path.join(participant_info_path, 'p2_micuschedules_public_5.21.csv'), index_col=0)
    micu_df = micu_df.dropna(subset=['MICU Start Date 1'])

    for participant_id in participant_list:

        id = participant_id[:8]
        if os.path.exists(os.path.join(delevery_root_path, 'Phase2', id, 'AtomProximity', id + '_AtomEddyStone.csv')) is False:
            continue

        eddy_df = pd.read_csv(os.path.join(delevery_root_path, 'Phase2', id, 'AtomProximity', id + '_AtomEddyStone.csv'))
        eddy_df = eddy_df.sort_index()

        # read start and end time for the study
        start_date = pd.to_datetime(study_period.loc[participant_id, 'start_date'])
        end_date = pd.to_datetime(study_period.loc[participant_id, 'end_date']) + timedelta(days=1)
        start_skip_date, end_skip_date = '', ''
        if len(str(study_period.loc[participant_id, 'start_skip_date'])) != 3:
            start_skip_date = pd.to_datetime(study_period.loc[participant_id, 'start_skip_date'])
            end_skip_date = pd.to_datetime(study_period.loc[participant_id, 'end_skip_date']) + timedelta(days=1)

        make_dir(os.path.join(saving_path, 'atomproximity'))
        make_dir(os.path.join(saving_path, 'atomproximity', 'eddystone'))
        save_root_path = os.path.join(saving_path, 'atomproximity', 'eddystone')

        micu_start1 = pd.to_datetime(micu_df.loc[participant_id, 'MICU Start Date 1']).strftime(date_time_format)[:-3]
        micu_end1 = pd.to_datetime(micu_df.loc[participant_id, 'MICU End Date 1']).strftime(date_time_format)[:-3]

        micu_start2 = str(micu_df.loc[participant_id, 'MICU Start Date 2'])
        micu_end2 = str(micu_df.loc[participant_id, 'MICU End Date 2'])

        if str(micu_start2) == 'nan':
            micu_end1 = (pd.to_datetime(micu_start1) + timedelta(days=21)).strftime(date_time_format)[:-3]
        else:
            number_of_days1 = int((pd.to_datetime(micu_end1) - pd.to_datetime(micu_start1)).total_seconds() / (24 * 3600)) + 1
            left_days = 21 - number_of_days1
            if left_days:
                micu_end2 = (pd.to_datetime(micu_start2) + timedelta(days=left_days)).strftime(date_time_format)[:-3]
            else:
                micu_end1 = (pd.to_datetime(micu_start1) + timedelta(days=21)).strftime(date_time_format)[:-3]
                micu_start2, micu_end2 = 'nan', 'nan'

        with open(os.path.join(save_root_path, participant_id + '.csv'), 'w') as csv_output:
            csv_writer = csv.writer(csv_output, delimiter=',')
            csv_writer.writerow(["timeStamp", "eddystoneDirectory", 'rssi'])

            for i, index in enumerate(list(eddy_df.index)):
                tmp_row_df = eddy_df.iloc[i, :]

                if check_micu_data_valid(tmp_row_df['timestamp'][:-5], micu_start1, micu_end1, micu_start2, micu_end2) == False:
                    print('Skip %s' % (tmp_row_df['timestamp']))
                else:
                    directory_str = tmp_row_df['eddystoneDirectory']
                    if 'lounge' in directory_str:
                        directory_str = directory_str.split(':lounge:')[0] + ':' + directory_str.split(':lounge:')[1]

                    hashed_str = hash_df.loc[hash_df['eddystone_directory'] == directory_str]['hashed'].values[0]
                    csv_writer.writerow([tmp_row_df['timestamp'], hashed_str, tmp_row_df['rssi']])
                    if i % 1000 == 0:
                        print('process %s, index at %.2f %%' % (id, i / len(eddy_df) * 100))

        final_df = pd.read_csv(os.path.join(saving_path, 'atomproximity', 'eddystone', participant_id + '.csv'))
        final_df.to_csv(os.path.join(saving_path, 'atomproximity', 'eddystone', participant_id + '.csv.gz'), index=False, compression='gzip')
        os.remove(os.path.join(saving_path, 'atomproximity', 'eddystone', participant_id + '.csv'))

