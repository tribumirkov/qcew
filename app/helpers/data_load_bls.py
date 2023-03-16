"""
Helpers for loading data from BLS
"""
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

from config import settings


def fetch_area_data(year, quarter, area):
    """
    Return a pandas table from BLS given year, quarter (a for year), and area code
    """
    url_path = f'{settings.qcew_api_url}/{year}/{quarter}/area/{area}.csv'
    data_frame = pd.read_csv(url_path)
    if is_numeric_dtype(data_frame['industry_code']):
        data_frame['industry_code'] = data_frame['industry_code'].astype("string")
    else:
        data_frame['industry_code'] = data_frame['industry_code'].str.replace(
            '-',
            settings.string_connecting_codes
        )
    return data_frame, url_path


def fetch_industry_data(year, quarter, industry):
    """
    Return a pandas table from BLS given year, quarter (a for year), and NAICS code
    """
    url_path = f'{settings.qcew_api_url}/{year}/{quarter}/industry/{industry}.csv'
    return pd.read_csv(url_path), url_path
