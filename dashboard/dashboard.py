import dash
from dash import html
import pandas as pd
import plotly.express as px
from dash import dcc

def create_value_fig(grade_data, assignment_survey_data, assignment, max_score):
  assignment_score_data = [name for name in grade_data.columns if assignment in name]
  assignment_calculations = grade_data[assignment_score_data].agg(["mean", "median"]).T
  assignment_time_data = assignment_survey_data.drop_duplicates(subset=[review_col]).sort_values(by=review_col)
  assignment_time_data["Project #"] = "Project #" + assignment_time_data[review_col].astype(str)
  assignment_time_data = assignment_time_data.set_index(f"{assignment} #")[median_time]
  assignment_aggregate_data = assignment_calculations.join(assignment_time_data)
  assignment_aggregate_data = assignment_aggregate_data.rename(columns={'mean': f'Average Score/{max_score}', 'median': f'Median Score/{max_score}'})
  assignment_aggregate_data["Points per Hour"] = assignment_aggregate_data[f"Median Score/{max_score}"] / assignment_aggregate_data["Median Time (hours)"]
  assignment_aggregate_data["Minutes per Point"] = assignment_aggregate_data["Median Time (hours)"] / assignment_aggregate_data[f"Median Score/{max_score}"] * 60
  assignment_aggregate_data = assignment_aggregate_data.reset_index()
  assignment_expected_time_fig = px.bar(
    assignment_aggregate_data,
    x="index",
    y="Points per Hour",
    labels={
      "index": "Project Name",
      "Points per Hour": "Median Points/Hour of Work",
    },
    text_auto=".2s",
    title="Expected Value Per Project"
  )
  assignment_expected_time_fig.update_layout(showlegend=False)
  assignment_expected_effort_fig = px.bar(
    assignment_aggregate_data,
    x="index",
    y="Minutes per Point",
    labels={
      "index": "Project Name",
      "Minutes per Point": "Median Minutes of Work/Point",
    },
    text_auto=".2s",
    title="Expected Effort Per Project"
  )
  assignment_expected_effort_fig.update_layout(showlegend=False)
  return assignment_expected_time_fig, assignment_expected_effort_fig


def create_assignment_fig(grade_data, assignment, total):
  assignment_data = [name for name in grade_data.columns if assignment in name]
  assignment_calculations = grade_data[assignment_data].agg(["mean", "median"]).T
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

def create_course_eval_fig(course_eval_data, question, axes_labels):
  colors = dict(zip(axes_labels, satisfaction_colors.values()))
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
    title=f"{question} by Subquestion".title(),
    color_discrete_map=colors
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
    title="Project Rubric Satisfaction Scores",
    color_continuous_scale=px.colors.sequential.Viridis
  )
  return rubric_scores_fig

def create_rubric_overview_fig(assignment_survey_data):
  data = assignment_survey_data[rubric_heading].value_counts()
  rubric_fig = px.bar(
    data, 
    color=data.index,
    category_orders={"index": list(satisfaction_mapping.values())},
    labels={
      "index": 'Response',
      "value": 'Number of Reviews',
      "color": 'Response'
    },
    text_auto=True,
    title="Project Rubric Satisfaction Overview",
    color_discrete_map=satisfaction_colors
  )
  rubric_fig.write_html(r'renders\diagram\rubric_fig.html')
  return rubric_fig

def create_rubric_breakdown_fig(assignment_survey_data):
  data = assignment_survey_data.groupby(review_col)[rubric_heading] \
    .value_counts() \
    .unstack() \
    .reset_index() \
    .melt(id_vars=[review_col], var_name="Response", value_name="Number of Reviews") \
    .dropna() 
  rubric_breakdown_fig = px.bar(
    data, 
    x="Response",
    y="Number of Reviews",
    color="Response",
    facet_col=review_col, 
    facet_col_wrap=2,
    text_auto=True,
    category_orders={
      rubric_heading: list(satisfaction_mapping.values()),
      review_col: list(range(1, 12))
    },
    labels={
      rubric_heading: 'Response',
    },
    title="Rubric Satisfaction By Project",
    color_discrete_map=satisfaction_colors
  )
  rubric_breakdown_fig.for_each_annotation(lambda a: a.update(text=f'Project {a.text.split("=")[-1]}'))
  rubric_breakdown_fig.write_html(r'renders\diagram\rubric_breakdown_fig.html')
  return rubric_breakdown_fig

def create_missing_assignment_fig(grade_data, assignment):
  missing_assignment_data = (grade_data == 0).sum() / len(grade_data) * 100
  missing_assignment_data = missing_assignment_data.reset_index()
  missing_assignment_data.rename(columns={'index': 'Assignment', 0: 'Percent Missing'}, inplace=True)
  missing_assignment_data = missing_assignment_data.loc[missing_assignment_data["Assignment"].str.contains(assignment)]
  missing_assignment_fig = px.bar(
    missing_assignment_data, 
    x="Assignment", 
    y="Percent Missing", 
    text_auto=".2s", 
    title=f"Percent of Missing {assignment}s"
  )
  return missing_assignment_fig

def create_project_trend_fig(grade_data, assignment):
  trend_data = grade_data.groupby("Date").mean()[[item for item in grade_data if assignment in item]]
  trend_data = trend_data.reset_index().melt(
    id_vars="Date",
    var_name="Assignment", 
    value_name="Average Score"
  ).dropna()
  
  trend_fig = px.line(
    trend_data,
    x="Date",
    y="Average Score",
    color="Assignment",
    markers=True,
    title=f"Average {assignment} Score by Date"
  )
  return trend_fig

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
likert_scale = ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
likert_scale_alt = ["Poor", "Fair", "Satisfactory", "Very good", "Excellent"]
satisfaction_colors = dict(zip(satisfaction_mapping.values(), px.colors.sequential.Viridis[::2]))

app = dash.Dash(__name__)

server = app.server

# Assignment survey figures
assignment_survey_data = pd.read_csv('https://raw.githubusercontent.com/TheRenegadeCoder/educator-dashboard/main/dashboard/data/assignment-survey-data.csv')
assignment_survey_data[avg_time] = assignment_survey_data.groupby(review_col)[time_col].transform(lambda x: x.mean())
assignment_survey_data[median_time] = assignment_survey_data.groupby(review_col)[time_col].transform(lambda x: x.median())
assignment_survey_data[review_count] = assignment_survey_data.groupby(review_col)[time_col].transform(lambda x: x.count())
project_time_fig = create_time_fig(assignment_survey_data)
rubric_scores_fig = create_rubric_scores_fig(assignment_survey_data)
assignment_survey_data[rubric_heading] = assignment_survey_data[rubric_heading].map(satisfaction_mapping)
rubric_fig = create_rubric_overview_fig(assignment_survey_data)
rubric_breakdown_fig = create_rubric_breakdown_fig(assignment_survey_data)

# SEI figures
sei_data = pd.read_csv('https://raw.githubusercontent.com/TheRenegadeCoder/educator-dashboard/main/dashboard/data/sei-data.csv')
sei_fig = create_sei_fig(sei_data)

# Course evaluation figures
course_eval_data = pd.read_csv('https://raw.githubusercontent.com/TheRenegadeCoder/educator-dashboard/main/dashboard/data/eval-data.csv')
course_content_fig = create_course_eval_fig(course_eval_data, "Course content", likert_scale)
skill_and_responsiveness_fig = create_course_eval_fig(course_eval_data, "Skill and responsiveness", likert_scale)
contribution_to_learning_fig = create_course_eval_fig(course_eval_data, "Contribution to learning", likert_scale_alt)

# Assignment figures
grade_data = pd.read_csv('https://raw.githubusercontent.com/TheRenegadeCoder/educator-dashboard/main/dashboard/data/cse-2221-grades.csv')
grade_data["Date"] = pd.to_datetime(grade_data["Date"])
project_calculations_fig = create_assignment_fig(grade_data, "Project", 10)
homework_calculations_fig = create_assignment_fig(grade_data, "Homework", 2)
exams_calculations_fig = create_assignment_fig(grade_data, "Exam", 100)
missing_project_fig = create_missing_assignment_fig(grade_data, "Project")
missing_homework_fig = create_missing_assignment_fig(grade_data, "Homework")
missing_exam_fig = create_missing_assignment_fig(grade_data, "Exam")
project_trend_fig = create_project_trend_fig(grade_data, "Project")
homework_trend_fig = create_project_trend_fig(grade_data, "Homework")
exam_trend_fig = create_project_trend_fig(grade_data, "Exam")
project_points_per_hour_fig, project_hours_per_point_fig = create_value_fig(grade_data, assignment_survey_data, "Project", 10)

app.layout = html.Div(children=[
  html.H1(children='The Educator\'s Dashboard'),
  html.Hr(),
  html.P(children=
  '''
  A collection of visualizations related to courses taught by myself, Jeremy Grifski, with the first two tabs dedicated
  to an overview of my ability as an instructor and the last two tabs dedicated to one of my courses. 
  '''
  ),
  dcc.Tabs([
    dcc.Tab(label="Student Evaluation of Instruction", children=[
      html.H2(children='Student Evaluation of Instruction'),
      html.P(children=
        '''
        Each semester, the university asks students to fill out a survey about the instruction for the course.
        These data are anonymized and provided as averages for each question. Here is the breakdown of my scores
        against the scores for various cohorts including my department, my college, and my university. In general,
        I outperform all three cohorts, but I'm noticing a downward trend in course organization. For context,
        I taught CSE 1223 in the Fall of 2018 and the Spring of 2019. I've been teaching CSE 2221 ever since, with
        a year gap for research. 
        '''
      ),
      dcc.Graph(id="bad-scale-1", figure=sei_fig),
    ]),
    dcc.Tab(label="Course Evaluation Survey", children=[
      html.H2(children='Course Evaluation Survey Data'),
      dcc.Markdown(
        '''
        At the end of each semester, I ask students to give me feedback on the course. These data are collected
        through a Google Form. Questions are broken down into different areas which include feedback on
        course content, my skill and responsiveness, and the course's contribution to learning. **Note**:
        future work is being done to ensure the following plots feature review counts as seen in the assignment
        survey data. 
        '''
      ),
      html.H3(children='Course Content'),
      html.P(children=
        '''
        One way the course was evaluated was by asking students to rate their satisfaction with the course content.
        In short, there are four questions that I ask that cover topics that range from learning objectives to
        organization. Generally, the students that choose to fill out the course survey seem to be satisfied with 
        the course content. For example, at this time, there have been no "strongly disagree" responses. 
        '''
      ),
      dcc.Graph(figure=course_content_fig),
      html.H3(children='Skill and Responsiveness of the Instructor'),
      html.P(children=
        '''
        Another way the course was evaluated was by asking students to rate their satisfaction with the instructor, me.
        This time around, I ask six questions which range from satisfaction with time usage to satisfaction
        with grading. Again, students are generally happy with my instruction. In fact, they're often more happy
        with my instruction than the course content itself. 
        '''
      ),
      dcc.Graph(figure=skill_and_responsiveness_fig),
      html.H3(children='Contribution to Learning'),
      dcc.Markdown(
        '''
        Yet another way the course was evaluated was by asking students how much they felt the course contributed to 
        their learning. In this section of the survey, I ask students four questions that attempt to chart how much
        students felt they learned over the course of the semester. In general, students believe they learned a great
        deal, with most students reporting only a fair amount of knowledge coming into the course and a very good
        amount of knowledge at the end of the course. **TODO**: I should add a plot showing the scores for all four
        questions with an additional plot showing the trajectory of learning over the semester.
        '''
      ),
      dcc.Graph(figure=contribution_to_learning_fig),
    ]),
    dcc.Tab(label="Assignment Survey [CSE 2221]", children=[
      html.H2(children='Assignment Survey Data [CSE 2221]'),
      html.P(children=
        '''
        Throughout the course, I asked students to give me feedback on the assignments. Originally,
        these data were collected through a Carmen quiz (Autumn 2021). However, I found the Carmen 
        quiz format to be limiting, so later iterations of the quiz were administered through a Google
        Form. 
        '''
      ),
      html.H3(children='Time Spent Working on Assignments'),
      html.P(children=
        '''
        One of the questions I asked my students was how long they spent on each project. Based on the responses,
        I found that students spent between 2 and 7.5 hours on each project on average. In general, these values
        trend up as the semester progresses. If we assume that students then spend an average of 4 hours on each
        project, they will conduct roughly 44 hours of work over the course of the semester. 
        '''
      ), # TODO: use an f-string to include the min and max average here
      dcc.Graph(figure=project_time_fig),
      html.H3(children='Rubric Evaluation'),
      html.P(children=
        """
        Another question I asked my students was about their satisfaction with the rubrics for each project. 
        The following plot gives the overview of the rubric ratings over all 11 projects. In general,
        it appears students are fairly satisfied with the rubrics.
        """
      ),
      dcc.Graph(figure=rubric_fig),
      dcc.Markdown(
        """
        In case you were curious about each project individually, here is a breakdown of the rubric scores for each project. 
        """
      ),
      dcc.Graph(id="bad-scale-2", figure=rubric_breakdown_fig),
      dcc.Markdown(
        """
        And just to be perfectly explicit, I also computed average scores for each rubric over all 11 projects.
        These scores are computed by assigning Very Dissatisfied (1) to the lowest score and Very Satisfied (5) 
        to the highest score. Then, we sum up all the values and divide by the number of reviews. As a result,
        you can see that students are generally the least satisfied with the project 1 rubric and most satisfied
        with the project 3 rubric. 
        """
      ),
      dcc.Graph(figure=rubric_scores_fig),
    ]),
    dcc.Tab(label="Grades [CSE 2221]", children=[
      html.H2(children='Grades [CSE 2221]'),
      html.P(children=
        '''
        Each semester, I collect grades for 22 homework assignments, 11 projects, and 3 exams. Fortunately,
        I have graders for the bulk of it, but I grade the exams. Recently, I decided to put together a
        database of grades which allows me to generate some pretty interesting plots.
        '''
      ),
      html.H3(children='Project Grades'),
      html.P(children=
        '''
        To start, I'd like to talk about the 11 projects. Specifically, I'll share the average and median grade
        for each project. The key takeaway here is that project 1 is a slam dunk while project 8 is a bit rough.
        '''
      ),
      dcc.Graph(figure=project_calculations_fig),
      html.P(children=
        '''
        While medians and averages are helpful, I also think it's useful to look at just how many students
        actually complete the projects. Or rather, what percentage of students skip out on projects, and
        is there a trend to observe? If so (spoiler alert: students turn in less work as the semester 
        progresses), that could potentially explain the low averages for certain projects. 
        '''
      ),
      dcc.Graph(figure=missing_project_fig),
      dcc.Markdown(
        '''
        Unfortunately, one of the drawbacks of the plots above is that they aggregate the data for every
        semester I've taught the course. Personally, I like to see trends, right? For example, it's 
        helpful to know if project grades are getting better over time. What I'm finding is that's not
        the case. Frankly, I think most of this is due to grader influences, but I have not investigated
        that. **TODO**: I should include grader influences in the plot. 
        '''
      ),
      dcc.Graph(figure=project_trend_fig),
      dcc.Markdown(
        '''
        Next, we get into the "advanced" metrics. In this case, I thought it would be interesting to combine
        some of the data found in the assignment survey with the grade data. For instance, remember how
        I previously shared the amount of time students spent on each project on average? Well, I figured
        it would be interesting to see how many points a student could expect to earn per hour on average.
        Ultimately, I ended up calling this metric "Expected Value" because it gives us a sense of how
        much value a student could get out of their time. With this metric, we're able to clearly see that 
        project 1 offers the most bang for your buck. Meanwhile, Project 8 offers very little in terms of
        value for your time. 
        '''
      ),
      dcc.Graph(figure=project_points_per_hour_fig),
      dcc.Markdown(
        '''
        Interestingly, if we invert the previous plot, we get what I'm calling the "Expected Effort" metric.
        Rather than describing the amount of points we expect to get for an hour of work, we begin talking
        about how much time we expect to give for a point. The distinction is fairly minor, but it allows
        us to see which projects require the most effort. In this case, the roles are reversed. Project 1
        requires the least amount of effort, while project 8 requires the most.
        '''
      ),
      dcc.Graph(figure=project_hours_per_point_fig),
      html.H3(children='Homework Grades'),
      dcc.Markdown(
        '''
        In addition to 11 projects, we also assign 22 homework assignments. These assignments are graded
        on completion for a maximum of 2 points each. Naturally, here's the breakdown of average and median
        scores for each assignment. As you can see, students generally get full credit, but there are some
        students who pull the average down with incomplete assignments (more on that later).
        '''
      ),
      dcc.Graph(figure=homework_calculations_fig),
      dcc.Markdown(
        '''
        As promised, here's a look at the trend of homework completion. As with projects, students tend
        to submit fewer assignments as the semester progresses. Though, I find it interesting that there
        are spikes in missing assignments at various points throughout the semester. I suspect that the 
        assignments that students submit least often are tied to larger review assignments before exams.
        **TODO**: I should look into this more.
        '''
      ),
      dcc.Graph(figure=missing_homework_fig),
      dcc.Markdown(
        '''
        Finally, here's a look at the trend of grades for the homework assignments. I find this plot really
        interesting because it shows the spread of homework grades against each semester. For instance,
        there is quite the spread of homework averages in Autumn 2021. 
        '''
      ),
      dcc.Graph(figure=homework_trend_fig),
      html.H3(children='Exam Grades'),
      dcc.Markdown(
        '''
        At this point, all that is left to discuss are the exams. In total, there are three exams, and the
        general trend tends to be that scores go down as the semester progresses. I haven't quite figured
        out why. 
        '''
      ),
      dcc.Graph(figure=exams_calculations_fig),
      dcc.Markdown(
        '''
        As with projects and homework assignments, I find it important to also track the percentage of students
        who skip exams. In general, it's pretty rare for a student to skip an exam, and it's usually due to some
        extreme circumstance. That said, the trend remains the same for exams as well (i.e., fewer students attend
        the exams as the semester progresses).
        '''
      ),
      dcc.Graph(figure=missing_exam_fig),
      dcc.Markdown(
        '''
        All that is left to talk about is the exam score trend over time. One thing that is worth noting is that
        the exams were not consistent from semester to semester. For example, you'll notice that exams 2 and 3
        are missing data points. The reason for this is that we eventually converted those exams to online quizzes
        due to COVID. As a result, those quiz scores are omitted. It's also worth noting that the data points in
        Summer 2019 are from before I started teaching the course (i.e., I was training to teach it at the time).
        As a result, the first time I taught the course, my exam scores were quite low. Since then, things have
        improved considerably. Well, except for the final exam. I'll be looking to provide more ways for
        students to practice ahead of time. 
        '''
      ),
      dcc.Graph(figure=exam_trend_fig),
    ]),
  ])
])

if __name__ == '__main__':
  app.run_server(debug=True)
