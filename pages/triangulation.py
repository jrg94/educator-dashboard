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

# TODO: this page will be where all the most interesting analyses happen

layout = html.Div([
    html.H1("Triangulation"),
    html.P(
        """
        TBD
        """
    )
])
