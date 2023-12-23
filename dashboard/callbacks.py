import pandas as pd
from dash import Input, Output, callback, dcc, html

from dashboard import create_time_fig
from constants import project_review_col

@callback(
    Output("project-time", "figure"),
    Input("assignment-survey", "data")
)
def render_project_time_figure(jsonified_data):
    df = pd.read_json(jsonified_data)
    return create_time_fig(df, col=project_review_col)
