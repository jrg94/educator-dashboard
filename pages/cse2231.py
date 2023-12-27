from io import StringIO
import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd

from core.data import load_cse2231_grade_data
from core.utils import create_grades_fig, create_assignment_fig

dash.register_page(
    __name__,
    path='/cse2231',
    name="CSE2231",
    title="The Education Dashboard: CSE 2231"
)


@callback(
    Output("cse2231-grade-overview", "figure"),
    Input("cse2231-grade-data", "data")
)
def render_grade_overview_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_grades_fig(df)


@callback(
    Output("cse2231-homework-calculations", "figure"),
    Input("cse2231-grade-data", "data")
)
def render_homework_calculations_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_assignment_fig(df, "Homework", 2)


@callback(
    Output("cse2231-project-calculations", "figure"),
    Input("cse2231-grade-data", "data")
)
def render_project_calculations_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_assignment_fig(df, "Project", 10)


layout = html.Div([
    html.H1('CSE 2231: Software 2'),
    dcc.Graph(id="cse2231-grade-overview"),
    html.H2(children='Homework Assignments'),
    dcc.Graph(id="cse2231-homework-calculations"),
    html.H2("Project Assignments"),
    dcc.Graph(id="cse2231-project-calculations"),
    load_cse2231_grade_data()
])
