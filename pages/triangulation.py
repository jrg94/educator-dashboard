import dash
from dash import html

from core.constants import *
from core.data import *
from core.utils import *

dash.register_page(
    __name__,
    path='/triangulation',
    name="Trianglulation",
    title="The Educator Dashboard: Triangulation"
)

layout = html.Div([
    html.H1("Triangulation"),
    html.P(
        """
        TBD
        """
    ),
    load_education_data(),
    load_assignment_survey_data()
])
