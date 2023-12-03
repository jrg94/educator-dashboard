from collections import Counter
import string
import dash
from dash import html
import pandas as pd
import plotly
import plotly.express as px
from dash import dcc
import nltk
from nltk.corpus import stopwords

# Constants
rubric_heading = 'On a scale from 1 to 5, how satisfied are you with the rubric for this project?'
project_review_col = "Which project are you reviewing (enter a # between 1 and 11)?"
homework_review_col = "Which homework assignment are you reviewing (enter a # between 1 and 37)?"
class_review_col = "Which of the following classes is this assignment for?"
pre_emotions_column = "Which of the following emotions did you experience **before** starting this project (select all that apply)?"
during_emotions_column = "Which of the following emotions did you experience while completing this project (select all that apply)?"
post_emotions_column = "Which of the following emotions did you experience **after** completing this project (select all that apply)?"
time_col = "How much time did you spend on this assignment in hours?"
avg_time = "Average Time (hours)"
median_time = "Median Time (hours)"
review_count = "Number of Reviews"
std_time = "Standard Deviation (hours)"
assignment_type = "Are you reviewing a project or a homework assignment?"
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

def _semester_order(data: pd.DataFrame):
  """
  Returns a sorted list of semesters in the expected order 
  (e.g., [Autumn 2018, Spring 2019, Autumn 2019, Spring 2020, ...]).
  
  It works by parsing the semester string and calculating a
  sortable numeric value where the year is used unless
  the semester is in the autumn, in which case the year + .5
  is used. 

  :param data: the DataFrame provided by the user with an assumed Semester column
  :return: a list of sorted semesters
  """
  return sorted(
    data["Semester"].unique(), 
    key=lambda x: int(x.split()[1]) + (.5 if x.split()[0] == "Autumn" else 0)
  )

def create_value_fig(grade_data, assignment_survey_data, assignment, max_score):
  assignment_score_data = [name for name in grade_data.columns if assignment in name]
  assignment_calculations = grade_data[assignment_score_data].agg(["mean", "median"]).T
  assignment_time_data = assignment_survey_data[assignment_survey_data[assignment_type] == "Project"]
  assignment_time_data = assignment_time_data.drop_duplicates(subset=[project_review_col]).sort_values(by=project_review_col)
  assignment_time_data["Project #"] = "Project #" + assignment_time_data[project_review_col].astype(int).astype(str)
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


def create_correlation_fig(grade_data, correlating_factor, label):
  grade_overview = generate_grade_overview(grade_data)

  total_scores = grade_overview["Exams"] * .6 \
    + grade_overview["Homeworks"] * .06 \
    + grade_overview["Projects"] * .3 \
    + grade_overview["Participation"] * .04

  correlation = {
    "Grades": total_scores,
    label: grade_data[correlating_factor]
  }

  return px.scatter(
    pd.DataFrame(correlation),
    y="Grades",
    x=label,
    trendline="ols",
    title=f"Grades vs {label}"
  )


def generate_grade_overview(grade_data):
  grade_data = grade_data[grade_data["Date"] != "2020-05-07"]
  exam_columns = [name for name in grade_data.columns if "Exam" in name]
  homework_columns = [name for name in grade_data.columns if "Homework" in name]
  project_columns = [name for name in grade_data.columns if "Project" in name]
  participation_columns = [name for name in grade_data.columns if "Participation" in name]

  exam_grades = grade_data[exam_columns].sum(axis=1) / (100 * 3) * 100
  homework_grades = grade_data[homework_columns].sum(axis=1) / (2 * 22) * 100
  project_grades = grade_data[project_columns].sum(axis=1) / (10 * 11) * 100
  participation_grades = grade_data[participation_columns].sum(axis=1) / (4 * 1) * 100

  overview_dict = {
    "Exams": exam_grades,
    "Homeworks": homework_grades,
    "Projects": project_grades,
    "Participation": participation_grades
  }

  return pd.DataFrame(overview_dict)


def create_grades_fig(grade_data):
  assignment_calculations = generate_grade_overview(grade_data).agg(["mean", "median"]).T
  row_count = len(grade_data.index)
  assignment_calculations["count"] = {
    "Exams": row_count * 3,
    "Projects": row_count * 11,
    "Homeworks": row_count * 22,
    "Participation": row_count
  }
  grade_fig = px.bar(
    assignment_calculations,
    labels={
      "index": "Assignment Type",
      "value": "Grade/100%",
      "variable": "Metric",
      "mean": "Average",
      "median": "Median",
      "count": "Estimated Count"
    },
    barmode="group",
    title=f"Overview of Course Grades by Type",
    hover_data=["count"]
  )
  return grade_fig


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

def create_sei_fig(sei_data: pd.DataFrame) -> plotly.graph_objs.Figure:
  """
  Creates an SEI data figure showing all of the SEI
  data results over "time", where time is a categorical
  semester string that is added to the SEI data. There
  are four lines in this plot to compare against my
  SEI data (i.e., the department, college, and university).
  
  :param sei_data: the raw SEI data as a dataframe
  :return: the resulting SEI figure
  """
  sei_data["Semester"] = sei_data["Season"] + " " + sei_data["Year"].astype(str)
  sei_fig = px.line(
    sei_data, 
    x="Semester", 
    y="Mean", 
    color="Group", 
    facet_col="Question", 
    facet_col_wrap=2, 
    markers=True, 
    title="Student Evaluation of Instruction Trends by Cohort",
    category_orders={
      "Semester": _semester_order(sei_data)
    },
    hover_data=["Course"]
  )
  sei_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
  return sei_fig

def create_sei_comment_fig(sei_comments: pd.DataFrame) -> plotly.graph_objs.Figure:
  # Tokenizes the comments and computes their counts
  results = Counter()
  sei_comments["Comment"].str.lower().str.capitalize().apply(nltk.word_tokenize).apply(results.update)
  word_counts = pd.DataFrame.from_dict(results, orient="index").reset_index()
  word_counts = word_counts.rename(columns={"index": "Word", 0:"Count"})  
  
  # Installs needed corpus data
  try:
    nltk.data.find("tokenizers/punkt")
  except LookupError:
    nltk.download('punkt')
    
  try:
    nltk.data.find("corpora/stopwords")
  except LookupError:
    nltk.download('stopwords')
  
  # Removes stop words and punctuation from the totals
  stop = stopwords.words("english")
  word_counts = word_counts[~word_counts["Word"].isin(stop)]
  word_counts = word_counts[~word_counts["Word"].isin(list(string.punctuation))]
  word_counts = word_counts[~word_counts["Word"].str.contains("'")]
  
  # Sorts and pulls the top 25 words
  word_counts = word_counts.sort_values(by="Count", ascending=False)
  word_counts = word_counts.head(25)
  word_counts = word_counts.sort_values(by="Count")
  sei_comment_fig = px.bar(
    word_counts,
    x="Count",
    y="Word",
    height=1000,
    title="Top 25 Most Common Words in SEI Comments"
  )
  return sei_comment_fig

def create_time_fig(assignment_survey_data: pd.DataFrame, col: str):
  """
  Creates a figure of the average and median time spent
  on each assignment.
  """
  to_plot = assignment_survey_data \
    .drop_duplicates(subset=[col]) \
    .dropna(subset=[col]) \
    .sort_values(by=col)
  to_plot = to_plot.melt(
    id_vars=[item for item in to_plot.columns if item not in [avg_time, median_time]], 
    var_name="Metric", 
    value_name="Time (hours)"
  )
  time_fig = px.bar(
    to_plot, 
    x=col, 
    y="Time (hours)", 
    color="Metric", 
    text_auto=".2s", 
    barmode='group',
    title="Average and Median Assignment Time",
    error_y=std_time,
    hover_data=[review_count]
  )
  time_fig.update_traces(textfont_size=12, textangle=0, textposition="inside", insidetextanchor="start", cliponaxis=False)
  return time_fig

def create_rubric_scores_fig(assignment_survey_data):
  rubric_scores = assignment_survey_data.groupby(project_review_col)[rubric_heading].agg(["mean", "count"])
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
  return rubric_fig

def create_rubric_breakdown_fig(assignment_survey_data):
  data = assignment_survey_data.groupby(project_review_col)[rubric_heading] \
    .value_counts() \
    .unstack() \
    .reset_index() \
    .melt(id_vars=[project_review_col], var_name="Response", value_name="Number of Reviews") \
    .dropna() 
  rubric_breakdown_fig = px.bar(
    data, 
    x="Response",
    y="Number of Reviews",
    color="Response",
    facet_col=project_review_col, 
    facet_col_wrap=2,
    text_auto=True,
    category_orders={
      rubric_heading: list(satisfaction_mapping.values()),
      project_review_col: list(range(1, 12))
    },
    labels={
      rubric_heading: 'Response',
    },
    title="Rubric Satisfaction By Project",
    color_discrete_map=satisfaction_colors
  )
  rubric_breakdown_fig.for_each_annotation(lambda a: a.update(text=f'Project {a.text.split("=")[-1]}'))
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

def create_project_trend_fig(grade_data: pd.DataFrame, assignment: str):
  """
  Creates a semesterly line graph for each assignment of a
  particular type (e.g., Exam, Project, Homework, etc.)
  """
  trend_data = grade_data.groupby("Date").mean(numeric_only=True)[[item for item in grade_data if assignment in item]]
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

def create_emotions_fig(assignment_survey_data, review_column):
  emotions_data = assignment_survey_data.explode(pre_emotions_column)
  emotions_data = emotions_data.explode(during_emotions_column)
  emotions_data = emotions_data.explode(post_emotions_column)
  emotions_data = emotions_data[emotions_data[pre_emotions_column].isin(["Joy", "Hope", "Hopelessness", "Relief", "Anxiety"])]
  emotions_data = emotions_data[emotions_data[during_emotions_column].isin(["Enjoyment", "Anger", "Frustration", "Boredom"])]
  emotions_data = emotions_data[emotions_data[post_emotions_column].isin(["Joy", "Pride", "Gratitude", "Sadness", "Shame", "Anger"])]
  emotions_data = emotions_data.groupby(review_column)[[pre_emotions_column, during_emotions_column, post_emotions_column]].value_counts() 
  emotions_data = emotions_data.reset_index().melt(id_vars=review_column, value_vars=[pre_emotions_column, during_emotions_column, post_emotions_column])
  emotions_data = emotions_data.replace({
    pre_emotions_column: "Pre-Assignment",
    during_emotions_column: "During Assignment",
    post_emotions_column: "Post-Assignment"
  })
  emotions_figure = px.histogram(
    emotions_data,
    x="value",
    color="variable",
    facet_col=review_column,
    facet_col_wrap=2,
    labels={
      "value": 'Emotion'    
    }
  )
  emotions_figure.for_each_annotation(lambda a: a.update(text=f'Homework {a.text.split("=")[-1].split(".")[0]}'))
  return emotions_figure

def create_sei_tab() -> dcc.Tab:
  """
  Creates the tab containing all of the student evaluation of instruction figures.

  :return: the tab containing all of the student evaluation of instruction figures
  """
  return dcc.Tab(label="Student Evaluation of Instruction", children=[
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
      html.P(children=
        """
        Also, as a qualitative researcher, I find the comments themselves to be more meaningful.
        Therefore, here's a plot of the most frequent terms in my SEI comments. 
        """
      ),
      dcc.Graph(figure=sei_comment_fig)
    ])

def create_course_eval_tab() -> dcc.Tab:
  return dcc.Tab(label="Course Evaluation Survey", children=[
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
    ])

def create_assignment_survey_tab() -> dcc.Tab:
  return dcc.Tab(label="Assignment Survey [CSE 2221]", children=[
      html.H2(children='Assignment Survey Data [CSE 2221]'),
      html.P(children=
        '''
        Throughout the course, I asked students to give me feedback on the assignments. Originally,
        these data were collected through a Carmen quiz (Autumn 2021). However, I found the Carmen 
        quiz format to be limiting, so later iterations of the quiz were administered through a Google
        Form. 
        '''
      ),
      html.H3(children='Time Spent Working on Projects'),
      html.P(children=
        '''
        One of the questions I asked my students was how long they spent on each project. Based on the responses,
        I found that students spent between 2 and 7.5 hours on each project on average. In general, these values
        trend up as the semester progresses. If we assume that students then spend an average of 4 hours on each
        project, they will conduct roughly 44 hours of work over the course of the semester. 
        '''
      ), # TODO: use an f-string to include the min and max average here
      dcc.Graph(figure=project_time_fig),
      html.H3(children='Time Spent Working on Homework Assignments'),
      html.P(children=
        '''
        Similarly, I asked students to tell me how much time they spent on the homework assignments.
        The data is fairly preliminary, so I only have the first few homework assignments. That
        said, I am finding that students spend multiple hours a week on each written assignment.
        '''
      ),
      dcc.Graph(figure=homework_time_fig),
      html.H3(children='Emotional Experience with Assignments'),
      html.P(children=
        '''
        Something new I tried in 2022 was asking students about the emotions they experienced
        before, during, and after assignments. For this, I borrowed the emotions from
        Control Value Theory and asked students retrospectively about their emotions. As it
        is early in the semester, I decided to only plot the homework assignments. Later,
        I'll update this dashboard to include the project assignments as well. 
        '''
      ),
      dcc.Graph(id="bad-scale-3", figure=emotions_fig),
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
    ])

def create_grades_tab() -> dcc.Tab:
  return dcc.Tab(label="Grades [CSE 2221]", children=[
      html.H2(children='Grades [CSE 2221]'),
      html.P(children=
        '''
        Each semester, I collect grades for 22 homework assignments, 11 projects, and 3 exams. Fortunately,
        I have graders for the bulk of it, but I grade the exams. Recently, I decided to put together a
        database of grades which allows me to generate some pretty interesting plots.
        '''
      ),
      html.H3(children='Overview'),
      dcc.Markdown(children=
        '''
        Given the different types of grade data I collect, I figured I'd start by sharing an overview
        of the grades by type. **TODO**: There is an assumption that there are three exams each semester.
        One semester, there was only one exam before COVID. Grades from the semester of COVID have been
        filtered out of the overview plots.
        '''
      ),
      dcc.Graph(figure=grade_overview_fig),
      html.P(children=
        '''
        Given the history of grades in this course, I was also interested in seeing how the grades correlated
        with attendance, which is a metric I track through Top Hat. For context, I don't force attendance,
        so the attendance scores are more of a lower bound.
        '''
      ),
      dcc.Graph(figure=grades_vs_attendance),
      html.P(children=
        '''
        At the moment, the connection between attendance and grades is pretty small. At the time of writing,
        the correlation between attendance and grades gives an R-squared of .23. I can't remember off the top of my
        head if this is a considered a good correlation in education, but online reasources point to this being
        a weak to moderate positive correlation. 
        '''
      ),
      html.P(children=
        '''
        Now, in order to get an attendance grade, you just enter some digits at the start of class.
        Participation, on the other hand, is calculated based on interaction with Top Hat. Some semesters,
        I've used Top Hat more often than others. For example, I used to use it quite a bit for Peer
        Instruction. These days, I don't use it as much, but it may be useful in demonstrating a
        strong correlation with grades. 
        '''
      ),
      dcc.Graph(figure=grades_vs_participation),
      html.P(children=
        '''
        At the time of writing, the correlation was slightly stronger with an R-squared of .28. Though,
        there's not much to brag about there. That said, it does imply that attendance and participation
        positively correlate with grades. I wouldn't go as far as to say that attending class will
        improve your grades, but I would be lying if I didn't tell you that it could. 
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
    ])

def create_app_layout(): 
  return html.Div(children=[
  html.H1(children='The Educator Dashboard'),
  html.Hr(),
  html.P(children=
    '''
    A collection of visualizations related to courses taught by myself, Jeremy Grifski, with the first two tabs dedicated
    to an overview of my ability as an instructor and the last two tabs dedicated to one of my courses. 
    '''
  ),
  dcc.Tabs([
    create_sei_tab(),
    create_course_eval_tab(),
    create_assignment_survey_tab(),
    create_grades_tab()
  ])
])

# Global app
app = dash.Dash(
  __name__,
  external_scripts=[
    {
      "src": "https://plausible.io/js/plausible.js",
      "data-domain": "educator.jeremygrifski.com"
    }
  ],
  title="The Educator Dashboard"
)
server = app.server

# Compute project statistics
assignment_survey_data = pd.read_csv('https://raw.githubusercontent.com/jrg94/personal-data/main/education/assignment-survey-data.csv')
assignment_survey_data = assignment_survey_data[assignment_survey_data[class_review_col].isna()]
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

assignment_survey_data[pre_emotions_column] = assignment_survey_data[pre_emotions_column].astype(str).apply(lambda x: x.split(";"))
assignment_survey_data[during_emotions_column] = assignment_survey_data[during_emotions_column].astype(str).apply(lambda x: x.split(";"))
assignment_survey_data[post_emotions_column] = assignment_survey_data[post_emotions_column].astype(str).apply(lambda x: x.split(";"))

# Generate assignment survey figures
project_time_fig = create_time_fig(assignment_survey_data, col=project_review_col)
homework_time_fig = create_time_fig(assignment_survey_data, col=homework_review_col)
rubric_scores_fig = create_rubric_scores_fig(assignment_survey_data)
assignment_survey_data[rubric_heading] = assignment_survey_data[rubric_heading].map(satisfaction_mapping)
rubric_fig = create_rubric_overview_fig(assignment_survey_data)
rubric_breakdown_fig = create_rubric_breakdown_fig(assignment_survey_data)
emotions_fig = create_emotions_fig(assignment_survey_data, review_column=homework_review_col)

# SEI figures
sei_data = pd.read_csv('https://raw.githubusercontent.com/jrg94/personal-data/main/education/sei-data.csv')
sei_fig = create_sei_fig(sei_data)
sei_comment_data = pd.read_csv('https://raw.githubusercontent.com/jrg94/personal-data/main/education/sei-comments.csv')
sei_comment_fig = create_sei_comment_fig(sei_comment_data)

# Course evaluation figures
course_eval_data = pd.read_csv('https://raw.githubusercontent.com/jrg94/personal-data/main/education/eval-data.csv')
course_content_fig = create_course_eval_fig(course_eval_data, "Course content", likert_scale)
skill_and_responsiveness_fig = create_course_eval_fig(course_eval_data, "Skill and responsiveness", likert_scale)
contribution_to_learning_fig = create_course_eval_fig(course_eval_data, "Contribution to learning", likert_scale_alt)

# Assignment figures
grade_data = pd.read_csv('https://raw.githubusercontent.com/jrg94/personal-data/main/education/cse-2221-grades.csv')
grade_data["Date"] = pd.to_datetime(grade_data["Date"])
grade_overview_fig = create_grades_fig(grade_data)
grades_vs_attendance = create_correlation_fig(grade_data, "TH-Attendance", "Top Hat Attendance")
grades_vs_participation = create_correlation_fig(grade_data, "Top Hat", "Top Hat Participation")
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

app.layout = create_app_layout()

if __name__ == '__main__':
  app.run_server(debug=True)
