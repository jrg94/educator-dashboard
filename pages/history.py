from io import StringIO

import dash
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Input, Output, callback, dcc, html

from core.constants import (COLUMN_COURSE_DEPARTMENT, COLUMN_COURSE_ID,
                            COLUMN_COURSE_NUMBER, COLUMN_SEMESTER_ID, COLUMN_SEMESTER_SEASON, COLUMN_SEMESTER_YEAR,
                            ID_HISTORY_DATA, ID_ROOM_COUNTS_FIG, ID_STUDENT_COUNTS_FIG, ID_TIME_COUNTS_FIG)
from core.data import load_teaching_history

dash.register_page(
    __name__,
    path='/history',
    name="History",
    title="The Educator Dashboard: History"
)

# Graph callbacks

@callback(
    Output("test", "children"),
    Input(ID_HISTORY_DATA, "data")
)
def render_course_history_list(history_data):
    history_df = pd.read_json(StringIO(history_data))
    
    list_items = []
    course_ids = history_df[COLUMN_COURSE_ID].unique()
    course_ids.sort()
    for course_id in course_ids:
        filtered_df = history_df[history_df[COLUMN_COURSE_ID] == course_id]
        course_department = filtered_df.iloc[0][COLUMN_COURSE_DEPARTMENT]
        course_number = filtered_df.iloc[0][COLUMN_COURSE_NUMBER]
        course_name = filtered_df.iloc[0]["Course Name"]
        min_year = filtered_df[COLUMN_SEMESTER_YEAR].min()
        max_year = filtered_df[COLUMN_SEMESTER_YEAR].max()
        title = filtered_df.iloc[0]["Educator Title"]
        list_item = html.Li(
            f"[{min_year} - {max_year}] {course_department} {course_number}—{course_name} as a {title}"
        )
        list_items.append(list_item)
    
    return list_items


@callback(
    Output(ID_TIME_COUNTS_FIG, "figure"),
    Input(ID_HISTORY_DATA, "data")
)
def render_time_counts_fig(history_data):
    history_df = pd.read_json(StringIO(history_data))
    history_df = history_df[history_df["Course Type"] == "Lecture"]
    history_df = history_df.sort_values(by="Section Start Time")
    
    time_counts_fig = go.Figure(layout=dict(template='plotly'))
    time_counts_fig = px.histogram(
        history_df,
        x="Section Start Time"
    ) 
    
    return time_counts_fig


@callback(
    Output(ID_ROOM_COUNTS_FIG, "figure"),
    Input(ID_HISTORY_DATA, "data")
)
def render_time_counts_fig(history_data):
    history_df = pd.read_json(StringIO(history_data))
    history_df = history_df[history_df["Course Type"] == "Lecture"]
    history_df["Classroom"] = history_df["Section Building"] + " " + history_df["Section Room Number"]
    history_df = history_df.sort_values(by="Classroom")
    
    time_counts_fig = go.Figure(layout=dict(template='plotly'))
    time_counts_fig = px.histogram(
        history_df,
        x="Classroom"
    ) 
    
    return time_counts_fig


@callback(
    Output(ID_STUDENT_COUNTS_FIG, "figure"),
    Input(ID_HISTORY_DATA, "data")
)
def render_time_counts_fig(history_data):
    history_df = pd.read_json(StringIO(history_data))
    history_df = history_df[history_df["Course Type"] == "Lecture"]
    history_df["Semester"] = history_df[COLUMN_SEMESTER_SEASON] + " " + history_df[COLUMN_SEMESTER_YEAR].astype(str)
    history_df = history_df.groupby("Semester").agg({"Enrollment Total": "sum", "Semester ID": "first"}).reset_index()
    history_df = history_df.sort_values(by=COLUMN_SEMESTER_ID)
    history_df["Cumulative Enrollment Total"] = history_df["Enrollment Total"].cumsum()
    
    time_counts_fig = go.Figure(layout=dict(template='plotly'))
    time_counts_fig = px.bar(
        history_df,
        x="Semester",
        y="Cumulative Enrollment Total"
    ) 
    
    return time_counts_fig


layout = html.Div([
    html.H1("History"),
    html.P(
        """
        To help track my progress as an educator and provide some level of 
        transparency around the development of my courses, I've created this 
        history document. It details my teaching history and all of the things
        I've changed over time. 
        """
    ),
    html.P(
        """
        Since 2018, I've taught in various capacities. For example, the
        following list details all of the courses I've taught.
        """
    ),
    html.Ul(id="test"),
    html.P(
        """
        At this point in my career, I've taught many students. To get a feel for
        just how many, I've plotted the cumulative number of students
        over time below.
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_STUDENT_COUNTS_FIG)],
        type="graph"
    ),
    # TODO: plot number of students over time as a cumulative?
    html.P(
        """
        On the remainder of this page, I'll share some interesting visualizations
        of my teaching history.
        """
    ),
    html.H2("Schedule Prediction"),
    html.P(
        """
        Every semester I get a wave of students asking me when I'll be teaching
        in the future. Because I have very little say in my schedule, I almost
        never know what my future schedule is going to look like until a week
        or two before each semester. However, I thought it would be interesting
        to look at my most common teaching times and rooms to see if I can
        better help students predict my future schedule. To start, here's a
        distribution of course times.
        """  
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_TIME_COUNTS_FIG)],
        type="graph"
    ),
    html.P(
        """
        Similarly, here's the distribution of classrooms that I've lectured in.
        """  
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_ROOM_COUNTS_FIG)],
        type="graph"
    ),
    html.H2("Hall of Fame"),
    html.P(
        """
        Because I've taught so many students, I just wanted to share some
        information about some of the students who have gone on to do great
        things. I'd also like to share some ways I help students get there. 
        """  
    ),
    # TODO: include graph around letters of recommendation
    html.H2("Course Changes"),
    html.P(
        """
        The last thing I'd like to document on this page is a list of changes
        I've made to my courses over the years. 
        """
    ),
    dcc.Markdown(
        """
        - Summer 2024
            - Overhauled dashboard to make use of pages and dropdowns
            - Added information about teaching history
        - Spring 2024
            - Started tracking patch notes
            - Drafted and piloted a VSCode monorepo for software 2
            - Updated dashboard to include software 2 statistics
            - Created slides for all lectures of software 2
            - Reworked site to make use of structured data files
        - Autumn 2023
            - Started teaching software 2 (CSE 2231)
            - Created checklists for all 10 projects in software 2
            - Created rubrics for all 10 projects in software 2
            - Piloted a portfolio project in software 2 where students create their own OSU component
            - Offered the portfolio project as a midterm exam replacement option
            - Converted exams to online format using Carmen quizzes
            - Extended duration of exams from 55 minutes to 80 minutes
        - Summer 2023
            - Trained to teach software 2 (CSE 2231)
            - Create homework solutions for all 10 projects in software 2
        - Spring 2023
            - Started allowing students in software 1 to resubmit projects after making corrections
            - Created checklists for all 11 projects in software 1
        - Spring 2022
            - Created checklists for all 11 projects in software 1
        - Autumn 2021
            - Created rubrics for all 11 projects in software 1
            - Started creating homework solutions for software 1
        - Spring 2020
            - Held a Small Group Instructional Diagnostic (SGID) with my software 1 class
            - Completed a portion of the semester online due to COVID
        - Autumn 2019
            - Started teaching software 1 (CSE 2221)
            - Administered grading guidelines to teaching assistants only
        - Summer 2019
            - Trained to teach software 1 (CSE 2221)
        - Autumn 2018
            - Started teaching introduction to Java (CSE 1223)
            - Learned to always ask students to request extensions in writing
        """
    ),
    html.P(
        """
        And, there you have it! I'll continue to update this site as I always
        do to show my dedication to education over time. 
        """
    ),
    load_teaching_history()
])
