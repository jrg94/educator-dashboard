import dash
from dash import html

dash.register_page(
    __name__, 
    path='/',
    title="The Educator Dashboard"
)

layout = html.Div([
    html.H1('Home'),
    html.P(
        '''
        Welcome to my educator dashboard! The purpose of this site is to 
        provide some transparency to my students about my teaching history.
        It also exists to plot my trajectory as an educator by showing how
        my teaching has developed over time. To help you navigate, I've
        provided the following links with a short blurb describing their
        purpose.
        '''
    ),
    html.Ul(
        [
            html.Li(
                [
                    html.A("Assessment", href=dash.get_relative_path("/assessment")),
                    ": shares a variety of plots around student grades"
                ]
            ),
            html.Li(
                [
                    html.A("Feedback", href=dash.get_relative_path("/feedback")),
                    ": shares a variety of plots around student feedback"
                ]
            ),
            html.Li(
                [
                    html.A("History", href=dash.get_relative_path("/history")),
                    ": shares teaching developments over time"
                ]
            ),
        ]
    ),
    html.P(
        """
        Each semester I update this site with new data and even new plots, so
        check back regularly!
        """
    )
])
