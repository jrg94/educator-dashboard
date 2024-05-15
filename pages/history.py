from io import StringIO

import dash
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

from core.constants import (COLUMN_COURSE_DEPARTMENT, COLUMN_COURSE_ID,
                            COLUMN_COURSE_NUMBER, COLUMN_SEMESTER_YEAR,
                            ID_HISTORY_DATA, ID_TIME_COUNTS_FIG)
from core.data import load_teaching_history

dash.register_page(
    __name__,
    path='/history',
    name="History",
    title="The Educator Dashboard: History"
)

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
    
    time_counts_fig = go.Figure(layout=dict(template='plotly'))    
    
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
    load_teaching_history()
])
