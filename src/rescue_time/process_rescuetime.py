from __future__ import print_function

import os, sys, argparse
import pandas as pd
from datetime import timedelta

###########################################################
# Add package path
###########################################################
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'util')))

import load_basic_data



if __name__ == '__main__':

    # Read data root path
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", required=False, help="Path to the folder containing data")
    parser.add_argument("--participant_info_path", required=False, help="Path to the folder containing participant info")
    parser.add_argument("--output_path", required=False, help="Path to output folder")
    args = parser.parse_args()

    # Read participant list
    data_path = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, 'tiles-phase2-evidation', 'rescuetime', 'rescuetime.csv') if args.data_path is None else args.data_path
    participant_info_path = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, 'participant-info') if args.participant_info_path is None else args.participant_info_path
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, 'tiles-phase2-opendataset')) if args.output_path is None else args.output_path

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
        data_df = rescue_df.loc[rescue_df['participant_id'] == id]

        # read start and end time for the study
        study_period_dict = load_basic_data.read_study_period(id, study_period)

        # iterate rows
        save_df = pd.DataFrame()
        for i in range(len(data_df)):
            participant_row_df = data_df.iloc[i, :]
            start_str = pd.to_datetime(participant_row_df['ts']).strftime(load_basic_data.date_time_format)[:-3]

            # read row data
            row_df = pd.DataFrame(index=[start_str])
            row_df['TimestampStart'] = start_str
            row_df['TimestampEnd'] = (pd.to_datetime(participant_row_df['ts']) + timedelta(minutes=5)).strftime(load_basic_data.date_time_format)[:-3]
            row_df['SecondsOnPhone'] = participant_row_df['seconds_on_device']

            save_df = pd.concat([save_df, row_df])

        # extract data in the study period and save
        save_df = load_basic_data.extract_data(save_df, study_period_dict, by_col='TimestampStart')

        micu_start1 = pd.to_datetime(micu_df.loc[id, 'MICU Start Date 1']).strftime(load_basic_data.date_time_format)[:-3]
        micu_end1 = pd.to_datetime(micu_df.loc[id, 'MICU End Date 1']).strftime(load_basic_data.date_time_format)[:-3]

        micu_start2 = str(micu_df.loc[id, 'MICU Start Date 2'])
        micu_end2 = str(micu_df.loc[id, 'MICU End Date 2'])

        if str(micu_start2) == 'nan':
            micu_end1 = (pd.to_datetime(micu_start1) + timedelta(days=21)).strftime(load_basic_data.date_time_format)[:-3]
            final_micu_df = save_df[save_df['TimestampStart'].between(micu_start1, micu_end1, inclusive=False)]
        else:
            micu_start2 = pd.to_datetime(micu_start2).strftime(load_basic_data.date_time_format)[:-3]
            micu_end2 = pd.to_datetime(micu_end2).strftime(load_basic_data.date_time_format)[:-3]

            number_of_days1 = int((pd.to_datetime(micu_end1) - pd.to_datetime(micu_start1)).total_seconds() / (24 * 3600)) + 1
            number_of_days2 = int((pd.to_datetime(micu_end2) - pd.to_datetime(micu_start2)).total_seconds() / (24 * 3600))

            left_days = 21 - number_of_days1
            if left_days:
                micu_end2 = (pd.to_datetime(micu_start2) + timedelta(days=left_days)).strftime(load_basic_data.date_time_format)[:-3]
                tmp_df1 = save_df[save_df['TimestampStart'].between(micu_start1, micu_end1, inclusive=False)]
                tmp_df2 = save_df[save_df['TimestampStart'].between(micu_start2, micu_end2, inclusive=False)]
                final_micu_df = tmp_df1.append(tmp_df2)
            else:
                micu_end1 = (pd.to_datetime(micu_start1) + timedelta(days=21)).strftime(load_basic_data.date_time_format)[:-3]
                final_micu_df = save_df[save_df['TimestampStart'].between(micu_start1, micu_end1, inclusive=False)]

        load_basic_data.make_dir(output_path)
        load_basic_data.make_dir(os.path.join(output_path, 'rescuetime'))
        final_micu_df.to_csv(os.path.join(output_path, 'rescuetime', id + '.csv.gz'), index=False, compression='gzip')



