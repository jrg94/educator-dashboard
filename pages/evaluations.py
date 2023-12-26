from io import StringIO

import dash
import pandas as pd
from dash import Input, Output, callback, dcc, html

from core.data import load_sei_comments_data, load_sei_data
from core.utils import create_sei_comment_fig, create_sei_fig

dash.register_page(__name__, path='/evaluations')


@callback(
    Output("sei-stats", "figure"),
    Input("sei-data", "data")
)
def render_sei_stats_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_sei_fig(df)


@callback(
    Output("sei-comments", "figure"),
    Input("sei-comments-data", "data")
)
def render_sei_comments_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_sei_comment_fig(df)


layout = html.Div(
    [
        html.H1('Student Evaluation of Instruction'),
        dcc.Markdown(
            '''
            Each semester, the university asks students to fill out a survey about the instruction for the course.
            These data are anonymized and provided as averages for each question. Here is the breakdown of my scores
            against the scores for various cohorts including my department, my college, and my university. In general,
            I outperform all three cohorts, but I'm noticing a downward trend in course organization. For context,
            I taught CSE 1223 in the Fall of 2018 and the Spring of 2019. I've been teaching CSE 2221 ever since, with
            a year gap for research during Autumn 2020 and Spring 2021. **TODO**: the plot should clearly show the
            gap in teaching. 
            '''
        ),
        dcc.Graph(id="sei-stats"),
        html.P(
            """
            Also, as a qualitative researcher, I find the comments themselves to be more meaningful.
            Therefore, here's a plot of the most frequent terms in my SEI comments. 
            """
        ),
        dcc.Graph(id="sei-comments", className="max-window"),
        load_sei_data(),
        load_sei_comments_data()
    ]
)
