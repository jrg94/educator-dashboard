import callbacks
import dash
from core.layouts import tab_layout


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

app.layout = tab_layout

if __name__ == '__main__':
    app.run_server(debug=True)
