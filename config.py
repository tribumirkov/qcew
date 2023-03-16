"""
Configuration file
"""
import json

import numpy as np

from pydantic import BaseSettings

class Settings(BaseSettings):

    qcew_api_url = 'http://data.bls.gov/cew/data/api'

    ownership_code = 5

    root_aggregation = 71
    highest_aggregation = 74
    lowest_aggregation = 78
    max_digits_of_naics = 6

    state_root_aggregation = 51
    state_highest_aggregation = 54
    state_lowest_aggregation = 58

    max_batch_constraints = 10

    string_connecting_codes = '_'

    period = '4'
    years = [str(year) for year in list(range(2014,2021+1))]
    establishments = 'qtrly_estabs'#'annual_avg_estabs'
    employment = 'month3_emplvl' #'annual_avg_emplvl'
    wages = 'total_qtrly_wages' #'total_annual_wages'

    employment_abbreviation = 'emp'
    wages_abbreviation = 'wages'
    number_of_digits_json = 4

    table_2_digits = 'employment_industry_qcew_2digit'
    table_3_digits = 'employment_industry_qcew_3digit'
    table_4_digits = 'employment_industry_qcew_4digit'
    table_5_digits = 'employment_industry_qcew_5digit'
    table_6_digits = 'employment_industry_qcew'

settings = Settings()


class NpEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        return super(NpEncoder, self).default(o)
