import pandas as pd
from dash import dcc
from constants import avg_time, median_time, review_count, std_time, class_review_col, project_review_col, time_col, homework_review_col, pre_emotions_column, during_emotions_column, post_emotions_column, rubric_heading, satisfaction_mapping


def load_assignment_survey_data() -> dcc.Store:
    """
    Loads the assignment survey data from a CSV, cleans it, and computes
    some important metrics. The result is returned as a dcc.Store object.
    """
    # Load and clean data
    assignment_survey_data = pd.read_csv('https://raw.githubusercontent.com/jrg94/personal-data/main/education/assignment-survey-data.csv')
    assignment_survey_data["Timestamp"] = pd.to_datetime(assignment_survey_data["Timestamp"], format="%Y/%m/%d %I:%M:%S %p %Z")
    assignment_survey_data = assignment_survey_data[assignment_survey_data[class_review_col].isna()]
    
    # Compute project statistics
    assignment_survey_data[avg_time] = assignment_survey_data.groupby(project_review_col)[time_col].transform(lambda x: x.mean())
    assignment_survey_data[median_time] = assignment_survey_data.groupby(project_review_col)[time_col].transform(lambda x: x.median())
    assignment_survey_data[review_count] = assignment_survey_data.groupby(project_review_col)[time_col].transform(lambda x: x.count())
    assignment_survey_data[std_time] = assignment_survey_data.groupby(project_review_col)[time_col].transform(lambda x: x.std())
    
    # Compute homework statistics
    homework_time_mean = assignment_survey_data.groupby(homework_review_col)[time_col].transform(lambda x: x.mean())
    homework_time_median = assignment_survey_data.groupby(homework_review_col)[time_col].transform(lambda x: x.median())
    homework_time_count = assignment_survey_data.groupby(homework_review_col)[time_col].transform(lambda x: x.count())
    homework_time_std = assignment_survey_data.groupby(homework_review_col)[time_col].transform(lambda x: x.std())
    
    # Update project statistics column with homework statistics data
    assignment_survey_data[avg_time] = assignment_survey_data[avg_time].combine_first(homework_time_mean)
    assignment_survey_data[median_time] = assignment_survey_data[median_time].combine_first(homework_time_median)
    assignment_survey_data[review_count] = assignment_survey_data[review_count].combine_first(homework_time_count)
    assignment_survey_data[std_time] = assignment_survey_data[std_time].combine_first(homework_time_std)

    # Clean emotions columns
    assignment_survey_data[pre_emotions_column] = assignment_survey_data[pre_emotions_column].astype(str).apply(lambda x: x.split(";"))
    assignment_survey_data[during_emotions_column] = assignment_survey_data[during_emotions_column].astype(str).apply(lambda x: x.split(";"))
    assignment_survey_data[post_emotions_column] = assignment_survey_data[post_emotions_column].astype(str).apply(lambda x: x.split(";"))    
    
    return dcc.Store(id="assignment-survey", data=assignment_survey_data.to_json())
