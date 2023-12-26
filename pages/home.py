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
        Welcome to the new and improved educator dashboard! This website was previously a single
        page website with tabs. As it grew, it felt necessary to expand the website into
        logical pages. For instance, if you want to learn about how I have been evaluated as an
        instructor, check out my evaluations page using the "Evaluations" link in the navigation bar.
        Alternatively, if you're interested in any of the classes I teach, click their associated
        links instead. At this time, the homepage is a work-in-progress. Happy browsing!
        '''
    ),
])
