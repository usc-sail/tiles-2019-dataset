import argparse
import pandas as pd

from pathlib import Path

class Processor:
    def __init__(self, column: str, counter: str, unit: str, shift: bool):
        self.column = column
        self.counter = counter
        self.unit = unit
        self.shift=shift

    def count(self, df: pd.DataFrame, cutoffs=[6, 17]) -> pd.DataFrame:
        df = df.loc[df[self.location] == self.unit, :]

        df = pd.DataFrame({'datetime': df[self.column], self.counter: 1}).sort_values(by='datetime')
        df = df.resample('1H', on='datetime').sum()

        start_date = (df.index[0] - pd.Timedelta(days=1)).replace(hour=cutoffs[-1])
        end_date = (df.index[-1] + pd.Timedelta(days=1)).replace(hour=cutoffs[0])
        df = pd.concat([
            pd.DataFrame({'datetime': pd.date_range(start=start_date, end=df.index[0] - pd.Timedelta(hours=1), freq='H'), self.counter: 0}).set_index('datetime'),
            df,
            pd.DataFrame({'datetime': pd.date_range(start=df.index[-1] + pd.Timedelta(hours=1), end=end_date, freq='H'), self.counter: 0}).set_index('datetime'),])
        df['group'] = df.index.hour.isin(cutoffs).cumsum()
        df = df.reset_index().groupby('group').agg({'datetime': 'first', self.counter: 'sum'})
        if self.shift:
            df[self.counter] = df[self.counter].shift(periods=1, fill_value=0)
        return df

class Admissions(Processor):
    def __init__(self, unit, shift):
        self.column = 'ICU_ADMISSION_DATE'
        self.location = 'ICU_LOCATION'
        self.counter = 'admissions'
        self.unit = unit
        self.shift = shift

class Discharges(Processor):
    def __init__(self, unit, shift):
        self.column = 'ICU_END_EFFECTIVE_DATE'
        self.location = 'ICU_LOCATION'
        self.counter = 'discharges'
        self.unit = unit
        self.shift = shift

def get_census(file: Path, unit, cutoffs=[6, 17], shift=True) -> pd.DataFrame:
    df = pd.read_excel(file)
    admissions = Admissions(unit, shift)
    discharges = Discharges(unit, shift)
    df = (admissions.count(df, cutoffs=cutoffs)).merge(discharges.count(df, cutoffs=cutoffs), on='datetime', how='outer').fillna(0)
    df.insert(1, 'unit', unit)
    return df

def merge_censuses(census_2019: pd.DataFrame, census_2020: pd.DataFrame) -> pd.DataFrame:
    df = census_2019.merge(census_2020, on=['datetime', 'unit'], how='outer', suffixes=['_2019', '_2020']).fillna(0)
    df['admissions'] = df['admissions_2019'] + df['admissions_2020']
    df['discharges'] = df['discharges_2019'] + df['discharges_2020']

    return df.loc[:, ['datetime', 'unit', 'admissions', 'discharges']]

def process_census(df: pd.DataFrame) -> pd.DataFrame:
    df['total'] = df['admissions'].cumsum() - df['discharges'].cumsum()
    df['max'] = df['admissions'].cumsum() - df['discharges'].shift(periods=1).fillna(0).cumsum()
    return df

def process_unit(unit, args, save=True):
    census_2019 = get_census(args.path/'4A 4B Admission Report 2019.xlsx', unit, cutoffs=args.cutoffs, shift=args.shift)
    census_2020 = get_census(args.path/'4A 4B Admission Report 2020.xlsx', unit, cutoffs=args.cutoffs, shift=args.shift)

    census = merge_censuses(census_2019, census_2020)
    census = process_census(census)

    census.set_index('datetime', inplace=True)
    census.index = census.index.tz_localize(tz="America/Los_Angeles", ambiguous="infer", nonexistent="shift_forward")

    if save:
        census.to_csv(args.save/f"LAC_unit{unit}_census.csv", index=True)
    else:
        return census

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract census data from files (LAC Data/'4A 4B Admission Report 20XX.xlsx').")
    parser.add_argument('path', type=Path, help='Path to folder containing 2019 and 2020 files.')
    parser.add_argument('--save', type=Path, default=Path(__file__).parent.absolute(), help='Path to save files.')
    parser.add_argument('--cutoffs', nargs='*', type=int, default=[6, 17], help='List of cutoff times to compute census separated by spaces in 24-hour format, e.g. 6 17.')
    parser.add_argument('--shift', default=False, action='store_true', help='Shift admissions and discharges to count by the of time window instead of the beginning.')

    args = parser.parse_args()

    for unit in ['4A', '4B']:
        process_unit(unit, args, save=True)