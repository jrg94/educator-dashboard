from io import StringIO
import dash
from dash import Input, Output, callback, html
import pandas as pd

from core.constants import ID_HISTORY_DATA
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
    history_df = history_df.groupby(["Course ID"]).first()
    history_df = history_df.sort_values(by="Semester Year")
    items = [
        html.Li(f"{row['Course Department']} {row['Course Number']}—{row['Course Name']}") 
        for _, row in history_df.iterrows()
    ]
    return items

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
