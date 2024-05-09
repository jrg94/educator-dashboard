from numpy import int64
import pandas as pd
from dash import dcc

from core.constants import *


def load_assignment_survey_data() -> dcc.Store:
    """
    Loads the assignment survey data from the remote CSV, cleans it, and computes
    some important metrics. The result is returned as a store object.

    :return: the assignment survey data as a store
    """
    # Load necessary data
    assessment_reviews_df = pd.read_csv(URL_ASSESSMENT_REVIEWS)
    assessments_df = pd.read_csv(URL_ASSESSMENTS)
    assessment_groups_df = pd.read_csv(URL_ASSESSMENT_GROUPS)
    df = assessment_reviews_df \
        .merge(assessments_df, on=COLUMN_ASSESSMENT_ID) \
        .merge(assessment_groups_df, on=COLUMN_ASSESSMENT_GROUP_ID)
        
    # Sets types of columns
    df["DateTime"] = pd.to_datetime(
        assessment_reviews_df["DateTime"],
        format="%Y/%m/%d %I:%M:%S %p %z",
        utc=True
    )
        
    return dcc.Store(id=ID_ASSIGNMENT_SURVEY_DATA, data=df.to_json())


def load_sei_data() -> dcc.Store:
    """
    Loads the SEI data from the remote CSV. The result is returned as a store 
    object.

    :return: the SEI data as a store
    """
    sei_instructor_scores_df = pd.read_csv(URL_SEI_INSTRUCTOR_SCORES)
    sei_reports_df = pd.read_csv(URL_SEI_REPORTS)
    course_sections_df = pd.read_csv(URL_COURSE_SECTIONS)
    courses_df = pd.read_csv(URL_COURSES)
    questions_df = pd.read_csv(URL_SEI_QUESTIONS)
    df = sei_instructor_scores_df \
        .merge(sei_reports_df, on=COLUMN_REPORT_ID) \
        .merge(course_sections_df, on=COLUMN_SECTION_ID) \
        .merge(courses_df, on=COLUMN_COURSE_ID) \
        .merge(questions_df, on=COLUMN_QUESTION_ID)
        
    return dcc.Store(id=ID_SEI_DATA, data=df.to_json())


def load_sei_comments_data() -> dcc.Store:
    """
    Loads the SEI comment data from the remote CSV. The result is returned as a 
    store object.

    :return: the SEI comment data as a store 
    """
    sei_comments = pd.read_csv(URL_SEI_COMMENTS)
    return dcc.Store(id=ID_SEI_COMMENTS_DATA, data=sei_comments.to_json())


def load_course_eval_data() -> dcc.Store:
    """
    Loads the course evaluation data from the remote CSV. The result is returned 
    as a store object.

    :return: the SEI course evaluation data as a store
    """
    course_eval_data = pd.read_csv(URL_EVALUATION_SURVEY_HISTORY)

    # Sets types of columns
    course_eval_data["Timestamp"] = pd.to_datetime(
        course_eval_data["Timestamp"],
        format="%Y/%m/%d %I:%M:%S %p %Z"
    )

    return dcc.Store(id=ID_COURSE_EVAL_DATA, data=course_eval_data.to_json())


def load_education_data() -> dcc.Store:
    """
    Loads the grade data from the remote CSV. The result is returned as a store 
    object. 

    :return: the grade data as a store
    """
    grades_df = pd.read_csv(URL_ASSESSMENT_GRADES)
    course_sections_df = pd.read_csv(URL_COURSE_SECTIONS)
    assessments_df = pd.read_csv(URL_ASSESSMENTS)
    assessment_groups_df = pd.read_csv(URL_ASSESSMENT_GROUPS)
    courses_df = pd.read_csv(URL_COURSES)
    semesters_df = pd.read_csv(URL_SEMESTERS)
    df = grades_df \
        .merge(assessments_df, on=COLUMN_ASSESSMENT_ID) \
        .merge(assessment_groups_df, on=COLUMN_ASSESSMENT_GROUP_ID) \
        .merge(course_sections_df, on=COLUMN_SECTION_ID) \
        .merge(courses_df, on=COLUMN_COURSE_ID) \
        .merge(semesters_df, on=COLUMN_SEMESTER_ID)
    return dcc.Store(id=ID_EDUCATION_DATA, data=df.to_json())
