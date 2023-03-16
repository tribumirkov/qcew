"""
General helpers called from anywhere
"""
import numpy as np

from config import settings


def adjust_aggregation_code(aggregation):
    """
    Return aggregation code that skips 72, and 73
    """
    aggregation_levels = list(
        range(
            settings.highest_aggregation, settings.lowest_aggregation + 1
        )
    )
    aggregation_levels.append(settings.root_aggregation)
    if aggregation in aggregation_levels:
        return aggregation
    if settings.root_aggregation < aggregation < settings.highest_aggregation:
        return settings.highest_aggregation
    raise Exception('Aggregation level code unknown.')


def get_variables(data_frame, code, aggregation):
    """
    Return variables of interest given industry code
    """
    ownership_code = settings.ownership_code
    where = (data_frame['industry_code']==code) & \
            (data_frame['agglvl_code']==aggregation) & \
            (data_frame['own_code']==ownership_code)
    est = data_frame[where][f'{settings.establishments}'].values[0]
    emp = data_frame[where][f'{settings.employment}'].values[0]
    wages = data_frame[where][f'{settings.wages}'].values[0]
    return est, emp, wages


def get_children_codes(data_frame, code, aggregation):
    """
    Return a list of children codes
    """
    if settings.string_connecting_codes in code:
        search_it = tuple([str(number) for number in range(int(code[0:2]), int(code[-2:]) + 1)])
    else:
        search_it = code
    if search_it == '10':
        where = (data_frame['agglvl_code']==settings.highest_aggregation) & \
                (data_frame['own_code']==settings.ownership_code)
    else:
        where = (data_frame['industry_code'].str.startswith(search_it)) & \
                (data_frame['own_code']==settings.ownership_code) & \
                (data_frame['agglvl_code']==aggregation+1)
    return sorted(np.unique(data_frame['industry_code'][where].values))


def state_aggregation(aggregation):
    """
    Return aggregation code that skips 52, and 53
    """
    aggregation_levels = list(
        range(
            settings.state_highest_aggregation, settings.state_lowest_aggregation + 1
        )
    )
    aggregation_levels.append(settings.state_root_aggregation)
    if aggregation in aggregation_levels:
        return aggregation
    if settings.state_root_aggregation < aggregation < settings.state_highest_aggregation:
        return settings.state_highest_aggregation
    raise Exception('Aggregation level code unknown.')


def state_children_codes(data_frame, code, aggregation):
    """
    Return a list of children codes
    """
    if settings.string_connecting_codes in code:
        search_it = tuple(str(number) for number in range(int(code[0:2]), int(code[-2:]) + 1))
    else:
        search_it = code
    if search_it == '10':
        where = (data_frame['agglvl_code']==settings.state_highest_aggregation) & \
                (data_frame['own_code']==settings.ownership_code)
    else:
        where = (data_frame['industry_code'].str.startswith(search_it)) & \
                (data_frame['own_code']==settings.ownership_code) & \
                (data_frame['agglvl_code']==aggregation+1)
    return sorted(np.unique(data_frame['industry_code'][where].values))


def extract_codes(variable_name):
    """
    Return county code and industry code from a variable's name
    """
    positions = [i for i, letter in enumerate(variable_name) if letter == '_']
    return variable_name[positions[0]+1:positions[1]], variable_name[positions[1]+1:].strip()
