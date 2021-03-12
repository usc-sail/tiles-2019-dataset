from process_census_data import *

from pathlib import Path

class Deaths(Processor):
    def __init__(self, unit, shift):
        self.column = 'Deceased Date/Time'
        self.location = 'Unit'
        self.counter = "deaths"
        self.unit = unit
        self.shift = shift

def get_deaths(file: Path, unit, cutoffs=[6, 17], freq="1H", shift=True) -> pd.DataFrame:
    df = pd.read_excel(file)
    deaths = Deaths(unit, shift)
    df = deaths.count(df, cutoffs=cutoffs, freq=freq)
    df.insert(1, 'unit', unit)
    df.set_index('datetime', inplace=True)
    dst = df.index < pd.to_datetime("2019-11-03T01:00:00", infer_datetime_format=True) # DST backward for 2019
    df.index = df.index.tz_localize(tz="America/Los_Angeles", ambiguous=dst, nonexistent="shift_forward") # Shifting forward for 2020
    return df

def merge_census_and_deaths(census: pd.DataFrame, deaths: pd.DataFrame):
    return census.merge(deaths, on='datetime', how='outer').fillna(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract census data from files (LAC Data/'4A 4B Admission Report 20XX.xlsx').")
    parser.add_argument('path', type=Path, help='Path to folder containing 2019 and 2020 files.')
    parser.add_argument('--save', type=Path, default=Path(__file__).parent.absolute(), help='Path to save files.')
    parser.add_argument('--cutoffs', nargs='*', type=int, default=[6, 17], help='List of cutoff times to compute census separated by spaces in 24-hour format, e.g. 6 17.')
    parser.add_argument('--freq', type=str, default="1H", help='Resampling frequency of time series (default, 1H. To resample every 30min, use "30T".')
    parser.add_argument('--shift', default=False, action='store_true', help='Shift admissions and discharges to count by the of time window instead of the beginning.')

    args = parser.parse_args()

    census = {}
    deaths = {}
    df = {}
    for unit in ['4A', '4B']:
        census[unit] = process_unit(unit, args, save=False)
        deaths[unit] = get_deaths(args.path/'Mortalities_LAC+USC.xlsx', unit, cutoffs=args.cutoffs, freq=args.freq, shift=args.shift)
        df[unit] = census[unit].merge(deaths[unit], on=['datetime', 'unit'], how='outer').fillna(0)

    results = pd.concat([df[unit] for unit in ['4A', '4B']]).reset_index()
    results = results.sort_values(by=['datetime', 'unit']).set_index('datetime')

    freqs = {"1H": "1hour", "30T": "30min"}
    results.to_csv(args.save/f"LAC+USC_census_and_mortalities_{freqs[args.freq]}.csv", index=True)