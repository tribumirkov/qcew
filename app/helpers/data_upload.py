from config import settings


def get_table_given_code(industry_code):
    """
    Return the appropriate Postgres table given the length of the industry code
    """
    if len(industry_code) == 2:
        return settings.table_2_digits
    if len(industry_code) == 3:
        return settings.table_3_digits
    if len(industry_code) == 4:
        return settings.table_4_digits
    if len(industry_code) == 5:
        return settings.table_5_digits
    if len(industry_code) == 6:
        return settings.table_6_digits
    raise NameError('Funny length of the industry code.')

