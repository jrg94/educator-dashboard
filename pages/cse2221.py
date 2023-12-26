from io import StringIO

import dash
import pandas as pd
from dash import Input, Output, callback, dcc, html

from core.constants import homework_review_col, project_review_col
from core.data import load_assignment_survey_data
from core.utils import (create_emotions_fig, create_rubric_breakdown_fig,
                        create_rubric_overview_fig, create_rubric_scores_fig,
                        create_time_fig)

dash.register_page(__name__, path='/cse2221')


@callback(
    Output("project-time", "figure"),
    Input("assignment-survey-data", "data")
)
def render_project_time_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_time_fig(df, col=project_review_col)


@callback(
    Output("homework-time", "figure"),
    Input("assignment-survey-data", "data")
)
def render_homework_time_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_time_fig(df, col=homework_review_col)


@callback(
    Output("emotions", "figure"),
    Input("assignment-survey-data", "data")
)
def render_emotions_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_emotions_fig(df, col=homework_review_col)


@callback(
    Output("rubric-overview", "figure"),
    Input("assignment-survey-data", "data")
)
def render_rubric_overview_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_rubric_overview_fig(df)


@callback(
    Output("rubric-breakdown", "figure"),
    Input("assignment-survey-data", "data")
)
def render_rubric_breakdown_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_rubric_breakdown_fig(df)


@callback(
    Output("rubric-scores", "figure"),
    Input("assignment-survey-data", "data")
)
def render_rubric_scores_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_rubric_scores_fig(df)


layout = html.Div([
    html.H1("CSE 2221: Software 1"),
    html.H2("Assignment Survey Data"),
    html.P(
        '''
        Throughout the course, I asked students to give me feedback on the assignments. Originally,
        these data were collected through a Carmen quiz (Autumn 2021). However, I found the Carmen 
        quiz format to be limiting, so later iterations of the quiz were administered through a Google
        Form. 
        '''
    ),
    html.H3('Time Spent Working on Projects'),
    html.P(
        '''
        One of the questions I asked my students was how long they spent on each project. Based on the responses,
        I found that students spent between 2 and 7.5 hours on each project on average. In general, these values
        trend up as the semester progresses. If we assume that students then spend an average of 4 hours on each
        project, they will conduct roughly 44 hours of work over the course of the semester. 
        '''
    ),  # TODO: use an f-string to include the min and max average here
    dcc.Graph(id="project-time"),
    html.H3('Time Spent Working on Homework Assignments'),
    html.P(
        '''
        Similarly, I asked students to tell me how much time they spent on the homework assignments.
        The data is fairly preliminary, so I only have the first few homework assignments. That
        said, I am finding that students spend multiple hours a week on each written assignment.
        '''
    ),
    dcc.Graph(id="homework-time"),
    html.H3('Emotional Experience with Assignments'),
    html.P(
        '''
        Something new I tried in 2022 was asking students about the emotions they experienced
        before, during, and after assignments. For this, I borrowed the emotions from
        Control Value Theory and asked students retrospectively about their emotions. As it
        is early in the semester, I decided to only plot the homework assignments. Later,
        I'll update this dashboard to include the project assignments as well. TODO: make this
        plot just a single image with a dropdown.
        '''
    ),
    dcc.Graph(id="emotions", className="max-window"),
    html.H3('Rubric Evaluation'),
    html.P(
        """
        Another question I asked my students was about their satisfaction with the rubrics for each project. 
        The following plot gives the overview of the rubric ratings over all 11 projects. In general,
        it appears students are fairly satisfied with the rubrics.
        """
    ),
    dcc.Graph(id="rubric-overview"),
    dcc.Markdown(
        """
        In case you were curious about each project individually, here is a breakdown of the rubric scores for each project. 
        """
    ),
    dcc.Graph(id="rubric-breakdown", className="max-window"),
    dcc.Markdown(
        """
        And just to be perfectly explicit, I also computed average scores for each rubric over all 11 projects.
        These scores are computed by assigning Very Dissatisfied (1) to the lowest score and Very Satisfied (5) 
        to the highest score. Then, we sum up all the values and divide by the number of reviews. As a result,
        you can see that students are generally the least satisfied with the project 1 rubric and most satisfied
        with the project 3 rubric. 
        """
    ),
    dcc.Graph(id="rubric-scores"),
    load_assignment_survey_data()
])
