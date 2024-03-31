from io import StringIO

import dash
import pandas as pd
from dash import Input, Output, callback, dcc, html

from core.constants import *
from core.data import *
from core.utils import *

dash.register_page(
    __name__,
    path='/evaluation',
    name="Evaluation",
    title="The Education Dashboard: Evaluation"
)


@callback(
    Output(ID_SEI_OVERVIEW_FIG, "figure"),
    Input(ID_SEI_DATA, "data")
)
def render_sei_stats_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_sei_fig(df)


@callback(
    Output(ID_SEI_COMMENTS_FIG, "figure"),
    Input(ID_SEI_COMMENTS_DATA, "data")
)
def render_sei_comments_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_sei_comment_fig(df)


@callback(
    Output(ID_EVAL_COURSE_CONTENT_FIG, "figure"),
    Input(ID_COURSE_EVAL_DATA, "data")
)
def render_course_content_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_course_eval_fig(df, "Course content", SCALE_LIKERT)


@callback(
    Output(ID_EVAL_SKILL_FIG, "figure"),
    Input(ID_COURSE_EVAL_DATA, "data")
)
def render_skill_and_responsiveness_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_course_eval_fig(df, "Skill and responsiveness", SCALE_LIKERT)


@callback(
    Output(ID_EVAL_CONTRIBUTION_FIG, "figure"),
    Input(ID_COURSE_EVAL_DATA, "data")
)
def render_course_content_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_course_eval_fig(
        df,
        "Contribution to learning",
        SCALE_LIKERT_ALT
    )


layout = html.Div([
    html.H1("Teaching Evaluation"),
    html.P(
        """
        As an educator, I spend a lot of time assessing my students. 
        Periodically, I give my students a chance to evaluate me. This page is 
        reserved for all of the data related to student evaluations of me.
        """
    ),
    html.H2("Student Evaluations of Instruction"),
    dcc.Markdown(
        """
        Each semester, the university asks students to fill out a survey about 
        the instruction for the course. These data are anonymized and provided 
        as averages for each question. Here is the breakdown of my scores 
        against the scores for various cohorts including my department, my 
        college, and my university. In general, I outperform all three cohorts, 
        but I'm noticing a downward trend in course organization. For context,
        I taught CSE 1223 in the Fall of 2018 and the Spring of 2019. I've been 
        teaching CSE 2221 ever since, with a year gap for research during Autumn 
        2020 and Spring 2021. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_SEI_OVERVIEW_FIG, className=CSS_FULL_SCREEN_FIG)],
        type="graph"
    ),
    html.P(
        """
        Also, as a qualitative researcher, I find the comments themselves to be 
        more meaningful. Therefore, here's a plot of the most frequent terms in 
        my SEI comments. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_SEI_COMMENTS_FIG, className=CSS_FULL_SCREEN_FIG)],
        type="graph"
    ),
    html.H2("Course Evaluation Survey Data"),
    dcc.Markdown(
        """
        At the end of each semester, I ask students to give me feedback on the 
        course. These data are collected through a Google Form. Questions are 
        broken down into different areas which include feedback on course 
        content, my skill and responsiveness, and the course's contribution to 
        learning. **Note**: future work is being done to ensure the following 
        plots feature review counts as seen in the assignment survey data. 
        """
    ),
    html.H3('Course Content'),
    html.P(
        """
        One way the course was evaluated was by asking students to rate their 
        satisfaction with the course content. In short, there are four questions 
        that I ask that cover topics that range from learning objectives to
        organization. Generally, the students that choose to fill out the course 
        survey seem to be satisfied with the course content. For example, at 
        this time, there have been no "strongly disagree" responses. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_EVAL_COURSE_CONTENT_FIG)],
        type="graph"
    ),
    html.H3("Skill and Responsiveness of the Instructor"),
    html.P(
        """
        Another way the course was evaluated was by asking students to rate 
        their satisfaction with the instructor, me. This time around, I ask six 
        questions which range from satisfaction with time usage to satisfaction
        with grading. Again, students are generally happy with my instruction. 
        In fact, they're often more happy with my instruction than the course 
        content itself. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_EVAL_SKILL_FIG, className=CSS_FULL_SCREEN_FIG)],
        type="graph"
    ),
    html.H3("Contribution to Learning"),
    dcc.Markdown(
        """
        Yet another way the course was evaluated was by asking students how much 
        they felt the course contributed to their learning. In this section of 
        the survey, I ask students four questions that attempt to chart how much
        students felt they learned over the course of the semester. In general, 
        students believe they learned a great deal, with most students reporting 
        only a fair amount of knowledge coming into the course and a very good
        amount of knowledge at the end of the course. 
        """
    ),
    # TODO: I should add a plot showing the scores for all four questions with an additional
    # plot showing the trajectory of learning over the semester.
    dcc.Loading(
        [dcc.Graph(id=ID_EVAL_CONTRIBUTION_FIG)],
        type="graph"
    ),
    load_sei_data(),
    load_sei_comments_data(),
    load_course_eval_data()
])
