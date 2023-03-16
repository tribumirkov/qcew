"""
Helpers related to estimation with vectorized constraints
"""
import re

import numpy as np

from app.helpers.data_load_bls import fetch_industry_data, fetch_area_data
from app.helpers.trees import build_state_tree, build_tree
from config import settings


def load_state_data(state_code):
    """
    Load state data from BLS given state code abbreviation (first two numbers)
    """
    print('Loading data from BLS ... ')
    state = {}
    for year in settings.years:
        print(f'*** {year} ***')
        data_frame, _ = fetch_industry_data(year, settings.period, '102')
        county_codes = list(
            np.unique(
                data_frame[data_frame['area_fips'].str.startswith(state_code)]['area_fips']
            )
        )
        counties = {}
        for i_county,county_code in enumerate(county_codes):
            print(f'county: {county_code}')
            data_frame, _ = fetch_area_data(year, settings.period, county_code)
            if i_county == 0:
                county = build_state_tree(data_frame, '10', 51)
            else:
                county = build_tree(data_frame, '10', 71)
            counties[county_code] = county
        state[year] = counties
    return state


def get_array_elements(variables, equation, key, row, constant):
    """
    Return the total number of employment accross counties
    """
    terms = re.findall(fr'({key}_[^ ]*|[+-]?\d+)', equation)
    positions = [
        m.start(0) for m in re.finditer(fr'({key}_[^ ]*|[+-]?\d+)', equation)
    ]
    for term,position in zip(terms, positions):
        if f'{key}_' in term:
            if position < equation.find('='):
                row[variables.index(term)] = 1
            else:
                row[variables.index(term)] = -1
        else:
            if position < equation.find('='):
                constant -= int(term)
            else:
                constant += int(term)
    return row, constant


def vectorize_equations(equations, key):
    """
    Vectorize a list of string equations and return the matrix A and the constant vector b.
    """
    variables = set()
    for equation in equations:
        for var in re.findall(fr"{key}_[^ ]*", equation):
            variables.add(var)
    variables = sorted(list(variables))
    number_of_variables = len(variables)
    number_of_equations = len(equations)
    A = np.empty((number_of_equations, number_of_variables))
    b = np.empty(number_of_equations)
    for i,equation in enumerate(equations):
        row, constant = get_array_elements(variables, equation, key, [0] * number_of_variables, 0)
        A[i,] = row
        b[i] = constant
    return A, b, variables
