import json

from app.helpers.trees import fetch_values_given_key, fetch_branch
from app.helpers.data_upload import get_table_given_code
from app.helpers.db import update_db

state_abbreviation = '56'

with open(f'{state_abbreviation}000.json', 'r', encoding='utf-8') as fp:
    state = json.load(fp)

years = list(state.keys())

for year in years:
    print(f'*** year {year} ***')
    for county_code in list(state[year].keys())[1:]:
        industry_codes = fetch_values_given_key(state[year][county_code], 'ind', [])
        for i_code,industry_code in enumerate(industry_codes):
            industry_code = industry_code.replace('_','')
            print(f'county_code {county_code}, naics_code {industry_code}')
            industry = fetch_branch(state[year][county_code], 'ind', industry_code)
            estabs_est = industry['est']
            if industry.get('emp_lp') is not None:
                emp_est = industry['emp_lp']
            else:
                emp_est = industry['emp']
            table_name = get_table_given_code(industry_code)
            area_fips = int(county_code)
            success, details = update_db(
                f'''UPDATE community_data.{table_name}
                    SET estabs_est = {estabs_est}, emp_est = {emp_est}
                    WHERE own_code = 5
                    AND area_fips = {area_fips}
                    AND "year" = {year}
                    AND naics_code = {industry_code}
                '''
            )
            if not success:
                print(f'year {year}, county_code {county_code}, naics_code {industry_code} was not uploaded')

