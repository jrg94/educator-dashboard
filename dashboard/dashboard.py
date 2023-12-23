import callbacks
import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from data import (load_assignment_survey_data, load_grade_data, load_sei_comments_data,
                  load_sei_data, load_course_eval_data)

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

def create_sei_tab() -> dcc.Tab:
    """
    Creates the tab containing all of the student evaluation of instruction figures.

    :return: the tab containing all of the student evaluation of instruction figures
    """
    return dcc.Tab(
        label="Student Evaluation of Instruction", 
        children=[
            html.H2('Student Evaluation of Instruction'),
            dcc.Markdown(
                '''
                Each semester, the university asks students to fill out a survey about the instruction for the course.
                These data are anonymized and provided as averages for each question. Here is the breakdown of my scores
                against the scores for various cohorts including my department, my college, and my university. In general,
                I outperform all three cohorts, but I'm noticing a downward trend in course organization. For context,
                I taught CSE 1223 in the Fall of 2018 and the Spring of 2019. I've been teaching CSE 2221 ever since, with
                a year gap for research during Autumn 2020 and Spring 2021. **TODO**: the plot should clearly show the
                gap in teaching. 
                '''
            ),
            dcc.Graph(id="sei-stats"),
            html.P(
                """
                Also, as a qualitative researcher, I find the comments themselves to be more meaningful.
                Therefore, here's a plot of the most frequent terms in my SEI comments. 
                """
            ),
            dcc.Graph(id="sei-comments"),
            load_sei_data(),
            load_sei_comments_data()
        ]
    )


def create_course_eval_tab() -> dcc.Tab:
    return dcc.Tab(
        label="Course Evaluation Survey",
        children=[
            html.H2('Course Evaluation Survey Data'),
            dcc.Markdown(
                '''
                At the end of each semester, I ask students to give me feedback on the course. These data are collected
                through a Google Form. Questions are broken down into different areas which include feedback on
                course content, my skill and responsiveness, and the course's contribution to learning. **Note**:
                future work is being done to ensure the following plots feature review counts as seen in the assignment
                survey data. 
                '''
            ),
            html.H3('Course Content'),
            html.P(
                '''
                One way the course was evaluated was by asking students to rate their satisfaction with the course content.
                In short, there are four questions that I ask that cover topics that range from learning objectives to
                organization. Generally, the students that choose to fill out the course survey seem to be satisfied with 
                the course content. For example, at this time, there have been no "strongly disagree" responses. 
                '''
            ),
            dcc.Graph(id="course-content"),
            html.H3('Skill and Responsiveness of the Instructor'),
            html.P(
                '''
                Another way the course was evaluated was by asking students to rate their satisfaction with the instructor, me.
                This time around, I ask six questions which range from satisfaction with time usage to satisfaction
                with grading. Again, students are generally happy with my instruction. In fact, they're often more happy
                with my instruction than the course content itself. 
                '''
            ),
            dcc.Graph(id="skill-and-responsiveness"),
            html.H3('Contribution to Learning'),
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
            dcc.Graph(id="contribution-to-learning"),
            load_course_eval_data()
        ]
    )

def create_assignment_survey_tab() -> dcc.Tab:
  return dcc.Tab(
      label="Assignment Survey [CSE 2221]", 
      children=[
        html.H2('Assignment Survey Data [CSE 2221]'),
        html.P(
            '''
            Throughout the course, I asked students to give me feedback on the assignments. Originally,
            these data were collected through a Carmen quiz (Autumn 2021). However, I found the Carmen 
            quiz format to be limiting, so later iterations of the quiz were administered through a Google
            Form. 
            '''
        ),
        html.H3('Time Spent Working on Projects'),
        html.P(
            '''
            One of the questions I asked my students was how long they spent on each project. Based on the responses,
            I found that students spent between 2 and 7.5 hours on each project on average. In general, these values
            trend up as the semester progresses. If we assume that students then spend an average of 4 hours on each
            project, they will conduct roughly 44 hours of work over the course of the semester. 
            '''
        ), # TODO: use an f-string to include the min and max average here
        dcc.Graph(id="project-time"),
        html.H3('Time Spent Working on Homework Assignments'),
        html.P(
            '''
            Similarly, I asked students to tell me how much time they spent on the homework assignments.
            The data is fairly preliminary, so I only have the first few homework assignments. That
            said, I am finding that students spend multiple hours a week on each written assignment.
            '''
        ),
        dcc.Graph(id="homework-time"),
        html.H3('Emotional Experience with Assignments'),
        html.P(
            '''
            Something new I tried in 2022 was asking students about the emotions they experienced
            before, during, and after assignments. For this, I borrowed the emotions from
            Control Value Theory and asked students retrospectively about their emotions. As it
            is early in the semester, I decided to only plot the homework assignments. Later,
            I'll update this dashboard to include the project assignments as well. 
            '''
        ),
        dcc.Graph(id="emotions"),
        html.H3('Rubric Evaluation'),
        html.P(
            """
            Another question I asked my students was about their satisfaction with the rubrics for each project. 
            The following plot gives the overview of the rubric ratings over all 11 projects. In general,
            it appears students are fairly satisfied with the rubrics.
            """
        ),
        dcc.Graph(id="rubric-overview"),
        dcc.Markdown(
            """
            In case you were curious about each project individually, here is a breakdown of the rubric scores for each project. 
            """
        ),
        dcc.Graph(id="rubric-breakdown"),
        dcc.Markdown(
            """
            And just to be perfectly explicit, I also computed average scores for each rubric over all 11 projects.
            These scores are computed by assigning Very Dissatisfied (1) to the lowest score and Very Satisfied (5) 
            to the highest score. Then, we sum up all the values and divide by the number of reviews. As a result,
            you can see that students are generally the least satisfied with the project 1 rubric and most satisfied
            with the project 3 rubric. 
            """
        ),
        dcc.Graph(id="rubric-scores"),
        load_assignment_survey_data()
    ]
)

def create_grades_tab() -> dcc.Tab:
  return dcc.Tab(
      label="Grades [CSE 2221]", 
      children=[
        html.H2('Grades [CSE 2221]'),
        html.P(
            '''
            Each semester, I collect grades for 22 homework assignments, 11 projects, and 3 exams. Fortunately,
            I have graders for the bulk of it, but I grade the exams. Recently, I decided to put together a
            database of grades which allows me to generate some pretty interesting plots.
            '''
        ),
        html.H3('Overview'),
        dcc.Markdown(
            '''
            Given the different types of grade data I collect, I figured I'd start by sharing an overview
            of the grades by type. **TODO**: There is an assumption that there are three exams each semester.
            One semester, there was only one exam before COVID. Grades from the semester of COVID have been
            filtered out of the overview plots.
            '''
        ),
        dcc.Graph(id="grade-overview"),
        html.P(
            '''
            Given the history of grades in this course, I was also interested in seeing how the grades correlated
            with attendance, which is a metric I track through Top Hat. For context, I don't force attendance,
            so the attendance scores are more of a lower bound.
            '''
        ),
        dcc.Graph(id="grade-vs-attendance"),
        html.P(
            '''
            At the moment, the connection between attendance and grades is pretty small. At the time of writing,
            the correlation between attendance and grades gives an R-squared of .23. I can't remember off the top of my
            head if this is a considered a good correlation in education, but online reasources point to this being
            a weak to moderate positive correlation. 
            '''
        ),
        html.P(
            '''
            Now, in order to get an attendance grade, you just enter some digits at the start of class.
            Participation, on the other hand, is calculated based on interaction with Top Hat. Some semesters,
            I've used Top Hat more often than others. For example, I used to use it quite a bit for Peer
            Instruction. These days, I don't use it as much, but it may be useful in demonstrating a
            strong correlation with grades. 
            '''
        ),
        dcc.Graph(id="grades-vs-participation"),
        html.P(
            '''
            At the time of writing, the correlation was slightly stronger with an R-squared of .28. Though,
            there's not much to brag about there. That said, it does imply that attendance and participation
            positively correlate with grades. I wouldn't go as far as to say that attending class will
            improve your grades, but I would be lying if I didn't tell you that it could. 
            '''
        ),
        html.H3('Project Grades'),
        html.P(
            '''
            To start, I'd like to talk about the 11 projects. Specifically, I'll share the average and median grade
            for each project. The key takeaway here is that project 1 is a slam dunk while project 8 is a bit rough.
            '''
        ),
        dcc.Graph(id="project-calculations"),
        html.P(children=
            '''
            While medians and averages are helpful, I also think it's useful to look at just how many students
            actually complete the projects. Or rather, what percentage of students skip out on projects, and
            is there a trend to observe? If so (spoiler alert: students turn in less work as the semester 
            progresses), that could potentially explain the low averages for certain projects. 
            '''
        ),
        dcc.Graph(id="missing-project"),
        dcc.Markdown(
            '''
            Unfortunately, one of the drawbacks of the plots above is that they aggregate the data for every
            semester I've taught the course. Personally, I like to see trends, right? For example, it's 
            helpful to know if project grades are getting better over time. What I'm finding is that's not
            the case. Frankly, I think most of this is due to grader influences, but I have not investigated
            that. **TODO**: I should include grader influences in the plot. 
            '''
        ),
        dcc.Graph(id="project-trends"),
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
        dcc.Graph(id="project-points-per-hour"),
        dcc.Markdown(
            '''
            Interestingly, if we invert the previous plot, we get what I'm calling the "Expected Effort" metric.
            Rather than describing the amount of points we expect to get for an hour of work, we begin talking
            about how much time we expect to give for a point. The distinction is fairly minor, but it allows
            us to see which projects require the most effort. In this case, the roles are reversed. Project 1
            requires the least amount of effort, while project 8 requires the most.
            '''
        ),
        dcc.Graph(id="project-hours-per-point"),
        html.H3(children='Homework Grades'),
        dcc.Markdown(
            '''
            In addition to 11 projects, we also assign 22 homework assignments. These assignments are graded
            on completion for a maximum of 2 points each. Naturally, here's the breakdown of average and median
            scores for each assignment. As you can see, students generally get full credit, but there are some
            students who pull the average down with incomplete assignments (more on that later).
            '''
        ),
        dcc.Graph(id="homework-calculations"),
        dcc.Markdown(
            '''
            As promised, here's a look at the trend of homework completion. As with projects, students tend
            to submit fewer assignments as the semester progresses. Though, I find it interesting that there
            are spikes in missing assignments at various points throughout the semester. I suspect that the 
            assignments that students submit least often are tied to larger review assignments before exams.
            **TODO**: I should look into this more.
            '''
        ),
        dcc.Graph(id="missing-homeworks"),
        dcc.Markdown(
            '''
            Finally, here's a look at the trend of grades for the homework assignments. I find this plot really
            interesting because it shows the spread of homework grades against each semester. For instance,
            there is quite the spread of homework averages in Autumn 2021. 
            '''
        ),
        dcc.Graph(id="homework-trends"),
        html.H3(children='Exam Grades'),
        dcc.Markdown(
            '''
            At this point, all that is left to discuss are the exams. In total, there are three exams, and the
            general trend tends to be that scores go down as the semester progresses. I haven't quite figured
            out why. 
            '''
        ),
        dcc.Graph(id="exams-calculations"),
        dcc.Markdown(
            '''
            As with projects and homework assignments, I find it important to also track the percentage of students
            who skip exams. In general, it's pretty rare for a student to skip an exam, and it's usually due to some
            extreme circumstance. That said, the trend remains the same for exams as well (i.e., fewer students attend
            the exams as the semester progresses).
            '''
        ),
        dcc.Graph(id="missing-exams"),
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
        dcc.Graph(id="exam-trends"),
        load_grade_data()
    ]
)

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

app.layout = create_app_layout()

if __name__ == '__main__':
  app.run_server(debug=True)
