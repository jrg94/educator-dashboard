from io import StringIO

import dash
import pandas as pd
from dash import Input, Output, callback, dcc, html

from core.constants import *
from core.data import *
from core.utils import *

dash.register_page(
    __name__,
    path='/cse2221',
    name="CSE2221",
    title="The Education Dashboard: CSE 2221"
)

# Graph Callbacks

@callback(
    Output(ID_CSE_2221_GRADE_OVERVIEW_FIG, "figure"),
    Input(ID_EDUCATION_DATA, "data")
)
def render_grade_overview_figure(education_data):
    """
    The first plot you would see on the page. It gives an overview
    of the types of assessments that have been given in CSE 2221. 
    """
    education_df = pd.read_json(StringIO(education_data))
    return create_grades_fig(education_df, 2221)


@callback(
    Output(ID_CSE_2221_HOMEWORK_GRADES_FIG, "figure"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_ASSIGNMENT_GROUP_FILTER, "value")
)
def render_assignment_calculations_figure(education_data, assignment_group):
    """
    The second plot you would see, which gives a breakdown of the averages and
    medians per assignment.
    """
    education_df = pd.read_json(StringIO(education_data))
    return create_assignment_fig(education_df, 2221, assignment_group)


@callback(
    Output(ID_CSE_2221_PROJECT_TIME_FIG, "figure"),
    Input(ID_ASSIGNMENT_SURVEY_DATA, "data")
)
def render_project_time_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_time_fig(df, assignment="Project", course=FILTER_SOFTWARE_1)


@callback(
    Output(ID_CSE_2221_HOMEWORK_TIME_FIG, "figure"),
    Input(ID_ASSIGNMENT_SURVEY_DATA, "data")
)
def render_homework_time_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_time_fig(df, assignment="Homework", course=FILTER_SOFTWARE_1)


@callback(
    Output(ID_CSE_2221_HOMEWORK_EMOTIONS_FIG, "figure"),
    Input(ID_ASSIGNMENT_SURVEY_DATA, "data")
)
def render_emotions_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_emotions_fig(
        df,
        assignment="Homework",
        course=FILTER_SOFTWARE_1
    )


@callback(
    Output(ID_CSE_2221_RUBRIC_OVERVIEW_FIG, "figure"),
    Input(ID_ASSIGNMENT_SURVEY_DATA, "data")
)
def render_rubric_overview_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_rubric_overview_fig(df)


@callback(
    Output(ID_CSE_2221_RUBRIC_BREAKDOWN_FIG, "figure"),
    Input(ID_ASSIGNMENT_SURVEY_DATA, "data")
)
def render_rubric_breakdown_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_rubric_breakdown_fig(df)


@callback(
    Output(ID_CSE_2221_RUBRIC_SCORES_FIG, "figure"),
    Input(ID_ASSIGNMENT_SURVEY_DATA, "data")
)
def render_rubric_scores_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_rubric_scores_fig(df)


@callback(
    Output(ID_CSE_2221_GRADES_ATTENDANCE_FIG, "figure"),
    Input(ID_CSE_2221_GRADE_DATA, "data")
)
def render_grades_vs_attendance_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_correlation_fig(df, "TH-Attendance", "Top Hat Attendance")


@callback(
    Output(ID_CSE_2221_GRADES_PARTICIPATION_FIG, "figure"),
    Input(ID_CSE_2221_GRADE_DATA, "data")
)
def render_grades_vs_participation_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_correlation_fig(df, "Top Hat", "Top Hat Participation")


@callback(
    Output(ID_CSE_2221_PROJECT_GRADES_FIG, "figure"),
    Input(ID_CSE_2221_GRADE_DATA, "data")
)
def render_project_calculations_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_assignment_fig(df, "Project", 10)


@callback(
    Output(ID_CSE_2221_EXAM_GRADES_FIG, "figure"),
    Input(ID_CSE_2221_GRADE_DATA, "data")
)
def render_exam_calculations_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_assignment_fig(df, "Exam", 100)


@callback(
    Output(ID_CSE_2221_MISSING_PROJECTS_FIG, "figure"),
    Input(ID_CSE_2221_GRADE_DATA, "data")
)
def render_missing_projects_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_missing_assignment_fig(df, "Project")


@callback(
    Output(ID_CSE_2221_MISSING_HOMEWORKS_FIG, "figure"),
    Input(ID_CSE_2221_GRADE_DATA, "data")
)
def render_missing_homeworks_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_missing_assignment_fig(df, "Homework")


@callback(
    Output(ID_CSE_2221_MISSING_EXAMS_FIG, "figure"),
    Input(ID_CSE_2221_GRADE_DATA, "data")
)
def render_missing_exams_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_missing_assignment_fig(df, "Exam")


@callback(
    Output(ID_CSE_2221_PROJECT_TRENDS_FIG, "figure"),
    Input(ID_CSE_2221_GRADE_DATA, "data")
)
def render_project_trends_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_project_trend_fig(df, "Project")


@callback(
    Output(ID_CSE_2221_HOMEWORK_TRENDS_FIG, "figure"),
    Input(ID_CSE_2221_GRADE_DATA, "data")
)
def render_homework_trends_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_project_trend_fig(df, "Homework")


@callback(
    Output(ID_CSE_2221_EXAM_TRENDS_FIG, "figure"),
    Input(ID_CSE_2221_GRADE_DATA, "data")
)
def render_exam_trends_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_project_trend_fig(df, "Exam")


@callback(
    Output(ID_CSE_2221_VALUE_FIG, "figure"),
    Output(ID_CSE_2221_EFFORT_FIG, "figure"),
    Input(ID_CSE_2221_GRADE_DATA, "data"),
    Input(ID_ASSIGNMENT_SURVEY_DATA, "data")
)
def render_points_per_hour_figure(jsonified_grade_data, jsonified_assignment_survey_data):
    grade_data = pd.read_json(StringIO(jsonified_grade_data))
    assignment_survey_data = pd.read_json(
        StringIO(jsonified_assignment_survey_data)
    )
    return create_value_fig(
        grade_data,
        assignment_survey_data,
        "Project",
        10,
        FILTER_SOFTWARE_1
    )
    
    
# Dropdown callbacks

@callback(
    Output(ID_ASSIGNMENT_GROUP_FILTER, "options"),
    Output(ID_ASSIGNMENT_GROUP_FILTER, "value"),
    Input(ID_EDUCATION_DATA, "data")
)
def update_dropdown_filter(education_data):
    education_df = pd.read_json(StringIO(education_data))
    education_df = education_df[education_df["Course Number"] == 2221]
    assignment_groups = sorted(education_df["Assignment Group Name"].unique())
    return assignment_groups, assignment_groups[0]


# TODO: mix in the assignment survey with the grades rather than having them
# separate
layout = html.Div([
    html.H1("CSE 2221: Software 1"),
    html.P(
        """
        Software 1 (CSE 2221) is a course I started teaching in late 2019. The 
        general purpose of the course is to teach students about software 
        components (i.e., APIs). The course, itself, is based in Java, and the 
        first third of the course focuses on Java basics. Then, in the second 
        third of the course, it focuses on problem solving techniques like 
        recursion. Then, the final third of the course focuses on data 
        structures like sets, stacks, maps, and queues.
        """
    ),
    html.P(
        """
        In terms of assessment, students spend their time on a mix of homework 
        assignments, programming projects, and exams. Specifically, students 
        complete 22 written homework assignments, 11 programming projects, and 3 
        exams. In addition, students are graded on participation. While this
        is the norm for the course, there have been assessments given from 
        time to time under various circumstances. For example, in the Spring of
        2020, we briefly switched over from midterms to quizzes. As a result, 
        the following plot details the average and median grades for all 
        categories of assessments, even if some categories are not the norm.
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_GRADE_OVERVIEW_FIG)],
        type="graph"
    ),
    html.P(
        """
        On the remainder of this page, we'll break down the assessments in
        more detail. 
        """
    ),
    html.H2("Assessment Breakdown"),
    dcc.Markdown(
        """
        Each category above can be broken down into plots of the individual
        assessments over the course of the semester. For example, the default
        plot below shows the final exam median and average in all my years of
        teaching. Feel free to use the dropdown to explore each assessment
        type. 
        """
    ),
    dcc.Dropdown(id=ID_ASSIGNMENT_GROUP_FILTER),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_HOMEWORK_GRADES_FIG)],
        type="graph"
    ),
    # TODO: look into possible causes of lack of submissions
    dcc.Markdown(
        """
        As promised, here's a look at the trend of homework completion. As with 
        projects, students tend to submit fewer assignments as the semester 
        progresses. Though, I find it interesting that there are spikes in 
        missing assignments at various points throughout the semester. I suspect 
        that the assignments that students submit least often are tied to larger 
        review assignments before exams.
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_MISSING_HOMEWORKS_FIG)],
        type="graph"
    ),
    dcc.Markdown(
        """
        In addition, here's a look at the trend of grades for the homework 
        assignments. I find this plot really interesting because it shows the 
        spread of homework grades against each semester. For instance, there is 
        quite the spread of homework averages in Autumn 2021. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_HOMEWORK_TRENDS_FIG)],
        type="graph"
    ),
    html.P(
        """
        While grades are an interesting metric, they don't exactly give us the 
        full context surrounding the student experience. After all, there are a 
        variety of reasons that a student might not do well on a certain 
        assignment or even choose not to submit one at all. As a result, I also 
        ask students to complete an assignment survey, which can be used to give 
        us a variety of other interesting data points. To kick things off, 
        here's how long students claimed they spent on each homework assignment.
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_HOMEWORK_TIME_FIG)],
        type="graph"
    ),
    html.P(
        """
        From this plot alone, it's clear that students are spending several 
        hours a week on just the homework assignments. That may be contributing 
        to the lack of submissions. 
        """
    ),
    html.P(
        """
        Something new I tried in 2022 was asking students about the emotions 
        they experienced before, during, and after assignments. For this, I 
        borrowed the emotions from Control Value Theory and asked students 
        retrospectively about their emotions. As it is early in the semester, I 
        decided to only plot the homework assignments. 
        """
    ),
    # TODO: make this plot just a single image with all of the homework
    # assignments in a single view as well as a dropdown to filter by
    # assignment. In 2024, we are not showing arrays of plots. I hate it.
    dcc.Loading(
        [
            dcc.Graph(
                id=ID_CSE_2221_HOMEWORK_EMOTIONS_FIG,
                className=CSS_FULL_SCREEN_FIG
            )
        ],
        type="graph"
    ),
    html.H2("Project Assignments"),
    html.P(
        """
        As previously stated, students are asked to complete 11 projects over 
        the course of the semester. In total, this amounts to 30% of their 
        grade. To kick things off, here are the average and median grades for 
        each project. The key takeaway here is that project 1 is a slam dunk 
        while project 8 is a bit rough.
        """
    ),

    html.P(
        """
        While medians and averages are helpful, I also think it's useful to look 
        at just how many students actually complete the projects. Or rather, 
        what percentage of students skip out on projects, and is there a trend 
        to observe? If so (spoiler alert: students turn in less work as the 
        semester progresses), that could potentially explain the low averages 
        for certain projects. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_MISSING_PROJECTS_FIG)],
        type="graph"
    ),
    dcc.Markdown(
        """
        Unfortunately, one of the drawbacks of the plots above is that they 
        aggregate the data for every semester I've taught the course. 
        Personally, I like to see trends. For example, it's helpful to know if 
        project grades are getting better over time. What I'm finding is that's 
        not the case. Frankly, I think most of this is due to grader influences, 
        but I have not investigated that.  
        """
    ),
    # TODO: consider including grader influences to the plots
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_PROJECT_TRENDS_FIG)],
        type="graph"
    ),
    html.P(
        """
        As with the homework assignments, I also surveyed my students about how 
        much time they spent on each project. Based on the responses, I found 
        that students spent between 2 and 7.5 hours on each project on average. 
        In general, these values trend up as the semester progresses. If we 
        assume that students then spend an average of 4 hours on each project, 
        they will conduct roughly 44 hours of work over the course of the 
        semester. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_PROJECT_TIME_FIG)],
        type="graph"
    ),
    dcc.Markdown(
        """
        Next, we get into the "advanced" metrics. In this case, I thought it 
        would be interesting to combine some of the data found in the assignment 
        survey with the grade data. For instance, remember how I previously 
        shared the amount of time students spent on each project on average? 
        Well, I figured it would be interesting to see how many points a student 
        could expect to earn per hour on average. Ultimately, I ended up calling 
        this metric "Expected Value" because it gives us a sense of how much 
        value a student could get out of their time. With this metric, we're 
        able to clearly see that project 1 offers the most bang for your buck. 
        Meanwhile, Project 8 offers very little in terms of value for your time. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_VALUE_FIG)],
        type="graph"
    ),
    dcc.Markdown(
        """
        Interestingly, if we invert the previous plot, we get what I'm calling 
        the "Expected Effort" metric. Rather than describing the amount of 
        points we expect to get for an hour of work, we begin talking about how 
        much time we expect to give for a point. The distinction is fairly 
        minor, but it allows us to see which projects require the most effort. 
        In this case, the roles are reversed. Project 1 requires the least 
        amount of effort, while project 8 requires the most.
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_EFFORT_FIG)],
        type="graph"
    ),
    html.P(
        """
        Perhaps unrelated to all of the wonderful plots above, I also provide 
        students with rubrics for each of their projects. I don't recall exactly 
        when I introduced the concept of rubrics, but it had to have been during 
        my second semester of teaching CSE2221 at the earliest. Out of 
        curiosity, I started asking my students about how much they liked and 
        used the rubrics. This resulted in a variety of great plots. The 
        following plot gives the overview of the rubric ratings over all 11 
        projects. In general, it appears students are fairly satisfied with the 
        rubrics.
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_RUBRIC_OVERVIEW_FIG)],
        type="graph"
    ),
    dcc.Markdown(
        """
        In case you were curious about each project individually, here is a 
        breakdown of the rubric scores for each project. 
        """
    ),
    dcc.Loading(
        [
            dcc.Graph(
                id=ID_CSE_2221_RUBRIC_BREAKDOWN_FIG,
                className=CSS_FULL_SCREEN_FIG
            )
        ],
        type="graph"
    ),
    dcc.Markdown(
        """
        And just to be perfectly explicit, I also computed average scores for 
        each rubric over all 11 projects. These scores are computed by assigning 
        Very Dissatisfied (1) to the lowest score and Very Satisfied (5) to the 
        highest score. Then, we sum up all the values and divide by the number 
        of reviews. As a result, you can see that students are generally the 
        least satisfied with the project 1 rubric and most satisfied with the 
        project 3 rubric. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_RUBRIC_SCORES_FIG)],
        type="graph"
    ),
    html.H2("Exams"),
    dcc.Markdown(
        """
        At this point, the last remaining assessments are the exams. In total, 
        there are three exams, and the general trend tends to be that scores go 
        down as the semester progresses. I haven't quite figured out why. 
        """
    ),
    dcc.Markdown(
        """
        As with projects and homework assignments, I find it important to also 
        track the percentage of students who skip exams. In general, it's pretty 
        rare for a student to skip an exam, and it's usually due to some extreme 
        circumstance. That said, the trend remains the same for exams as well 
        (i.e., fewer students attend the exams as the semester progresses).
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_MISSING_EXAMS_FIG)],
        type="graph"
    ),
    dcc.Markdown(
        """
        All that is left to talk about is the exam score trend over time. One 
        thing that is worth noting is that the exams were not consistent from 
        semester to semester. For example, you'll notice that exams 2 and 3 are 
        missing data points. The reason for this is that we eventually converted 
        those exams to online quizzes due to COVID. As a result, those quiz 
        scores are omitted. It's also worth noting that the data points in 
        Summer 2019 are from before I started teaching the course (i.e., I was 
        training to teach it at the time). As a result, the first time I taught 
        the course, my exam scores were quite low. Since then, things have 
        improved considerably. Well, except for the final exam. I'll be looking 
        to provide more ways for students to practice ahead of time. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_EXAM_TRENDS_FIG)],
        type="graph"
    ),
    html.H2("Participation and Attendance"),
    html.P(
        """
        In general, attendance is not something I really care about. That said, 
        it is something I track as a proxy for participation when needed. It's 
        also a useful tool for making sure students aren't missing. Finally, I 
        just like having the data because we can do more interesting analyses. 
        For example, I was interested in seeing how the grades correlated with 
        attendance as follows:
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_GRADES_ATTENDANCE_FIG)],
        type="graph"
    ),
    html.P(
        """
        At the moment, the connection between attendance and grades is pretty 
        small. At the time of writing, the correlation between attendance and 
        grades gives an R-squared of .13. I can't remember off the top of my
        head if this is a considered a good correlation in education, but online 
        resources point to this being a weak positive correlation. 
        """
    ),
    html.P(
        """
        Now, in order to get an attendance grade, you just enter some digits 
        into TopHat at the start of class. Participation, on the other hand, is 
        calculated based on interaction with Top Hat. Some semesters, I've used 
        Top Hat more often than others. For example, I used to use it quite a 
        bit for Peer Instruction. These days, I don't use it as much, but it may 
        be useful in demonstrating a strong correlation with grades. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_GRADES_PARTICIPATION_FIG)],
        type="graph"
    ),
    html.P(
        """
        At the time of writing, the correlation was slightly stronger with an 
        R-squared of .30. Though, there's not much to brag about there. That 
        said, it does imply that attendance and participation positively 
        correlate with grades. I wouldn't go as far as to say that attending 
        class will improve your grades, but I would be lying if I didn't tell 
        you that it could. 
        """
    ),
    load_cse2221_grade_data(),
    load_assignment_survey_data(),
    load_education_data()
])
