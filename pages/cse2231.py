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
    html.P(
        """
        As far as assessments are concerned, the expectations are roughly the
        same as software 1. In general, students complete a series of homework
        assignments, projects, and exams. However, there are significantly
        more homework assignments in software 2 at a total of 37. There is
        also one fewer project at a total of 10, which are completed in pairs.
        Meanwhile, exam expectations are exactly the same. In addition, students
        are assessed on participation. Here's a quick overview of the
        averages for each of these assessments.
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_GRADES_OVERVIEW_FIG)],
        type="graph"
    ),
    html.P(
        """
        As always, the remainder of this page is dedicated to a breakdown
        of each assessment type. 
        """
    ),
    html.H2("Homework Assignments"),
    html.P(
        """
        Once again, students are tasked with completing 37 written homework
        assignments in software 2. Given a 15-week semester, this means students
        are asked to complete roughly 2 written assignments a week. However, to
        be completely fair, most homework assignments are just lab preparation,
        so all of the work is closely connected to the day-to-day. 
        """
    ),
    html.P(
        """
        Like software 1, homework assignments take up just 6% of the overall
        grade. In addition, each assignment is graded on completion, not 
        correctness. Therefore, as you'll see below, the median homework grades
        are high (i.e., over half the class always submits something). 
        Therefore, the average grade is usually most influence by lack of 
        submissions (as you'll see later).
        """
    ),  
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_HOMEWORK_GRADES_FIG)],
        type="graph"
    ),
    html.P(
        """
        As promised, here's what the trend of missing assignments looks like for
        homeworks. One that jumps right out at me is homework 27! I wonder
        what's going on there. I can't say for certain why this assignment is
        most often forgotten, but it's one of two assignments due the same day 
        as a project. The other assignment being homework 14, which doesn't look
        out of the ordinary. Homework 27 is, however, the fourth homework of
        the week, which might play a role in its lack of submissions. 
        """
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
