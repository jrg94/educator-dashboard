from io import StringIO

import pandas as pd
from constants import homework_review_col, project_review_col
from dash import Input, Output, callback
from utils import (create_emotions_fig, create_rubric_breakdown_fig,
                   create_rubric_overview_fig, create_rubric_scores_fig,
                   create_time_fig)


@callback(
    Output("project-time", "figure"),
    Input("assignment-survey", "data")
)
def render_project_time_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_time_fig(df, col=project_review_col)


@callback(
    Output("homework-time", "figure"),
    Input("assignment-survey", "data")
)
def render_homework_time_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_time_fig(df, col=homework_review_col)


@callback(
    Output("emotions", "figure"),
    Input("assignment-survey", "data")
)
def render_emotions_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_emotions_fig(df, col=homework_review_col)


@callback(
    Output("rubric-overview", "figure"),
    Input("assignment-survey", "data")
)
def render_rubric_overview_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_rubric_overview_fig(df)


@callback(
    Output("rubric-breakdown", "figure"),
    Input("assignment-survey", "data")
)
def render_rubric_breakdown_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_rubric_breakdown_fig(df)


@callback(
    Output("rubric-scores", "figure"),
    Input("assignment-survey", "data")
)
def render_rubric_scores_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_rubric_scores_fig(df)
