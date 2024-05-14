from io import StringIO
import dash
from dash import Input, Output, callback, html
import pandas as pd

from core.constants import COLUMN_COURSE_ID, ID_HISTORY_DATA
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
        course_department = filtered_df.iloc[0]["Course Department"]
        course_number = filtered_df.iloc[0]["Course Number"]
        course_name = filtered_df.iloc[0]["Course Name"]
        min_year = filtered_df["Semester Year"].min()
        max_year = filtered_df["Semester Year"].max()
        title = filtered_df.iloc[0]["Educator Title"]
        list_item = html.Li(
            f"[{min_year} - {max_year}] {course_department} {course_number}—{course_name} as a {title}"
        )
        list_items.append(list_item)
    
    return list_items

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
    load_teaching_history()
])
