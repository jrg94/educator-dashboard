import pandas as pd

from core.constants import *

# TODO: attempt to remove this as the semesters CSV provides the order we need
def semester_order(data: pd.DataFrame) -> dict:
    """
    Returns a sorted list of semesters in the expected order 
    (e.g., [Autumn 2018, Spring 2019, Autumn 2019, Spring 2020, ...]).

    :param data: the DataFrame provided by the user with an assumed Semester 
    Year column
    :return: a list of sorted semesters
    """
    SEASON_SORT_ORDER = ["Spring", "Summer", "Autumn"]
    min_year = data[COLUMN_SEMESTER_YEAR].min()
    max_year = data[COLUMN_SEMESTER_YEAR].max()
    semesters = {}
    order = 1
    for year in range(min_year, max_year + 1):
        for season in SEASON_SORT_ORDER:
            semesters[f"{season} {year}"] = order
            order += 1
    return semesters
