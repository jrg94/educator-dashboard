import dash
import dash_bootstrap_components as dbc
from dash import html

TRC_LOGO = "https://avatars.githubusercontent.com/u/42280715"


app = dash.Dash(
    __name__,
    external_scripts=[
        {
            "src": "https://plausible.io/js/plausible.js",
            "data-domain": "educator.jeremygrifski.com"
        }
    ],
    external_stylesheets=[
        dbc.themes.BOOTSTRAP
    ],
    title="The Educator Dashboard",
    use_pages=True,
    suppress_callback_exceptions=True
)
server = app.server


logo = html.A(
    dbc.Row(
        [
            dbc.Col(html.Img(src=TRC_LOGO, height="30px")),
            dbc.Col(
                dbc.NavbarBrand("Grifski Educator Dashboard", className="ms-2")
            ),
        ],
        align="center",
        className="g-0",
    ),
    href="https://jeremygrifski.com",
    style={"textDecoration": "none"},
)


navlinks = dbc.Nav(
    [
        dbc.NavLink(
            html.Div(page["name"]),
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    pills=True,
)


app.layout = dbc.Container([
    dbc.Navbar(
        dbc.Container(
            [
                logo,
                navlinks
            ]
        ),
        color="dark",
        dark="True"
    ),
    dash.page_container
])


if __name__ == '__main__':
    app.run_server(debug=True)
