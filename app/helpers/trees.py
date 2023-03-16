"""
Helpers that build tree and query it
"""
from app.helpers.helpers import adjust_aggregation_code, get_variables, get_children_codes, \
    state_aggregation, state_children_codes
from config import settings


def fetch_branch(tree, key, value):
    """
    Find key - value pair in the tree
    """
    if tree.get(key) == value:
        return tree
    for child in tree['children']:
        match = fetch_branch(child, key, value)
        if match is not None:
            return match


def write_into(tree, key, value, data):
    """
    Return the tree with data written in the given node
    """
    if tree.get(key) == value:
        for data_key in data.keys():
            tree[data_key] = data[data_key]
    else:
        for child in tree['children']:
            write_into(child, key, value, data)
    return tree


def fetch_values_given_key(tree, key, values):
    """
    Return all the values in the tree given a key e.g. 'ind'
    """
    if tree.get(key) is not None:
        values.append(tree[key])
    if len(tree['children']) > 0:
        for child in tree['children']:
            values = fetch_values_given_key(child, key, values)
    return values


def build_tree(data_frame, code, aggregation):
    """
    Return the complete tree with nodes and leaves
    """
    if code is not None:
        aggregation = adjust_aggregation_code(aggregation)
        est, emp, wages = get_variables(data_frame, code, aggregation)
        children_codes = get_children_codes(data_frame, code, aggregation)
        children = []
        if aggregation <= settings.lowest_aggregation:
            for child_code in children_codes:
                children.append(build_tree(data_frame, child_code, aggregation+1))
        return {'ind': code, 'est': est, 'emp': emp, 'wages': wages,'children':children}


def build_state_tree(data_frame, code, aggregation):
    """
    Return the complete tree with nodes and leaves
    """
    if code is not None:
        aggregation = state_aggregation(aggregation)
        est, emp, wages = get_variables(data_frame, code, aggregation)
        children_codes = state_children_codes(data_frame, code, aggregation)
        children = []
        if aggregation <= settings.state_lowest_aggregation:
            for child_code in children_codes:
                children.append(build_state_tree(data_frame, child_code, aggregation+1))
        return {'ind': code, 'est': est, 'emp': emp, 'wages': wages,'children':children}
    return None
