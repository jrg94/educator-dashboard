import pandas as pd
from dash import dcc

from core.constants import (class_review_col, during_emotions_column,
                            post_emotions_column, pre_emotions_column)


def load_assignment_survey_data() -> dcc.Store:
    """
    Loads the assignment survey data from the remote CSV, cleans it, and computes
    some important metrics. The result is returned as a store object.
    
    :return: the assignment survey data as a store
    """
    # Load and clean data
    assignment_survey_data = pd.read_csv('https://raw.githubusercontent.com/jrg94/personal-data/main/education/assignment-survey-data.csv')
    assignment_survey_data["Timestamp"] = pd.to_datetime(assignment_survey_data["Timestamp"], format="%Y/%m/%d %I:%M:%S %p %Z")
    assignment_survey_data[class_review_col] = assignment_survey_data[class_review_col].fillna("CSE 2221: Software 1")    
    assignment_survey_data[pre_emotions_column] = assignment_survey_data[pre_emotions_column].astype(str).apply(lambda x: x.split(";"))
    assignment_survey_data[during_emotions_column] = assignment_survey_data[during_emotions_column].astype(str).apply(lambda x: x.split(";"))
    assignment_survey_data[post_emotions_column] = assignment_survey_data[post_emotions_column].astype(str).apply(lambda x: x.split(";"))    
    
    return dcc.Store(id="assignment-survey-data", data=assignment_survey_data.to_json())


def load_sei_data() -> dcc.Store:
    """
    Loads the SEI data from the remote CSV. The result is returned as a store object.
    
    :return: the SEI data as a store
    """
    sei_data = pd.read_csv('https://raw.githubusercontent.com/jrg94/personal-data/main/education/sei-data.csv')
    return dcc.Store(id="sei-data", data=sei_data.to_json())


def load_sei_comments_data() -> dcc.Store:
    """
    Loads the SEI comment data from the remote CSV. The result is returned as a store object.
    
    :return: the SEI comment data as a store 
    """
    sei_comment_data = pd.read_csv('https://raw.githubusercontent.com/jrg94/personal-data/main/education/sei-comments.csv')
    return dcc.Store(id="sei-comments-data", data=sei_comment_data.to_json())


def load_course_eval_data() -> dcc.Store:
    """
    Loads the course evaluation data from the remote CSV. The result is returned as a store object.
    
    :return: the SEI course evaluation data as a store
    """
    course_eval_data = pd.read_csv('https://raw.githubusercontent.com/jrg94/personal-data/main/education/eval-data.csv')
    course_eval_data["Timestamp"] = pd.to_datetime(course_eval_data["Timestamp"], format="%Y/%m/%d %I:%M:%S %p %Z")
    return dcc.Store(id="course-eval-data", data=course_eval_data.to_json())    


def load_cse2221_grade_data() -> dcc.Store:
    """
    Loads the grade data from the remote CSV. The result is returned as a store object. 
    
    :return: the grade data as a store
    """
    grade_data = pd.read_csv('https://raw.githubusercontent.com/jrg94/personal-data/main/education/cse-2221-grades.csv')
    return dcc.Store(id="cse2221-grade-data", data=grade_data.to_json())


def load_cse2231_grade_data() -> dcc.Store:
    """
    Loads the grade data from the remote CSV. The result is returned as a store object. 
    
    :return: the grade data as a store
    """
    grade_data = pd.read_csv('https://raw.githubusercontent.com/jrg94/personal-data/main/education/cse-2231-grades.csv')
    grade_data["Midterm Exam #1"] = pd.to_numeric(grade_data["Midterm Exam #1"], errors="coerce")
    return dcc.Store(id="cse2231-grade-data", data=grade_data.to_json())
