from io import StringIO

import dash
import pandas as pd
from dash import Input, Output, callback, dcc, html

from core.constants import *
from core.data import *
from core.utils import *

dash.register_page(
    __name__,
    path='/cse2231',
    name="CSE2231",
    title="The Education Dashboard: CSE 2231"
)


@callback(
    Output(ID_CSE_2231_GRADES_OVERVIEW_FIG, "figure"),
    Input(ID_CSE_2231_GRADE_DATA, "data")
)
def render_grade_overview_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_grades_fig(df)


@callback(
    Output(ID_CSE_2231_HOMEWORK_GRADES_FIG, "figure"),
    Input(ID_CSE_2231_GRADE_DATA, "data")
)
def render_homework_calculations_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_assignment_fig(df, "Homework", 2)


@callback(
    Output(ID_CSE_2231_PROJECT_GRADES_FIG, "figure"),
    Input(ID_CSE_2231_GRADE_DATA, "data")
)
def render_project_calculations_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_assignment_fig(df, "Project", 10)


@callback(
    Output(ID_CSE_2231_EXAM_GRADES_FIG, "figure"),
    Input(ID_CSE_2231_GRADE_DATA, "data")
)
def render_exam_calculations_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_assignment_fig(df, "Exam", 100)


@callback(
    Output(ID_CSE_2231_HOMEWORK_TIME_FIG, "figure"),
    Input(ID_ASSIGNMENT_SURVEY_DATA, "data")
)
def render_homework_time_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_time_fig(df, assignment="Homework", course=FILTER_SOFTWARE_2)


@callback(
    Output(ID_CSE_2231_MISSING_HOMEWORKS_FIG, "figure"),
    Input(ID_CSE_2231_GRADE_DATA, "data")
)
def render_missing_homeworks_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_missing_assignment_fig(df, "Homework")


@callback(
    Output(ID_CSE_2231_PROJECT_TIME_FIG, "figure"),
    Input(ID_ASSIGNMENT_SURVEY_DATA, "data")
)
def render_project_time_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_time_fig(df, assignment="Project", course=FILTER_SOFTWARE_2)


layout = html.Div([
    html.H1("CSE 2231: Software 2"),
    html.P(
        """
        Software 2 (CSE 2231) is a course I started teaching in Autumn 2023. 
        Naturally, it follows software 1, which is a course I previously taught.
        The purpose of software 2 is to flip the script on students. No longer
        are they clients of APIs (though, there is no avoiding this). Instead,
        they're implementors of those APIs. 
        """
    ),
    html.P(
        """
        In terms of course design, software 2 is broken into three main parts.
        During the first part of the course, students focus on what we call
        "kernel implementations", which are the students' first exposure to
        developing APIs. I've deemed the second part of the course "compilers"
        because it focuses primarily on compiler techniques like parsing, 
        tokenizing, and code generation. Finally, the last third of the course
        focuses on what we call "loose ends", which is basically everything
        we've neglected over the course sequence about the Java language. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_GRADES_OVERVIEW_FIG)],
        type="graph"
    ),
    html.H2("Homework Assignments"),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_HOMEWORK_GRADES_FIG)],
        type="graph"
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_MISSING_HOMEWORKS_FIG)],
        type="graph"
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_HOMEWORK_TIME_FIG)],
        type="graph"
    ),
    html.H2("Project Assignments"),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_PROJECT_GRADES_FIG)],
        type="graph"
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_PROJECT_TIME_FIG)],
        type="graph"
    ),
    html.H2("Exams"),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_EXAM_GRADES_FIG)],
        type="graph"
    ),
    load_cse2231_grade_data(),
    load_assignment_survey_data()
])
