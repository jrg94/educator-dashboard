from io import StringIO

import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

from core.constants import *
from core.data import *

dash.register_page(
    __name__,
    path=HISTORY_PAGE_PATH,
    name=HISTORY_PAGE_NAME,
    title=HISTORY_PAGE_TITLE
)

# Graph callbacks

@callback(
    Output(ID_COURSE_HISTORY_LIST, "children"),
    Input(ID_HISTORY_DATA, "data")
)
def render_course_history_list(history_data: str) -> list[html.Li]:
    """
    Creates a list of all the courses I've taught with key information.

    :param history_data: the jsonified teaching history
    :return: a list of list item objects
    """
    history_df = pd.read_json(StringIO(history_data))

    list_items = []
    course_ids = history_df[COLUMN_COURSE_ID].unique()
    course_ids.sort()
    for course_id in course_ids:
        filtered_df = history_df[history_df[COLUMN_COURSE_ID] == course_id]
        course_department = filtered_df.iloc[0][COLUMN_COURSE_DEPARTMENT]
        course_number = filtered_df.iloc[0][COLUMN_COURSE_NUMBER]
        course_name = filtered_df.iloc[0][COLUMN_COURSE_NAME]
        min_year = filtered_df[COLUMN_SEMESTER_YEAR].min()
        max_year = filtered_df[COLUMN_SEMESTER_YEAR].max()
        title = filtered_df.iloc[0][COLUMN_EDUCATOR_TITLE]
        list_item = html.Li(
            f"[{min_year} - {max_year}] {course_department} {course_number}—{course_name} as a {title}"
        )
        list_items.append(list_item)

    return list_items


@callback(
    Output(ID_TIME_COUNTS_FIG, "figure"),
    Input(ID_HISTORY_DATA, "data")
)
def render_time_counts_fig(history_data: str) -> go.Figure:
    """
    Creates a figure of the most common section times in my teaching history.

    :param history_data: the jsonified teaching history
    :return: a bar graph
    """
    history_df = pd.read_json(StringIO(history_data))
    history_df = history_df[history_df[COLUMN_COURSE_TYPE] == "Lecture"]
    history_df = history_df.sort_values(by=COLUMN_SECTION_START_TIME)

    time_counts_fig = go.Figure(layout=dict(template='plotly'))
    time_counts_fig = px.histogram(
        history_df,
        x=COLUMN_SECTION_START_TIME
    )

    return time_counts_fig


@callback(
    Output(ID_ROOM_COUNTS_FIG, "figure"),
    Input(ID_HISTORY_DATA, "data")
)
def render_room_counts_fig(history_data: str) -> go.Figure:
    """
    Creates a figure of the most common classrooms in my teaching history.

    :param history_data: the jsonified teaching history
    :return: a bar graph
    """
    history_df = pd.read_json(StringIO(history_data))
    history_df = history_df[history_df[COLUMN_COURSE_TYPE] == "Lecture"]
    history_df[COLUMN_CLASSROOM] = history_df[COLUMN_SECTION_BUILDING] + " " + history_df[COLUMN_SECTION_ROOM_NUMBER]
    history_df = history_df.sort_values(by=COLUMN_CLASSROOM)

    time_counts_fig = go.Figure(layout=dict(template='plotly'))
    time_counts_fig = px.histogram(
        history_df,
        x=COLUMN_CLASSROOM
    )

    return time_counts_fig


@callback(
    Output(ID_STUDENT_COUNTS_FIG, "figure"),
    Input(ID_HISTORY_DATA, "data")
)
def render_cumulative_enrollment_fig(history_data: str) -> go.Figure:
    """
    Creates a figure of the number of students I've acummulated over time.

    :param history_data: the jsonified teaching history
    :return: a bar graph
    """
    history_df = pd.read_json(StringIO(history_data))
    history_df = history_df[history_df[COLUMN_COURSE_TYPE] == "Lecture"]
    history_df[COLUMN_SEMESTER] = history_df[COLUMN_SEMESTER_SEASON] + " " + history_df[COLUMN_SEMESTER_YEAR].astype(str)
    history_df = history_df.groupby(COLUMN_SEMESTER).agg({
        COLUMN_ENROLLMENT_TOTAL: "sum", 
        COLUMN_SEMESTER_ID: "first"
    }).reset_index()
    history_df = history_df.sort_values(by=COLUMN_SEMESTER_ID)
    history_df[COLUMN_CUMULATIVE_ENROLLMENT_TOTAL] = history_df[COLUMN_ENROLLMENT_TOTAL].cumsum()

    time_counts_fig = go.Figure(layout=dict(template='plotly'))
    time_counts_fig = px.bar(
        history_df,
        x=COLUMN_SEMESTER,
        y=COLUMN_CUMULATIVE_ENROLLMENT_TOTAL
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
    html.Ul(id=ID_COURSE_HISTORY_LIST),
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
