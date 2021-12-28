import dash
from dash import html
import pandas as pd
import plotly.express as px
from dash import dcc

review_col = "Which project are you reviewing (enter a # between 1 and 11)?"
time_col = "How much time did you spend on this assignment in hours?"
avg_time = "Average Time (hours)"
median_time = "Median Time (hours)"
review_count = "Number of Reviews"

app = dash.Dash(__name__)

# Loading and managing assignment data
grading_data = pd.read_csv(r'viz\data\assignment-survey-data.csv')
grading_data[avg_time] = grading_data.groupby(review_col)[time_col].transform(lambda x: x.mean())
grading_data[median_time] = grading_data.groupby(review_col)[time_col].transform(lambda x: x.median())
grading_data[review_count] = grading_data.groupby(review_col)[time_col].transform(lambda x: x.count())

to_plot = grading_data.drop_duplicates(subset=[review_col]).sort_values(by=review_col)
project_mean_fig = px.bar(to_plot, x=review_col, y=avg_time, color=review_count, text_auto=".2s")
project_mean_fig.write_html(r'renders\diagram\project_fig.html')
project_median_fig = px.bar(to_plot, x=review_col, y=median_time, color=review_count, text_auto=".2s")

rubric_heading = 'On a scale from 1 to 5, how satisfied are you with the rubric for this project?'

rubric_scores = grading_data.groupby(review_col)[rubric_heading].agg(["mean", "count"])
rubric_scores_fig = px.bar(
  rubric_scores, 
  y="mean", 
  color="count",
  labels={
    "mean": "Average Score (out of 5)",
    "count": "Number of Reviews"
  },
  text_auto=".3s"
)

satisfaction_mapping = {1: 'Very Dissatisfied', 2: 'Dissatisfied', 3: 'Neutral', 4: 'Satisfied', 5: 'Very Satisfied'}
grading_data[rubric_heading] = grading_data[rubric_heading].map(satisfaction_mapping)
rubric_fig = px.histogram(
  grading_data, 
  x=rubric_heading, 
  color=rubric_heading, 
  category_orders={rubric_heading: list(satisfaction_mapping.values())},
    labels={rubric_heading: 'Response'}
)
rubric_fig.write_html(r'renders\diagram\rubric_fig.html')

rubric_breakdown_fig = px.histogram(
  grading_data, 
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
  }
)
rubric_breakdown_fig.for_each_annotation(lambda a: a.update(text=f'Project {a.text.split("=")[-1]}'))
rubric_breakdown_fig.write_html(r'renders\diagram\rubric_breakdown_fig.html')

# Loading and managing course evaluation data
course_eval_data = pd.read_csv(r'viz\data\eval-data.csv')

def create_course_eval_fig(course_eval_data, question):
  axes_labels = ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
  question = course_eval_data.melt(
    id_vars=[item for item in course_eval_data.columns if question not in item],
    var_name="Question",
    value_name="Response"
  )
  question = question[question["Response"].notna()]
  question_fig = px.histogram(question, x="Response", color="Response", facet_col="Question", facet_col_wrap=2, category_orders=dict(Response=axes_labels))
  question_fig.for_each_annotation(lambda a: a.update(text=a.text[a.text.find("[")+1:a.text.find("]")]))
  return question_fig

course_content_fig = create_course_eval_fig(course_eval_data, "Course content")

skill_and_responsiveness = course_eval_data.melt(
  id_vars=[item for item in course_eval_data.columns if "Skill and responsiveness of the instructor" not in item],
  var_name="Question", 
  value_name="Response"
)
skill_and_responsiveness = skill_and_responsiveness[skill_and_responsiveness["Response"].notna()]

axes_labels = ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
skill_and_responsiveness_fig = px.histogram(skill_and_responsiveness, x="Response", color="Response", facet_col="Question", facet_col_wrap=2, category_orders=dict(Response=axes_labels))
skill_and_responsiveness_fig.for_each_annotation(lambda a: a.update(text=a.text[a.text.find("[")+1:a.text.find("]")]))

contribution_to_learning = course_eval_data.melt(
  id_vars=[item for item in course_eval_data.columns if "Contribution to learning" not in item],
  var_name="Question", 
  value_name="Response"
)
contribution_to_learning = contribution_to_learning[contribution_to_learning["Response"].notna()]

axes_labels = ["Poor", "Fair", "Satisfactory", "Very good", "Excellent"]
contribution_to_learning_fig = px.histogram(contribution_to_learning, x="Response", color="Response", facet_col="Question", facet_col_wrap=2, category_orders=dict(Response=axes_labels))
contribution_to_learning_fig.for_each_annotation(lambda a: a.update(text=a.text[a.text.find("[")+1:a.text.find("]")]))

# Loading and managing course evaluation data
sei_data = pd.read_csv(r'viz\data\sei-data.csv')
sei_data["Date"] = pd.to_datetime(sei_data["Date"])
sei_fig = px.line(sei_data, x="Date", y="Mean", color="Group", facet_col="Question", facet_col_wrap=2, markers=True, height=800)
sei_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Loading and managing grades
grade_data = pd.read_csv(r'viz\data\au-2021-cse-2221-grades.csv')
projects = [name for name in grade_data.columns if "Project" in name]
project_means = grade_data[projects].agg(["mean", "median"]).T
project_means_fig = px.bar(
  project_means,
  labels={
    "index": "Project Name",
    "value": "Grade/10",
    "variable": "Calculation"
  },
  barmode='group'
)

homework = [name for name in grade_data.columns if "Homework" in name]
homework_calculations = grade_data[homework].agg(["mean", "median"]).T
homework_calculations_fig = px.bar(
  homework_calculations,
  labels={
    "index": "Homework Name",
    "value": "Grade/2",
    "variable": "Calculation"
  },
  barmode='group'
)

exams = [name for name in grade_data.columns if "Exam" in name]
exams_calculations = grade_data[exams].agg(["mean", "median"]).T
exams_calculations_fig = px.bar(
  exams_calculations,
  labels={
    "index": "Exam Name",
    "value": "Grade/100",
    "variable": "Calculation"
  },
  barmode='group'
)

app.layout = html.Div(children=[
  html.H1(children='CSE 2221 Visualization'),
  html.Hr(),
  html.P(children='A collection of visualizations related to course data for CSE 2221.'),
  html.H2(children='Assignment Survey Data'),
  html.P(children='Throughout the course, I asked students to give me feedback on the assignments.'),
  html.H3(children='Time Spent Working on Assignments'),
  html.P(children='One of the questions I asked was how long students spent on each project.'),
  dcc.Graph(figure=project_mean_fig),
  dcc.Graph(figure=project_median_fig),
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
  dcc.Graph(figure=project_means_fig),
  dcc.Graph(figure=homework_calculations_fig),
  dcc.Graph(figure=exams_calculations_fig)
])

if __name__ == '__main__':
  app.run_server(debug=True)
