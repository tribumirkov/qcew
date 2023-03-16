"""
Endpoints for estimation using Q4 data and vectorization of constraints
"""
import json

import cvxpy as cp
import numpy as np

from app.helpers.estimation import get_constraints, get_state_county_constraints
from app.helpers.helpers import extract_codes
from app.helpers.trees import fetch_branch, write_into
from app.statevectorized.helpers import load_state_data, vectorize_equations
from config import settings, NpEncoder

ststes = [
    '56', '50', '11', '02', '38', '46', '10', '44', '30', '23', 
    '33', '15', '54', '16', '31', '35', '20', '28', '05', '32', 
    '19', '49', '09', '40', '41', '21', '22', '01', '45', '27',
    '08', '55', '24', '29', '18', '25', '47', '04', '53', '51',
    '34', '26', '37', '13', '39', '17', '42', '36', '12', '48',
    '06'
]

for state_abbreviation in ststes:

    print(f'Running the state {state_abbreviation}000')
    state = load_state_data(state_abbreviation)

    print('Estimating undisclosed data... ')
    for year in settings.years:
        print(f'*** {year} ***')
        print('Loading area constraints... ')
        area_constraints = []
        for code in list(state[year].keys()):
            area_constraints = get_constraints(code, state[year][code], 'emp', area_constraints)
        print('Loading state-level constraints... ')
        state_level_constraints = get_state_county_constraints(state, year, 'emp')

        constraints = area_constraints + state_level_constraints
        print('Vectorizing constraints... ')
        A, b, variables = vectorize_equations(constraints, 'emp')

        x = cp.Variable(len(variables))
        s = cp.Variable(b.shape[0])
        print('Estimating LP... ')
        objective = cp.Minimize(np.ones(len(variables)) @ x)
        numerical_constraints = [A @ x + s == b, x >= 0, s>=0]
        problem = cp.Problem(objective, numerical_constraints)
        problem.solve(solver=cp.ECOS, verbose = True, max_iters = 1000000)

        for var,x_j in zip(variables, x):
            county_code, ind = extract_codes(var)
            county = state[year][county_code]
            branch = fetch_branch(county, 'ind', ind)
            county = write_into(
                county,
                'ind',
                branch['ind'],
                {'emp_lp': max(round(x_j.value, settings.number_of_digits_json), 0)}
                )
            state[year][county_code] = county

    with open(f'{state_abbreviation}000.json', 'w', encoding='utf-8') as fp:
        json.dump(state, fp, cls=NpEncoder)
