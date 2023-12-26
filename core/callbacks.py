from io import StringIO

import pandas as pd
from dash import Input, Output, callback

from core.constants import (homework_review_col, likert_scale,
                            likert_scale_alt, project_review_col)
from core.utils import (create_assignment_fig, create_correlation_fig,
                        create_course_eval_fig, create_emotions_fig,
                        create_grades_fig, create_missing_assignment_fig,
                        create_project_trend_fig, create_rubric_breakdown_fig,
                        create_rubric_overview_fig, create_rubric_scores_fig,
                        create_sei_comment_fig, create_sei_fig,
                        create_time_fig, create_value_fig)




@callback(
    Output("grade-overview", "figure"),
    Input("grade-data", "data")
)
def render_grade_overview_data(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_grades_fig(df)


@callback(
    Output("grade-vs-attendance", "figure"),
    Input("grade-data", "data")
)
def render_grade_overview_data(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_correlation_fig(df, "TH-Attendance", "Top Hat Attendance")


@callback(
    Output("grade-vs-participation", "figure"),
    Input("grade-data", "data")
)
def render_grade_overview_data(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_correlation_fig(df, "Top Hat", "Top Hat Participation")


@callback(
    Output("project-calculations", "figure"),
    Input("grade-data", "data")
)
def render_grade_overview_data(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_assignment_fig(df, "Project", 10)


@callback(
    Output("homework-calculations", "figure"),
    Input("grade-data", "data")
)
def render_grade_overview_data(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_assignment_fig(df, "Homework", 2)


@callback(
    Output("exams-calculations", "figure"),
    Input("grade-data", "data")
)
def render_grade_overview_data(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_assignment_fig(df, "Exam", 100)


@callback(
    Output("missing-projects", "figure"),
    Input("grade-data", "data")
)
def render_grade_overview_data(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_missing_assignment_fig(df, "Project")


@callback(
    Output("missing-homeworks", "figure"),
    Input("grade-data", "data")
)
def render_grade_overview_data(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_missing_assignment_fig(df, "Homework")


@callback(
    Output("missing-exams", "figure"),
    Input("grade-data", "data")
)
def render_grade_overview_data(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_missing_assignment_fig(df, "Exam")


@callback(
    Output("project-trends", "figure"),
    Input("grade-data", "data")
)
def render_grade_overview_data(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_project_trend_fig(df, "Project")


@callback(
    Output("homework-trends", "figure"),
    Input("grade-data", "data")
)
def render_grade_overview_data(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_project_trend_fig(df, "Homework")


@callback(
    Output("exam-trends", "figure"),
    Input("grade-data", "data")
)
def render_grade_overview_data(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_project_trend_fig(df, "Exam")


@callback(
    Output("project-points-per-hour", "figure"),
    Output("project-hours-per-point", "figure"),
    Input("grade-data", "data"),
    Input("assignment-survey-data", "data")
)
def render_points_per_hour_graph(jsonified_grade_data, jsonified_assignment_survey_data):
    grade_data = pd.read_json(StringIO(jsonified_grade_data))
    assignment_survey_data = pd.read_json(StringIO(jsonified_assignment_survey_data))
    return create_value_fig(grade_data, assignment_survey_data, "Project", 10)
