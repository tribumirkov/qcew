"""
Helpers for estimation in general
"""

import re

from app.helpers.trees import fetch_values_given_key, fetch_branch


def get_constraints(tree_code, tree, key, constraints):
    """
    Return all the constraints in a tree
    """
    if len(tree['children'])>0:
        if tree[key] == 0:
            constraint = f"{key}_{tree_code}_{tree['ind']} = "
        else:
            constraint = f"{tree[key]} = "
        for i,child in enumerate(tree['children']):
            if i > 0:
                constraint += ' + '
            if child[key] == 0:
                constraint+= f"{key}_{tree_code}_{child['ind']} "
            else:
                constraint+= f"{child[key]}"
        if key in constraint:
            check = constraint.split(' = ')
            if check[0] != check[1]:
                constraints.append(re.sub(r'\s+', ' ', constraint))
    for child in tree['children']:
        constraints = get_constraints(tree_code, child, key, constraints)
    return constraints


def get_state_county_constraints(state, year, key):
    """
    Return all the constraints in a tree
    """
    state_county_constraints = []
    state_code = list(state[year].keys())[0]
    county_codes = list(state[year].keys())[1:]
    state_inds = fetch_values_given_key(state[year][state_code], 'ind', [])
    for state_ind in state_inds:
        state_node = fetch_branch(state[year][state_code], 'ind', state_ind)
        if state_node[key] == 0:
            state_county_constraint = f"{key}_{state_code}_{state_ind} = "
        else:
            state_county_constraint = f"{state_node[key]} = "
        for county_code in county_codes:
            county_node = fetch_branch(state[year][county_code], 'ind', state_ind)
            if county_node is not None:
                if county_node[key] == 0:
                    state_county_constraint += f" + {key}_{county_code}_{state_ind}"
                else:
                    state_county_constraint += f" + {county_node[key]}"
        if f'{key}_' in state_county_constraint:
            state_county_constraints.append(
                re.sub(r'\s+', ' ', state_county_constraint.replace('=  + ','= '))
            )
    return state_county_constraints
