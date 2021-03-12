from process_census_data import *

from pathlib import Path

class Deaths(Processor):
    def __init__(self, unit, shift):
        self.column = 'Deceased Date/Time'
        self.location = 'Unit'
        self.counter = "deaths"
        self.unit = unit
        self.shift = shift

def get_deaths(file: Path, unit, cutoffs=[6, 17], shift=True) -> pd.DataFrame:
    df = pd.read_excel(file)
    deaths = Deaths(unit, shift)
    df = deaths.count(df, cutoffs=cutoffs)
    df.insert(1, 'unit', unit)
    return df

def merge_census_and_deaths(census: pd.DataFrame, deaths: pd.DataFrame):
    return census.merge(deaths, on='datetime', how='outer').fillna(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract census data from files (LAC Data/'4A 4B Admission Report 20XX.xlsx').")
    parser.add_argument('path', type=Path, help='Path to folder containing 2019 and 2020 files.')
    parser.add_argument('--save', type=Path, default=Path(__file__).parent.absolute(), help='Path to save files.')
    parser.add_argument('--cutoffs', nargs='*', type=int, default=[6, 17], help='List of cutoff times to compute census separated by spaces in 24-hour format, e.g. 6 17.')
    parser.add_argument('--shift', default=False, action='store_true', help='Shift admissions and discharges to count by the of time window instead of the beginning.')

    args = parser.parse_args()

    census = {}
    deaths = {}
    df = {}
    for unit in ['4A', '4B']:
        census[unit] = process_unit(unit, args, save=False)
        deaths[unit] = get_deaths(args.path/'Mortalities_LAC+USC.xlsx', unit, cutoffs=args.cutoffs, shift=args.shift)
        df[unit] = census[unit].merge(deaths[unit], on=['datetime', 'unit'], how='outer').fillna(0)

    results = pd.concat([df[unit] for unit in ['4A', '4B']]).sort_values(['datetime', 'unit']).set_index('datetime')
    results.index = results.index.tz_localize(tz="America/Los_Angeles", ambiguous="infer", nonexistent="shift_forward")

    results.to_csv(args.save/"LAC+USC_census_and_mortalities.csv", index=True)