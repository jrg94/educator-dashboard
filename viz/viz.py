import dash
from dash import html
import pandas as pd
import plotly.express as px
from dash import dcc

def create_assignment_fig(grade_data, assignment, total):
  assgnment_data = [name for name in grade_data.columns if assignment in name]
  assignment_calculations = grade_data[assgnment_data].agg(["mean", "median"]).T
  assignment_calculations.rename(columns={'mean': 'Average', 'median': 'Median'}, inplace=True)
  assignment_calculations_fig = px.bar(
    assignment_calculations,
    labels={
      "index": "Project Name",
      "value": f"Grade/{total}",
      "variable": "Metric",
      "mean": "Average",
      "median": "Median"
    },
    barmode='group',
    text_auto=".2s",
    title=f"Average and Median {assignment} Grades".title()
  )
  return assignment_calculations_fig

def create_course_eval_fig(course_eval_data, question):
  axes_labels = ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
  question_data = course_eval_data.melt(
    id_vars=[item for item in course_eval_data.columns if question not in item],
    var_name="Question",
    value_name="Response"
  )
  question_data = question_data[question_data["Response"].notna()]
  question_fig = px.histogram(
    question_data, 
    x="Response", 
    color="Response", 
    facet_col="Question", 
    facet_col_wrap=2, 
    category_orders=dict(Response=axes_labels),
    text_auto=True,
    title=f"{question} by Subquestion".title()
  )
  question_fig.for_each_annotation(lambda a: a.update(text=a.text[a.text.find("[")+1:a.text.find("]")]))
  return question_fig

def create_sei_fig(sei_data):
  sei_data["Date"] = pd.to_datetime(sei_data["Date"])
  sei_fig = px.line(
    sei_data, 
    x="Date", 
    y="Mean", 
    color="Group", 
    facet_col="Question", 
    facet_col_wrap=2, 
    markers=True, 
    height=800,
    title="Student Evaluation of Instruction Trends by Cohort"
  )
  sei_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
  return sei_fig

def create_time_fig(assignment_survey_data):
  to_plot = assignment_survey_data.drop_duplicates(subset=[review_col]).sort_values(by=review_col)
  to_plot = to_plot.melt(
    id_vars=[item for item in to_plot.columns if item not in [avg_time, median_time]], 
    var_name="Metric", 
    value_name="Time (hours)"
  )
  time_fig = px.bar(
    to_plot, 
    x=review_col, 
    y="Time (hours)", 
    color="Metric", 
    text_auto=".2s", 
    barmode='group',
    title="Average and Median Project Time"
  )
  time_fig.write_html(r'renders\diagram\project_fig.html')
  return time_fig

def create_rubric_scores_fig(assignment_survey_data):
  rubric_scores = assignment_survey_data.groupby(review_col)[rubric_heading].agg(["mean", "count"])
  rubric_scores_fig = px.bar(
    rubric_scores, 
    y="mean", 
    color="count",
    labels={
      "mean": "Average Score (out of 5)",
      "count": "Number of Reviews"
    },
    text_auto=".3s",
    title="Project Rubric Satisfaction Scores"
  )
  return rubric_scores_fig

def create_rubric_overview_fig(assignment_survey_data):
  rubric_fig = px.histogram(
    assignment_survey_data, 
    x=rubric_heading, 
    color=rubric_heading, 
    category_orders={rubric_heading: list(satisfaction_mapping.values())},
    labels={rubric_heading: 'Response'},
    text_auto=".3s",
    title="Project Rubric Satisfaction Overview"
  )
  rubric_fig.write_html(r'renders\diagram\rubric_fig.html')
  return rubric_fig

def create_rubric_breakdown_fig(assignment_survey_data):
  rubric_breakdown_fig = px.histogram(
    assignment_survey_data, 
    x=rubric_heading, 
    color=rubric_heading,
    facet_col=review_col, 
    facet_col_wrap=2,
    height=800, 
    category_orders={
      rubric_heading: list(satisfaction_mapping.values()),
      review_col: list(range(1, 12))
    },
    labels={
      rubric_heading: 'Response',
    },
    title="Rubric Satisfaction By Project"
  )
  rubric_breakdown_fig.for_each_annotation(lambda a: a.update(text=f'Project {a.text.split("=")[-1]}'))
  rubric_breakdown_fig.write_html(r'renders\diagram\rubric_breakdown_fig.html')
  return rubric_breakdown_fig

rubric_heading = 'On a scale from 1 to 5, how satisfied are you with the rubric for this project?'
review_col = "Which project are you reviewing (enter a # between 1 and 11)?"
time_col = "How much time did you spend on this assignment in hours?"
avg_time = "Average Time (hours)"
median_time = "Median Time (hours)"
review_count = "Number of Reviews"
satisfaction_mapping = {
  1: 'Very Dissatisfied', 
  2: 'Dissatisfied', 
  3: 'Neutral', 
  4: 'Satisfied', 
  5: 'Very Satisfied'
}

app = dash.Dash(__name__)

# Assignment survey figures
assignment_survey_data = pd.read_csv(r'viz\data\assignment-survey-data.csv')
assignment_survey_data[avg_time] = assignment_survey_data.groupby(review_col)[time_col].transform(lambda x: x.mean())
assignment_survey_data[median_time] = assignment_survey_data.groupby(review_col)[time_col].transform(lambda x: x.median())
assignment_survey_data[review_count] = assignment_survey_data.groupby(review_col)[time_col].transform(lambda x: x.count())
project_time_fig = create_time_fig(assignment_survey_data)
rubric_scores_fig = create_rubric_scores_fig(assignment_survey_data)
assignment_survey_data[rubric_heading] = assignment_survey_data[rubric_heading].map(satisfaction_mapping)
rubric_fig = create_rubric_overview_fig(assignment_survey_data)
rubric_breakdown_fig = create_rubric_breakdown_fig(assignment_survey_data)

# SEI figures
sei_data = pd.read_csv(r'viz\data\sei-data.csv')
sei_fig = create_sei_fig(sei_data)

# Course evaluation figures
course_eval_data = pd.read_csv(r'viz\data\eval-data.csv')
course_content_fig = create_course_eval_fig(course_eval_data, "Course content")
skill_and_responsiveness_fig = create_course_eval_fig(course_eval_data, "Skill and responsiveness")
contribution_to_learning_fig = create_course_eval_fig(course_eval_data, "Contribution to learning")

# Assignment figures
grade_data = pd.read_csv(r'viz\data\au-2021-cse-2221-grades.csv')
project_calculations_fig = create_assignment_fig(grade_data, "Project", 10)
homework_calculations_fig = create_assignment_fig(grade_data, "Homework", 2)
exams_calculations_fig = create_assignment_fig(grade_data, "Exam", 100)

print((grade_data == 0).sum())

app.layout = html.Div(children=[
  html.H1(children='CSE 2221 Visualization'),
  html.Hr(),
  html.P(children='A collection of visualizations related to course data for CSE 2221.'),
  html.H2(children='Assignment Survey Data'),
  html.P(children='Throughout the course, I asked students to give me feedback on the assignments.'),
  html.H3(children='Time Spent Working on Assignments'),
  html.P(children='One of the questions I asked was how long students spent on each project.'),
  dcc.Graph(figure=project_time_fig),
  html.H3(children='Rubric Evaluation'),
  html.P(children="""
    The rubric for each project was used to evaluate students\' performance. I asked students to rate their satisfaction with the rubric.
    The first plot gives the overview of the rubric ratings over all 11 projects. The following plot gives a per project breakdown. 
  """
  ),
  dcc.Graph(figure=rubric_fig),
  dcc.Graph(figure=rubric_breakdown_fig),
  dcc.Graph(figure=rubric_scores_fig),
  html.H2(children='Course Evaluation Survey Data'),
  html.P(children='At the end of the course, I ask students to give me feedback on it.'),
  html.H3(children='Course Content'),
  html.P(children='One way the course was evaluated by asking students to rate their satisfaction with the course content.'),
  dcc.Graph(figure=course_content_fig),
  html.H3(children='Skill and Responsiveness of the Instructor'),
  html.P(children='Another way the course was evaluated by asking students to rate their satisfaction with the instructor.'),
  dcc.Graph(figure=skill_and_responsiveness_fig),
  html.H3(children='Contribution to Learning'),
  html.P(children='Another way the course was evaluated by asking students how much they felt the course contributed to their.'),
  dcc.Graph(figure=contribution_to_learning_fig),
  html.H2(children='Student Evaluation of Instruction Data'),
  html.P(children='Each semester, the university asks students to fill out a survey about instruction.'),
  dcc.Graph(figure=sei_fig),
  html.H2(children='Grades'),
  html.P(children='The grades for each project are shown below.'),
  dcc.Graph(figure=project_calculations_fig),
  dcc.Graph(figure=homework_calculations_fig),
  dcc.Graph(figure=exams_calculations_fig)
])

if __name__ == '__main__':
  app.run_server(debug=True)
