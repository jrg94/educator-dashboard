import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from core.constants import *


def semester_order(data: pd.DataFrame) -> dict:
    """
    Returns a sorted list of semesters in the expected order 
    (e.g., [Autumn 2018, Spring 2019, Autumn 2019, Spring 2020, ...]).

    :param data: the DataFrame provided by the user with an assumed Semester column
    :return: a list of sorted semesters
    """
    SEASON_SORT_ORDER = ["Spring", "Summer", "Autumn"]
    min_year = data["Year"].min()
    max_year = data["Year"].max()
    semesters = {}
    order = 1
    for year in range(min_year, max_year + 1):
        for season in SEASON_SORT_ORDER:
            semesters[f"{season} {year}"] = order
            order += 1
    return semesters


def create_course_eval_fig(course_eval_data, question, axes_labels):
    colors = dict(zip(axes_labels, COLORS_SATISFACTION.values()))
    question_data = course_eval_data.melt(
        id_vars=[item for item in course_eval_data.columns if question not in item],
        var_name="Question",
        value_name="Response"
    )
    question_data = question_data[question_data["Response"].notna()]
    question_fig = go.Figure(layout=dict(template='plotly'))
    question_fig = px.histogram(
        question_data,
        x="Response",
        color="Response",
        facet_col="Question",
        facet_col_wrap=2,
        category_orders=dict(Response=axes_labels),
        text_auto=True,
        title=f"{question} by Subquestion".title(),
        color_discrete_map=colors
    )
    question_fig.for_each_annotation(lambda a: a.update(
        text=a.text[a.text.find("[")+1:a.text.find("]")]))
    return question_fig
