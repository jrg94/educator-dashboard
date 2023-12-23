import pandas as pd
from dash import dcc

class_review_col = "Which of the following classes is this assignment for?"
project_review_col = "Which project are you reviewing (enter a # between 1 and 11)?"
time_col = "How much time did you spend on this assignment in hours?"
avg_time = "Average Time (hours)"
median_time = "Median Time (hours)"
review_count = "Number of Reviews"
std_time = "Standard Deviation (hours)"

def load_assignment_survey_data() -> dcc.Store:
  """
  Loads the assignment survey data from a CSV, cleans it, and computes
  some important metrics. The result is returned as a dcc.Store object.
  """
  assignment_survey_data = pd.read_csv('https://raw.githubusercontent.com/jrg94/personal-data/main/education/assignment-survey-data.csv')
  assignment_survey_data = assignment_survey_data[assignment_survey_data[class_review_col].isna()]
  assignment_survey_data[avg_time] = assignment_survey_data.groupby(project_review_col)[time_col].transform(lambda x: x.mean())
  assignment_survey_data[median_time] = assignment_survey_data.groupby(project_review_col)[time_col].transform(lambda x: x.median())
  assignment_survey_data[review_count] = assignment_survey_data.groupby(project_review_col)[time_col].transform(lambda x: x.count())
  assignment_survey_data[std_time] = assignment_survey_data.groupby(project_review_col)[time_col].transform(lambda x: x.std())
  return dcc.Store(id="assignment-survey", data=assignment_survey_data.to_json())