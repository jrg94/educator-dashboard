import dash
from dash import html, dcc

dash.register_page(
    __name__, 
    path='/patch-notes',
    name="Patch Notes",
    title="Grifski Educator Dashboard: Patch Notes"
)


layout = html.Div([
    dcc.Markdown(open("data/patch-notes.md", mode="r").read())
])
