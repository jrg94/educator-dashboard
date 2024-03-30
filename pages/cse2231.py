from io import StringIO

import dash
import pandas as pd
from dash import Input, Output, callback, dcc, html

from core.constants import *
from core.data import *
from core.utils import *

dash.register_page(
    __name__,
    path='/cse2231',
    name="CSE2231",
    title="The Education Dashboard: CSE 2231"
)

@callback(
    Output(ID_CSE_2231_GRADES_OVERVIEW_FIG, "figure"),
    Input(ID_EDUCATION_DATA, "data")
)
def render_grade_overview_figure(education_data):
    education_df = pd.read_json(StringIO(education_data))
    return create_grades_fig(education_df, 2231)


@callback(
    Output(ID_CSE_2231_HOMEWORK_GRADES_FIG, "figure"),
    Input(ID_CSE_2231_GRADE_DATA, "data")
)
def render_homework_calculations_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_assignment_fig(df, "Homework", 2)


@callback(
    Output(ID_CSE_2231_HOMEWORK_TIME_FIG, "figure"),
    Input(ID_ASSIGNMENT_SURVEY_DATA, "data")
)
def render_homework_time_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_time_fig(df, assignment="Homework", course=FILTER_SOFTWARE_2)


@callback(
    Output(ID_CSE_2231_MISSING_HOMEWORKS_FIG, "figure"),
    Input(ID_CSE_2231_GRADE_DATA, "data")
)
def render_missing_homeworks_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_missing_assignment_fig(df, "Homework")


@callback(
    Output(ID_CSE_2231_PROJECT_GRADES_FIG, "figure"),
    Input(ID_CSE_2231_GRADE_DATA, "data")
)
def render_project_calculations_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_assignment_fig(df, "Project", 10)


@callback(
    Output(ID_CSE_2231_PROJECT_TIME_FIG, "figure"),
    Input(ID_ASSIGNMENT_SURVEY_DATA, "data")
)
def render_project_time_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_time_fig(df, assignment="Project", course=FILTER_SOFTWARE_2)


@callback(
    Output(ID_CSE_2231_MISSING_PROJECTS_FIG, "figure"),
    Input(ID_CSE_2231_GRADE_DATA, "data")
)
def render_missing_homeworks_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_missing_assignment_fig(df, "Project")


@callback(
    Output(ID_CSE_2231_EXAM_GRADES_FIG, "figure"),
    Input(ID_CSE_2231_GRADE_DATA, "data")
)
def render_exam_calculations_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_assignment_fig(df, "Exam", 100)


@callback(
    Output(ID_CSE_2231_MISSING_EXAMS_FIG, "figure"),
    Input(ID_CSE_2231_GRADE_DATA, "data")
)
def render_missing_homeworks_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_missing_assignment_fig(df, "Exam")


layout = html.Div([
    html.H1("CSE 2231: Software 2"),
    html.P(
        """
        Software 2 (CSE 2231) is a course I started teaching in Autumn 2023. 
        Naturally, it follows software 1, which is a course I previously taught.
        The purpose of software 2 is to flip the script on students. No longer
        are they clients of APIs (though, there is no avoiding this). Instead,
        they're implementors of those APIs. 
        """
    ),
    html.P(
        """
        In terms of course design, software 2 is broken into three main parts.
        During the first part of the course, students focus on what we call
        "kernel implementations", which are the students' first exposure to
        developing APIs. I've deemed the second part of the course "compilers"
        because it focuses primarily on compiler techniques like parsing, 
        tokenizing, and code generation. Finally, the last third of the course
        focuses on what we call "loose ends", which is basically everything
        we've neglected over the course sequence about the Java language. 
        """
    ),
    html.P(
        """
        As far as assessments are concerned, the expectations are roughly the
        same as software 1. In general, students complete a series of homework
        assignments, projects, and exams. However, there are significantly
        more homework assignments in software 2 at a total of 37. There is
        also one fewer project at a total of 10, which are completed in pairs.
        Meanwhile, exam expectations are exactly the same. In addition, students
        are assessed on participation. Here's a quick overview of the
        averages for each of these assessments.
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_GRADES_OVERVIEW_FIG)],
        type="graph"
    ),
    html.P(
        """
        As always, the remainder of this page is dedicated to a breakdown
        of each assessment type. 
        """
    ),
    html.H2("Homework Assignments"),
    html.P(
        """
        Once again, students are tasked with completing 37 written homework
        assignments in software 2. Given a 15-week semester, this means students
        are asked to complete roughly 2 written assignments a week. However, to
        be completely fair, most homework assignments are just lab preparation,
        so all of the work is closely connected to the day-to-day. 
        """
    ),
    html.P(
        """
        Like software 1, homework assignments take up just 6% of the overall
        grade. In addition, each assignment is graded on completion, not 
        correctness. Therefore, as you'll see below, the median homework grades
        are high (i.e., over half the class always submits something). 
        Therefore, the average grade is usually most influence by lack of 
        submissions (as you'll see later).
        """
    ),  
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_HOMEWORK_GRADES_FIG)],
        type="graph"
    ),
    html.P(
        """
        As promised, here's what the trend of missing assignments looks like for
        homeworks. One that jumps right out at me is homework 27! I wonder
        what's going on there. I can't say for certain why this assignment is
        most often forgotten, but it's one of two assignments due the same day 
        as a project. The other assignment being homework 14, which doesn't look
        out of the ordinary. Homework 27 is, however, the fourth homework of
        the week, which might play a role in its lack of submissions. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_MISSING_HOMEWORKS_FIG)],
        type="graph"
    ),
    html.P(
        """
        As with software 1, I also share a survey with my software 2 students to 
        get a feel for how long it takes them to complete homeworks. 
        Unfortunately, this semester, students didn't really complete it. That 
        said, there are a few responses. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_HOMEWORK_TIME_FIG)],
        type="graph"
    ),
    html.H2("Project Assignments"),
    html.P(
        """
        As far as projects are concerned in software 2, there are 10 in total.
        However, unlike software 1, 9 of the 10 projects are completed in pairs.
        In total, these 10 projects make up 30% of each student's final grade. 
        The following plot gives an overview of the average and media grades for
        each project. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_PROJECT_GRADES_FIG)],
        type="graph"
    ),
    html.P(
        """
        Something I should mention at this point is that project grades are
        very high on average compared to software 1. There are variety of
        potential reasons for this. On one hand, this could be due to the 
        student teams, which could result in students checking over each other's 
        work (i.e., rising tides lift all boats kind of argument). On the other 
        hand, I have more recently started allowing resubmissions of projects, 
        so students can fix issues in their code. The latter is more likely as 
        you see a clear drop off in averages for projects near the end of the
        semester. These projects cannot be resubmitted because I have a hard
        deadline for all submissions as the last day of class. 
        """
    ),
    html.P(
        """
        Not to muddy the waters, but another variable at play could be the
        rubrics. I've been running rubrics for a long time, so I don't 
        anticipate then having a noticeable effect on software 2 over software 
        1. That said, I do think they play a role in higher grades overview. 
        """
    ),
    html.P(
        """
        At any rate, let's take a look at how many projects are missing. You
        may be surprised to find out that once students are in teams the number
        of projects that go unsubmitted is near zero. I would say that
        certainly contributes to much higher grades overall. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_MISSING_PROJECTS_FIG)],
        type="graph"
    ),
    html.P(
        """
        Of course, in addition to grades, I find it important to also consider
        how long it takes to complete each project. Unfortunately, almost no
        students have contributed to this knowledge. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_PROJECT_TIME_FIG)],
        type="graph"
    ),
    html.H2("Exams"),
    html.P(
        """
        As in software 1, software 2 features three exams that account for 60%
        of the students' overall grade. Here's a quick overview of the grades
        for each exam. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_EXAM_GRADES_FIG)],
        type="graph"
    ),
    html.P(
        """
        At a quick glance, the trend of exam grades going down over time seems
        to hold in software 2 as well. However, you may notice high exam scores.
        I am actually somewhat surprised by this as I didn't do anything
        different in terms of exam design, even though I have that power now.
        That said, I did shift to online exams for the second and third exams,
        which demonstrated no real difference in overall grades to me (though,
        maybe a 5% increase overall). 
        """
    ),
    html.P(
        """
        As usual, I have my theories about the differences in overall grades
        between the two courses. One theory is that software 2 has students
        that have beaten the challenge of software 1 and are therefore better
        prepared for software 2. However, I don't really buy that theory because
        there are a few things I've done differently than before. To start, 
        I offer retakes for folks who perform particularly poorly. That's not
        really new, but I felt like I had more students take me up on that offer
        than before. Second, I piloted a new project this semester, which I used
        as an exam replacement. Students in general got near perfect grades on 
        the extra project, so it's no surprise to me that the midterm grades
        were so high. If you want to truly compare software 1 grades against
        software 2 grades, you'd have to compare the finals. That said, I'll
        save those analytics for another day. 
        """
    ),
    html.P(
        """
        In the meantime, here's the data on missing exams.
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2231_MISSING_EXAMS_FIG)],
        type="graph"
    ),
    html.P(
        """
        Missing exams were already an exceedingly rare occurence, but the shift
        to online exams seems to have eliminated the problem almost entirely.
        """
    ),
    html.H2("Participation and Attendance"),
    html.P(
        """
        Participation is not something that I tracked this year, but I did track
        attendance. Unfortunately, I failed to export attendance grades as a
        percentage and instead exported as days attended. As a result, existing
        plots won't work as expected, so there are none here. 
        """
    ),
    load_cse2231_grade_data(),
    load_assignment_survey_data(),
    load_education_data()
])
