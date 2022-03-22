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
import csv

from dateutil.parser import parse
import pytz

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

    hash_df = pd.read_csv('hashed_phase2.csv')
    study_period = pd.read_csv(os.path.join(participant_info_path, 'study-periods.csv'), index_col=0)
    mm_df = pd.read_csv(os.path.join(participant_info_path, 'minimally-involved-participant-info.csv'), index_col=0)
    participant_info_df = pd.read_csv(os.path.join(participant_info_path, 'participant-info.csv'), index_col=0)

    # participant_list = os.listdir(os.path.join(delevery_root_path, 'Phase2'))
    participant_list = list(study_period.index)
    participant_list.sort()

    participant_dict = {}
    for id in list(participant_info_df.index):
        participant_dict[id[:8]] = id
    for id in list(mm_df.index):
        participant_dict[id[:8]] = id

    micu_df = pd.read_csv(os.path.join(participant_info_path, 'p2_micuschedules_public_5.21.csv'), index_col=0)
    micu_df = micu_df.dropna(subset=['MICU Start Date 1'])

    for participant_id in participant_list[:]:

        id = participant_id[:8]
        if 'DS' in id:
            continue

        if os.path.exists(os.path.join(delevery_root_path, 'Phase2', id, 'AtomProximity', id + '_AtomMinew.csv')) is False:
            continue

        # read start and end time for the study
        start_date = pd.to_datetime(study_period.loc[participant_id, 'start_date'])
        end_date = pd.to_datetime(study_period.loc[participant_id, 'end_date']) + timedelta(days=1)

        start_skip_date, end_skip_date = '', ''
        if len(str(study_period.loc[participant_id, 'start_skip_date'])) != 3:
            start_skip_date = pd.to_datetime(study_period.loc[participant_id, 'start_skip_date'])
            end_skip_date = pd.to_datetime(study_period.loc[participant_id, 'end_skip_date']) + timedelta(days=1)

        # start_date1
        minew_df = pd.read_csv(os.path.join(delevery_root_path, 'Phase2', id, 'AtomProximity', id + '_AtomMinew.csv'))
        minew_df = minew_df.sort_index()

        if 'Timestamp' in list(minew_df.columns):
            timestamp_col = 'Timestamp'
        else:
            timestamp_col = 'timestamp'

        make_dir(os.path.join(saving_path, 'atomproximity'))
        make_dir(os.path.join(saving_path, 'atomproximity', 'interaction'))

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

        with open(os.path.join(saving_path, 'atomproximity', 'interaction', participant_id + '.csv'), 'w') as csv_output:
            csv_writer = csv.writer(csv_output, delimiter=',')
            csv_writer.writerow(["timeStamp", "participantId", 'rssi'])

            print('process %s' % (participant_id))
            for i in range(len(minew_df.index)):

                tmp_row_df = minew_df.iloc[i, :]

                # check data in the study period or not
                if check_micu_data_valid(tmp_row_df[timestamp_col][:-5], micu_start1, micu_end1, micu_start2, micu_end2) == False:
                    print('Skip %s' % (tmp_row_df[timestamp_col]))
                else:
                    participantId = tmp_row_df['participantId']
                    if participantId in participant_dict:
                        csv_writer.writerow([tmp_row_df[timestamp_col], participant_dict[participantId], tmp_row_df['rssi']])
                        if i % 1000 == 0:
                            print('process %s, index at %.2f %%' % (id, i / len(minew_df) * 100))

        final_df = pd.read_csv(os.path.join(saving_path, 'atomproximity', 'interaction', participant_id + '.csv'))
        final_df.to_csv(os.path.join(saving_path, 'atomproximity', 'interaction', participant_id + '.csv.gz'), index=False, compression='gzip')
        os.remove(os.path.join(saving_path, 'atomproximity', 'interaction', participant_id + '.csv'))







