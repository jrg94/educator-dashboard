from io import StringIO
import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd

from core.data import load_cse2231_grade_data
from core.utils import create_grades_fig

dash.register_page(
    __name__,
    path='/cse2231',
    name="CSE2231",
    title="The Education Dashboard: CSE 2231"
)


@callback(
    Output("cse2231-grade-overview", "figure"),
    Input("cse2231-grade-data", "data")
)
def render_grade_overview_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_grades_fig(df)

layout = html.Div([
    html.H1('CSE 2231: Software 2'),
    dcc.Graph(id="cse2231-grade-overview"),
    load_cse2231_grade_data()
])
