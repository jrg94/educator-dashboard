import pandas as pd
from dash import Input, Output, callback, dcc, html

from constants import project_review_col, homework_review_col
from utils import create_time_fig

@callback(
    Output("project-time", "figure"),
    Input("assignment-survey", "data")
)
def render_project_time_figure(jsonified_data):
    df = pd.read_json(jsonified_data)
    return create_time_fig(df, col=project_review_col)

@callback(
    Output("homework-time", "figure"),
    Input("assignment-survey", "data")
)
def render_homework_time_figure(jsonified_data):
    df = pd.read_json(jsonified_data)
    return create_time_fig(df, col=homework_review_col)
