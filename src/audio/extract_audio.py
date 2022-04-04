from __future__ import print_function
from fileinput import filename

import os
import pandas as pd
import pdb
from datetime import timedelta
import datetime
import shutil

date_time_format = '%Y-%m-%dT%H:%M:%S.%f'
date_format = '%Y-%m-%d'


def make_dir(data_path):
    if os.path.exists(data_path) is False:
        os.mkdir(data_path)
        

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
    root_dir = '/media/data/tiles-processed/tiles-phase2-delivery'
    output_dir = '/media/data/tiles-opendataset/tiles-phase2-opendataset-audio'
    delevery_root_path = os.path.abspath(os.path.join(root_dir, 'delivery_data'))
    setup_root_path = os.path.abspath(os.path.join(root_dir, 'setup_data'))
    participant_info_path = os.path.abspath(os.path.join(root_dir, 'participant-info'))

    # read study period data frame
    consent_df = pd.read_csv(os.path.join(root_dir, 'consents.csv'), index_col=5)
    study_period = pd.read_csv(os.path.join(participant_info_path, 'study-periods.csv'), index_col=0)
    micu_df = pd.read_csv(os.path.join(participant_info_path, 'p2_micuschedules_public_5.21.csv'), index_col=0)
    micu_df = micu_df.dropna(subset=['MICU Start Date 1'])

    participant_list = list(study_period.index)
    consent_participant_list = list(consent_df.index)
    participant_list.sort()
    
    for id in participant_list:
        
        # if no consent
        if id not in consent_participant_list:
            continue
        print(id, consent_df.loc[id, 'audio_future'])
        if consent_df.loc[id, 'audio_future'] is False:
            continue
        
        # if no data, continue
        audio_data_path = os.path.join('/media/data/tiles-processed', 'tiles-phase2-opendataset-audio', 'raw-features', id)
        if os.path.exists(audio_data_path) is False:
            continue
        
        micu_start1 = pd.to_datetime(micu_df.loc[id, 'MICU Start Date 1']).strftime(date_time_format)[:-3]
        micu_start2 = str(micu_df.loc[id, 'MICU Start Date 2'])

        micu_end1 = (pd.to_datetime(micu_df.loc[id, 'MICU End Date 1'])+timedelta(days=1, minutes=-1)).strftime(date_time_format)[:-3]
        micu_end2 = str(micu_df.loc[id, 'MICU End Date 2'])

        if str(micu_start2) != 'nan':
            number_of_days1 = int((pd.to_datetime(micu_end1) - pd.to_datetime(micu_start1)).total_seconds() / (24 * 3600)) + 1
            left_days = 21 - number_of_days1
            if left_days:
                micu_end2 = (pd.to_datetime(micu_start2) + timedelta(days=left_days, minutes=-1)).strftime(date_time_format)[:-3]
            else:
                micu_start2, micu_end2 = 'nan', 'nan'
        
        file_list = os.listdir(audio_data_path)
        for file_name in file_list:
            if 'RawFeatures' in file_name:
                continue
            time = file_name.split('.csv.gz')[0]
            date_time = datetime.datetime.fromtimestamp(int(time)).strftime(date_format)
            if check_micu_data_valid(date_time, micu_start1, micu_end1, micu_start2, micu_end2) is True:
                make_dir(output_dir)
                make_dir(os.path.join(output_dir, 'raw-features'))
                make_dir(os.path.join(output_dir, 'raw-features', id))
                
                make_dir(os.path.join(output_dir, 'fg-predictions'))
                make_dir(os.path.join(output_dir, 'fg-predictions', id))
                
                # original file
                raw_feature_output_path = os.path.join(output_dir, 'raw-features', id, file_name)
                fg_predictions_output_path = os.path.join(output_dir, 'fg-predictions', id, str(time)+'.npy')
                
                # output file
                raw_feature_path = os.path.join(audio_data_path, file_name)
                fg_predictions_path = os.path.join('/media/data/tiles-processed', 'tiles-phase2-opendataset-audio', 'fg-predictions', id, str(time)+'.npy')
                shutil.copy(raw_feature_path, raw_feature_output_path)
                if os.path.exists(fg_predictions_path) is True:
                    shutil.copy(fg_predictions_path, fg_predictions_output_path)
                print('save %s, %s' % (id, raw_feature_path))
        