from io import StringIO

import pandas as pd
from constants import homework_review_col, project_review_col, likert_scale, likert_scale_alt
from dash import Input, Output, callback
from utils import (create_emotions_fig, create_rubric_breakdown_fig,
                   create_rubric_overview_fig, create_rubric_scores_fig,
                   create_sei_fig, create_time_fig, create_sei_comment_fig, create_course_eval_fig, create_grades_fig, create_correlation_fig, create_assignment_fig, create_missing_assignment_fig, create_project_trend_fig)


@callback(
    Output("project-time", "figure"),
    Input("assignment-survey", "data")
)
def render_project_time_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_time_fig(df, col=project_review_col)


@callback(
    Output("homework-time", "figure"),
    Input("assignment-survey", "data")
)
def render_homework_time_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_time_fig(df, col=homework_review_col)


@callback(
    Output("emotions", "figure"),
    Input("assignment-survey", "data")
)
def render_emotions_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_emotions_fig(df, col=homework_review_col)


@callback(
    Output("rubric-overview", "figure"),
    Input("assignment-survey", "data")
)
def render_rubric_overview_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_rubric_overview_fig(df)


@callback(
    Output("rubric-breakdown", "figure"),
    Input("assignment-survey", "data")
)
def render_rubric_breakdown_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_rubric_breakdown_fig(df)


@callback(
    Output("rubric-scores", "figure"),
    Input("assignment-survey", "data")
)
def render_rubric_scores_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_rubric_scores_fig(df)


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


@callback(
    Output("course-content", "figure"),
    Input("course-eval-data", "data")
)
def render_course_content_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_course_eval_fig(df, "Course content", likert_scale)


@callback(
    Output("skill-and-responsiveness", "figure"),
    Input("course-eval-data", "data")
)
def render_skill_and_responsiveness_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_course_eval_fig(df, "Skill and responsiveness", likert_scale)


@callback(
    Output("contribution-to-learning", "figure"),
    Input("course-eval-data", "data")
)
def render_course_content_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_course_eval_fig(df, "Contribution to learning", likert_scale_alt)


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
