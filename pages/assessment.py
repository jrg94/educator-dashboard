from io import StringIO

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html

from core.constants import *
from core.data import *
from core.utils import *
from core.utils import _semester_order

dash.register_page(
    __name__,
    path='/assessment',
    name="Assessment",
    title="The Educator Dashboard: Assessment"
)

# Graph Callbacks

@callback(
    Output(ID_GRADE_OVERVIEW_FIG, "figure"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_COURSE_FILTER, "value")
)
def render_grade_overview_figure(education_data: str, course_filter: int) -> go.Figure:
    """
    Plots an overview of the types of assessments that have been given in
    the current course. 
    
    :param education_data: the jsonified education dataframe
    :param course_filter: the course ID
    :return: the grade overview figure object
    """
    # Convert the data back into a dataframe
    education_df = pd.read_json(StringIO(education_data))
    
    # Filter
    education_df = education_df[education_df["Course ID"] == course_filter]
    education_df = education_df[education_df["Grade"] != "EX"]
    education_df = education_df[education_df["Total"] != 0]
    
    # Type cast
    education_df["Grade"] = pd.to_numeric(education_df["Grade"])
    education_df["Total"] = pd.to_numeric(education_df["Total"])
    
    # Precompute columns 
    education_df["Percentage"] = education_df["Grade"] / education_df["Total"] * 100
        
    # Perform analysis
    to_plot = education_df.groupby("Assignment Group Name")["Percentage"].aggregate({"mean", "median", "count"})
    
    # Helpful values
    course_code = f'{education_df.iloc[0]["Course Department"]} {str(education_df.iloc[0]["Course Number"])}'
    
    # Plot figure
    grade_fig = go.Figure(layout=dict(template='plotly'))
    grade_fig = px.bar(
        to_plot,
        labels={
            "index": "Assignment Type",
            "value": "Percentage",
            "variable": "Metric",
            "mean": "Average",
            "median": "Median",
            "count": "Count"
        },
        barmode="group",
        title=f"Overview of Course Grades by Type for {course_code}",
        hover_data=["count"]
    )
    
    return grade_fig


@callback(
    Output(ID_DETAILED_ASSESSMENT_GRADES_FIG, "figure"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_ASSESSMENT_GROUP_FILTER, "value"),
    Input(ID_COURSE_FILTER, "value")
)
def render_assessment_calculations_figure(education_data: str, assessment_group_filter: str, course_filter: int):
    """
    Plots a breakdown of the averages and medians per assessment for a specific
    course and assessment group. 
    
    :param education_data: the jsonified education dataframe
    :param course_filter: the course ID
    :param assessment_group_filter: the assessment group  # TODO: make this an ID for consistency
    :return: the assessment calculations figure object
    """
    # Convert the data back into a dataframe
    education_df = pd.read_json(StringIO(education_data))
    
    # Filter
    education_df = education_df[education_df["Course ID"] == course_filter]
    education_df = education_df[education_df["Assignment Group Name"] == assessment_group_filter]
    education_df = education_df[education_df["Grade"] != "EX"]
    education_df = education_df[education_df["Total"] != 0]
    
    # Type cast
    education_df["Grade"] = pd.to_numeric(education_df["Grade"])
    education_df["Total"] = pd.to_numeric(education_df["Total"])
    
    # Precompute columns 
    education_df["Percentage"] = education_df["Grade"] / education_df["Total"] * 100
    
    # Perform analysis
    to_plot = education_df.groupby("Assignment Name")["Percentage"].aggregate({"mean", "median", "count"})
    
    # Helpful variables
    course_code = f'{education_df.iloc[0]["Course Department"]} {str(education_df.iloc[0]["Course Number"])}'
    assignment_types = education_df.sort_values("Assignment ID")["Assignment Name"].unique()
    
    # Plot figure
    assignment_calculations_fig = go.Figure(layout=dict(template='plotly'))    
    assignment_calculations_fig = px.bar(
        to_plot,
        labels={
            "index": "Project Name",
            "value": "Percentage",
            "variable": "Metric",
            "mean": "Average",
            "median": "Median",
            "count": "Count"
        },
        barmode='group',
        text_auto=".2s",
        title=f"Average and Median Grades for {assessment_group_filter} in {course_code}",
        category_orders={
            "Assignment Name": assignment_types
        },
        hover_data=["count"]
    )
    assignment_calculations_fig.update_yaxes(range=[0, 100])
    
    return assignment_calculations_fig


@callback(
    Output(ID_CSE_2221_MISSING_HOMEWORKS_FIG, "figure"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_ASSESSMENT_GROUP_FILTER, "value"),
    Input(ID_COURSE_FILTER, "value")
)
def render_missing_assessments_figure(education_data: str, assessment_group_filter: str, course_filter: int):
    """
    Plots a breakdown of the averages and medians per assessment for a specific
    course and assessment group. 
    
    :param education_data: the jsonified education dataframe
    :param course_filter: the course ID
    :param assessment_group_filter: the assessment group  # TODO: make this an ID for consistency
    :return: the missing assessments figure object
    """
    # Convert the data back into a dataframe
    education_df = pd.read_json(StringIO(education_data))
    
    # Filter
    education_df = education_df[education_df["Course ID"] == course_filter]
    education_df = education_df[education_df["Assignment Group Name"] == assessment_group_filter]
    education_df = education_df[education_df["Grade"] != "EX"]
    education_df = education_df[education_df["Total"] != 0]
    
    # Type cast
    education_df["Grade"] = pd.to_numeric(education_df["Grade"])
    
    # Helpful values
    course_code = f'{education_df.iloc[0]["Course Department"]} {str(education_df.iloc[0]["Course Number"])}'
    assignment_types = education_df.sort_values("Assignment ID")["Assignment Name"].unique()
    
    # Helper function
    def number_missing(series):
        return len(series[series == 0])
    
    # Perform analysis
    to_plot = education_df.groupby("Assignment Name")["Grade"].agg(["count", number_missing])
    to_plot["Percent Missing"] = to_plot["number_missing"] / to_plot["count"] * 100
    
    # Plot figure
    missing_assignment_fig = go.Figure(layout=dict(template='plotly'))    
    missing_assignment_fig = px.bar(
        to_plot, 
        y="Percent Missing", 
        text_auto=".2s", 
        title=f"Percent of Missing {assessment_group_filter} in {course_code}",
        category_orders={
            "Assignment Name": assignment_types
        },
        hover_data=["count"]
    )
    missing_assignment_fig.update_yaxes(range=[0, 100])
    
    return missing_assignment_fig

@callback(
    Output(ID_ASSESSMENT_TRENDS_FIG, "figure"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_ASSESSMENT_GROUP_FILTER, "value"),
    Input(ID_COURSE_FILTER, "value")
)
def render_assessment_trends_figure(education_data: str, assessment_group_filter: str, course_filter: int):
    """
    Plots the average grade for all assignments in an assignment group over time.
    
    :param education_data: the jsonified education dataframe
    :param course_filter: the course ID
    :param assessment_group_filter: the assessment group  # TODO: make this an ID for consistency
    :return: the grade overview figure object
    """
    
    # Convert the data back into a dataframe
    education_df = pd.read_json(StringIO(education_data))
        
    # Filter
    education_df = education_df[education_df["Course ID"] == course_filter]
    education_df = education_df[education_df["Assignment Group Name"] == assessment_group_filter]
    education_df = education_df[education_df["Grade"] != "EX"]
    education_df = education_df[education_df["Total"] != 0]
    
    # Type cast
    education_df["Grade"] = pd.to_numeric(education_df["Grade"])
    education_df["Total"] = pd.to_numeric(education_df["Total"])
    
    # Precompute some columns
    education_df["Semester"] = education_df["Season"] + " " + education_df["Year"].astype(str)
    education_df["Percentage"] = education_df["Grade"] / education_df["Total"] * 100

    # Perform analysis
    to_plot = education_df.groupby(["Semester", "Assignment Name"]).agg({
        "Percentage": "mean",
        "Season": "first",
        "Year": "first"
    }).reset_index()
    to_plot = to_plot.sort_values(by="Season", ascending=False).sort_values(by="Year", kind="stable")
    print(to_plot)
    
    trend_fig = go.Figure(layout=dict(template='plotly'))    
    trend_fig = px.line(
        to_plot,
        x="Semester",
        y="Percentage",
        color="Assignment Name",
        markers=True,
        title=f"Average {assessment_group_filter} Score by Semester",
        category_orders={
            "Semester": _semester_order(education_df)
        },
    )
    return trend_fig

# Dropdown callbacks

@callback(
    Output(ID_ASSESSMENT_GROUP_FILTER, "options"),
    Output(ID_ASSESSMENT_GROUP_FILTER, "value"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_COURSE_FILTER, "value")
)
def update_dropdown_assessment_filter(education_data, course_filter):
    """
    A callback for populating the assessment group dropdown.
    The labels and values are the same. 
    """
    education_df = pd.read_json(StringIO(education_data))
    education_df = education_df[education_df["Course ID"] == course_filter]
    assignment_groups = sorted(education_df["Assignment Group Name"].unique())
    return assignment_groups, assignment_groups[0]


@callback(
    Output(ID_COURSE_FILTER, "options"),
    Output(ID_COURSE_FILTER, "value"),
    Input(ID_EDUCATION_DATA, "data")
)
def update_dropdown_course_filter(education_data):
    """
    A callback for populating the course dropdown. 
    The labels in the dropdown are meant to be descriptive.
    The values are Course IDs, which can be used for filtering. 
    """
    education_df = pd.read_json(StringIO(education_data))
    course_ids = sorted(education_df["Course ID"].unique())
    options = []
    for course_id in course_ids:
        course_data = education_df[education_df["Course ID"] == course_id].iloc[0]
        label = f"{course_data['Course Department']} {course_data['Course Number']}: {course_data['Course Name']}"
        value = course_id
        options.append({"label": label, "value": value})
    return options, course_ids[0]


layout = html.Div([
    dbc.Navbar(
        dbc.Container(
            [
                dcc.Dropdown(id=ID_COURSE_FILTER),
                dcc.Dropdown(id=ID_ASSESSMENT_GROUP_FILTER)
            ]
        ),
        color="dark",
        dark=True,
        sticky="top"
    ),
    html.H1("Assessment"),
    html.P(
        """
        Since I began teaching in 2018, I've kept a lot of data about the
        assessment of students. The goal of this page is to give you an overview 
        of the way I've assessed students over the years. To browse a course, 
        use the first dropdown at the top of the screen. All of the following 
        plots will regenerate for you. 
        """
    ),
    html.H2("Course Overview"),
    html.P(
        """
        To kick things off, here's a plot of the average and median grades
        grouped by assessment type (e.g., projects, homework, labs, etc.).
        This should give you an overview of the types of assessments I've
        used in my classes. 
        """  
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_GRADE_OVERVIEW_FIG)],
        type="graph"
    ),
    html.H2("Assessment Group Breakdown"),
    dcc.Markdown(
        """
        Each assessment group can be broken down into its individual
        assessments over the course of the semester. Feel free to use the 
        second dropdown to explore each assessment group in depth. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_DETAILED_ASSESSMENT_GRADES_FIG)],
        type="graph"
    ),
    dcc.Markdown(
        """
        As promised, here's a look at the trend of homework completion. As with 
        projects, students tend to submit fewer assignments as the semester 
        progresses. Though, I find it interesting that there are spikes in 
        missing assignments at various points throughout the semester. I suspect 
        that the assignments that students submit least often are tied to larger 
        review assignments before exams.
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_CSE_2221_MISSING_HOMEWORKS_FIG)],
        type="graph"
    ),
    dcc.Markdown(
        """
        Finally, I find it helpful to look at average and median grades over
        time. So, here's what that looks from semester to semester. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_ASSESSMENT_TRENDS_FIG)],
        type="graph"
    ),
    html.H2("Assessment Breakdown"),
    html.P(
        """
        Naturally, each assessment can be broken down into its individual 
        submissions. At this level, we can take a look at assessment
        distributions, which provide more context to the averages and medians.
        """
    ),
    html.P(
        """
        If you liked these plots, I'd encourage you to browse the triangulation
        tab, which combines the grade data with some of the feedback I've gotten
        over the years. 
        """
    ),
    load_cse2221_grade_data(),
    load_education_data()
])
