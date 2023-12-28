from io import StringIO

import dash
import pandas as pd
from dash import Input, Output, callback, dcc, html

from core.constants import FILTER_SOFTWARE_2
from core.data import load_assignment_survey_data, load_cse2231_grade_data
from core.utils import (create_assignment_fig, create_grades_fig,
                        create_missing_assignment_fig, create_time_fig)

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


@callback(
    Output("cse2231-exams-calculations", "figure"),
    Input("cse2231-grade-data", "data")
)
def render_exam_calculations_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_assignment_fig(df, "Exam", 100)


@callback(
    Output("cse2231-homework-time", "figure"),
    Input("assignment-survey-data", "data")
)
def render_homework_time_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_time_fig(df, assignment="Homework", course=FILTER_SOFTWARE_2)


@callback(
    Output("cse2231-project-time", "figure"),
    Input("assignment-survey-data", "data")
)
def render_project_time_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_time_fig(df, assignment="Project", course=FILTER_SOFTWARE_2)


@callback(
    Output("cse2231-missing-homeworks", "figure"),
    Input("cse2231-grade-data", "data")
)
def render_missing_homeworks_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_missing_assignment_fig(df, "Homework")


layout = html.Div([
    html.H1('CSE 2231: Software 2'),
    dcc.Graph(id="cse2231-grade-overview"),
    html.H2(children='Homework Assignments'),
    dcc.Graph(id="cse2231-homework-calculations"),
    dcc.Graph(id="cse2231-missing-homeworks"),
    dcc.Graph(id="cse2231-homework-time"),
    html.H2("Project Assignments"),
    dcc.Graph(id="cse2231-project-calculations"),
    dcc.Graph(id="cse2231-project-time"),
    html.H2(children='Exams'),
    dcc.Graph(id="cse2231-exams-calculations"),
    load_cse2231_grade_data(),
    load_assignment_survey_data()
])
