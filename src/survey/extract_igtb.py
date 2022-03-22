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


pt = pytz.timezone('US/Pacific')


def make_dir(data_path):
	if os.path.exists(data_path) is False:
		os.mkdir(data_path)


if __name__ == '__main__':
	# Read data root path
	delevery_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, 'delivery_data'))
	igtb_df = pd.read_csv(os.path.join(delevery_root_path, 'p2_baseline_processed_11.2020.csv'), index_col=0)
	# id,started_ts,completed_ts,duration,weekcompleted,gender,traininglevel
	# Phase1Training_IGTB.csv

	save_igtb_df = pd.DataFrame()

	id_list = list(igtb_df.index)
	id_list.sort()

	for id in id_list:

		row_df = pd.DataFrame(index=[id])
		row_df['id'] = id[:8]
		row_df['gender'] = igtb_df.loc[id, 'gender']
		row_df['traininglevel'] = igtb_df.loc[id, 'traininglevel']

		save_igtb_df = pd.concat([save_igtb_df, row_df])

	save_igtb_df.to_csv(os.path.join(delevery_root_path, 'tiles-phase2-gpr', 'Phase2', 'Phase2_IGTB.csv'), index=False)





