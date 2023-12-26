import dash
from dash import html, dcc

dash.register_page(__name__, path='/patch-notes')


layout = html.Div(
    children=[
        dcc.Markdown(open("data/patch-notes.md", mode="r").read())
    ]
)
