import dash
from dash import Input, Output, callback

import core.callbacks
from core.layouts import common_layout, tab_layout, patch_notes_layout

app = dash.Dash(
    __name__,
    external_scripts=[
        {
            "src": "https://plausible.io/js/plausible.js",
            "data-domain": "educator.jeremygrifski.com"
        }
    ],
    title="The Educator Dashboard"
)
server = app.server

app.layout = common_layout

@callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/":
        return tab_layout
    elif pathname == "/patch-notes":
        return patch_notes_layout
    else:
        return "404"

if __name__ == '__main__':
    app.run_server(debug=True)
