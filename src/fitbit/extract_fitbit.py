from __future__ import print_function

import os
import pandas as pd
from datetime import timedelta

date_time_format = '%Y-%m-%dT%H:%M:%S.%f'
date_format = '%Y-%m-%d'


def make_dir(data_path):
	if os.path.exists(data_path) is False:
		os.mkdir(data_path)


def extract_fitbit_data(id, start_date, end_date, start_skip_date, end_skip_date, delevery_root_path, output_path, by_col, file_type):
	if os.path.exists(os.path.join(delevery_root_path, 'Phase2', id[:8], 'Fitbit', id[:8] + file_type + '.csv')) is True:

		data_df = pd.read_csv(os.path.join(delevery_root_path, 'Phase2', id[:8], 'Fitbit', id[:8] + file_type + '.csv'))
		data_df = data_df.sort_values(by=[by_col])
		if start_skip_date == '':
			final_df = data_df[data_df[by_col].between(start_date, end_date, inclusive=False)]
		else:
			tmp_df1 = data_df[data_df[by_col].between(start_date, start_skip_date, inclusive=False)]
			tmp_df2 = data_df[data_df[by_col].between(end_skip_date, end_date, inclusive=False)]
			final_df = tmp_df1.append(tmp_df2)

		make_dir(os.path.join(output_path,))
		make_dir(os.path.join(output_path, 'Phase2'))
		make_dir(os.path.join(output_path, 'Phase2', id[:8]))
		make_dir(os.path.join(output_path, 'Phase2', id[:8], 'Fitbit'))

		print('save %s, %s' % (id[:8], id[:8] + file_type + '.csv'))
		final_df.to_csv(os.path.join(output_path, 'Phase2', id[:8], 'Fitbit', id[:8] + file_type + '.csv'), index=False)


if __name__ == '__main__':

	# Read data root path
	delevery_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, 'delivery_data'))
	setup_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, 'setup_data'))
	participant_info_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, 'participant-info'))

	study_period = pd.read_csv(os.path.join(participant_info_path, 'study-periods.csv'), index_col=0)
	participant_list = list(study_period.index)
	participant_list.sort()

	for id in participant_list[:]:

		# read start and end time for the study
		start_date = pd.to_datetime(study_period.loc[id, 'start_date']).strftime(date_time_format)[:-3]
		end_date = (pd.to_datetime(study_period.loc[id, 'end_date']) + timedelta(days=1)).strftime(date_time_format)[:-3]
		start_skip_date, end_skip_date = '', ''
		if len(str(study_period.loc[id, 'start_skip_date'])) != 3:
			start_skip_date = (pd.to_datetime(study_period.loc[id, 'start_skip_date']) - timedelta(seconds=1)).strftime(date_time_format)[:-3]
			end_skip_date = (pd.to_datetime(study_period.loc[id, 'end_skip_date']) + timedelta(days=1)).strftime(date_time_format)[:-3]

		output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, 'delivery_data_utc'))

		# sleep data
		extract_fitbit_data(id, start_date, end_date, start_skip_date, end_skip_date, delevery_root_path, output_path, by_col='dateTime', file_type='_Fitbit_SleepData')

		# sleep meta
		extract_fitbit_data(id, start_date, end_date, start_skip_date, end_skip_date, delevery_root_path, output_path, by_col='startTime', file_type='_Fitbit_SleepMetaData')

		# sync
		extract_fitbit_data(id, start_date, end_date, start_skip_date, end_skip_date, delevery_root_path, output_path, by_col='sync_time', file_type='_Fitbit_Sync')

		# heart rate
		extract_fitbit_data(id, start_date, end_date, start_skip_date, end_skip_date, delevery_root_path, output_path, by_col='Timestamp', file_type='_Fitbit_HeartRate')

		# step count
		extract_fitbit_data(id, start_date, end_date, start_skip_date, end_skip_date, delevery_root_path, output_path, by_col='Timestamp', file_type='_Fitbit_StepCount')

		# summary
		extract_fitbit_data(id, start_date, end_date, start_skip_date, end_skip_date, delevery_root_path, output_path, by_col='Timestamp', file_type='_Fitbit_DailySummary')
