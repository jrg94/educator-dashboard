from io import StringIO

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html

from core.constants import *
from core.data import *
from core.utils import *

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
    education_df = education_df[education_df[COLUMN_COURSE_ID] == course_filter]
    education_df = education_df[education_df["Grade"] != "EX"]
    education_df = education_df[education_df["Total"] != 0]
    
    # Type cast
    education_df["Grade"] = pd.to_numeric(education_df["Grade"])
    education_df["Total"] = pd.to_numeric(education_df["Total"])
    
    # Precompute columns 
    education_df["Percentage"] = education_df["Grade"] / education_df["Total"] * 100
        
    # Perform analysis
    to_plot = education_df.groupby("Assessment Group Name")["Percentage"].aggregate({"mean", "median", "count"})
    
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
def render_assessment_calculations_figure(education_data: str, assessment_group_filter: int, course_filter: int):
    """
    Plots a breakdown of the averages and medians per assessment for a specific
    course and assessment group. 
    
    :param education_data: the jsonified education dataframe
    :param course_filter: the course ID
    :param assessment_group_filter: the assessment group ID
    :return: the assessment calculations figure object
    """
    # Convert the data back into a dataframe
    education_df = pd.read_json(StringIO(education_data))
    
    # Filter
    education_df = education_df[education_df[COLUMN_COURSE_ID] == course_filter]
    education_df = education_df[education_df[COLUMN_ASSESSMENT_GROUP_ID] == assessment_group_filter]
    education_df = education_df[education_df["Grade"] != "EX"]
    education_df = education_df[education_df["Total"] != 0]
    
    # Type cast
    education_df["Grade"] = pd.to_numeric(education_df["Grade"])
    education_df["Total"] = pd.to_numeric(education_df["Total"])
    
    # Precompute columns 
    education_df["Percentage"] = education_df["Grade"] / education_df["Total"] * 100
    
    # Perform analysis
    to_plot = education_df.groupby(COLUMN_ASSESSMENT_NAME)["Percentage"].aggregate({"mean", "median", "count"})
    
    # Helpful variables
    course_code = f'{education_df.iloc[0]["Course Department"]} {str(education_df.iloc[0]["Course Number"])}'
    assignment_types = education_df.sort_values(COLUMN_ASSESSMENT_ID)[COLUMN_ASSESSMENT_NAME].unique()
    assessment_group_name = education_df.iloc[0][COLUMN_ASSESSMENT_GROUP_NAME]
        
    # Plot figure
    assignment_calculations_fig = go.Figure(layout=dict(template='plotly'))    
    assignment_calculations_fig = px.bar(
        to_plot,
        labels={
            "value": "Percentage",
            "variable": "Metric",
            "count": "Count"
        },
        barmode='group',
        text_auto=".2s",
        title=f"Average and Median Grades for {assessment_group_name} in {course_code}",
        category_orders={
            "Assessment Name": assignment_types
        },
        hover_data=["count"]
    )
    assignment_calculations_fig.update_yaxes(range=[0, 100])
    
    return assignment_calculations_fig


@callback(
    Output(ID_MISSING_ASSESSMENT_FIG, "figure"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_ASSESSMENT_GROUP_FILTER, "value"),
    Input(ID_COURSE_FILTER, "value")
)
def render_missing_assessments_figure(education_data: str, assessment_group_filter: int, course_filter: int):
    """
    Plots a breakdown of the averages and medians per assessment for a specific
    course and assessment group. 
    
    :param education_data: the jsonified education dataframe
    :param course_filter: the course ID
    :param assessment_group_filter: the assessment group ID
    :return: the missing assessments figure object
    """
    # Convert the data back into a dataframe
    education_df = pd.read_json(StringIO(education_data))
    
    # Filter
    education_df = education_df[education_df[COLUMN_COURSE_ID] == course_filter]
    education_df = education_df[education_df[COLUMN_ASSESSMENT_GROUP_ID] == assessment_group_filter]
    education_df = education_df[education_df["Grade"] != "EX"]
    education_df = education_df[education_df["Total"] != 0]
    
    # Type cast
    education_df["Grade"] = pd.to_numeric(education_df["Grade"])
    
    # Helpful values
    course_code = f'{education_df.iloc[0]["Course Department"]} {str(education_df.iloc[0]["Course Number"])}'
    assignment_types = education_df.sort_values(COLUMN_ASSESSMENT_ID)[COLUMN_ASSESSMENT_NAME].unique()
    assessment_name = education_df.iloc[0][COLUMN_ASSESSMENT_NAME]
    
    # Helper function
    def number_missing(series):
        return len(series[series == 0])
    
    # Perform analysis
    to_plot = education_df.groupby(COLUMN_ASSESSMENT_NAME)["Grade"].agg(["count", number_missing])
    to_plot["Percent Missing"] = to_plot["number_missing"] / to_plot["count"] * 100
    
    # Plot figure
    missing_assignment_fig = go.Figure(layout=dict(template='plotly'))    
    missing_assignment_fig = px.bar(
        to_plot, 
        y="Percent Missing", 
        text_auto=".2s", 
        title=f"Percent of Missing {assessment_name} in {course_code}",
        category_orders={
            COLUMN_ASSESSMENT_NAME: assignment_types
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
    Plots the average grade for all assessments in an assessment group over time.
    
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
    
    # Helpful values
    semesters_in_order = semester_order(education_df)
    course_code = f'{education_df.iloc[0]["Course Department"]} {str(education_df.iloc[0]["Course Number"])}'

    # Perform analysis
    to_plot = education_df.groupby(["Semester", "Assignment Name"]).agg({
        "Percentage": "mean"
    }).reset_index()
    to_plot = to_plot.sort_values(by="Semester", key=lambda col: col.map(lambda x: semesters_in_order[x]))
    
    # Plot figure
    trend_fig = go.Figure(layout=dict(template='plotly'))    
    trend_fig = px.line(
        to_plot,
        x="Semester",
        y="Percentage",
        color="Assignment Name",
        markers=True,
        title=f"Average Grades for {assessment_group_filter} in {course_code} by Semester",
        category_orders={
            "Semester": list(semesters_in_order.keys())
        },
    )
    trend_fig.update_yaxes(range=[0, 100])
    
    return trend_fig


@callback(
    Output(ID_ASSESSMENT_GROUP_TIME_FIG, "figure"),
    Input(ID_ASSIGNMENT_SURVEY_DATA, "data"),
    Input(ID_ASSESSMENT_GROUP_FILTER, "value"),
    Input(ID_COURSE_FILTER, "value")
) 
def render_assessment_times_figure(assignment_survey_data: str, assessment_group_filter: str, course_filter: int):
    """
    Creates a figure of the average and median time spent on each assignment.
    
    :param assignment_survey_data: the dataframe of all the data from the assignment survey
    :param assignment_group_filter: the assignment type (i.e., Homework or Project)
    :param course_filter: the course for which to create the time figure (e.g., CSE 2221: Software 1)
    """
    
    # Convert the data back into a dataframe
    assignment_survey_df = pd.read_json(StringIO(assignment_survey_data))
    
    # Filter
    assignment_survey_df = assignment_survey_df[assignment_survey_df["Course ID"] == course_filter]
    assignment_survey_df = assignment_survey_df[assignment_survey_df["Assignment Group Name"] == assessment_group_filter]

    # TODO: very stuck with this one


@callback(
    Output(ID_GRADE_DISTRIBUTION_FIG, "figure"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_ASSESSMENT_GROUP_FILTER, "value"),
    Input(ID_COURSE_FILTER, "value"),
    Input(ID_ASSESSMENT_FILTER, "value")
)
def render_grade_distribution_figure(education_data: str, assessment_group_filter: str, course_filter: int, assessment_filter: str):
    """
    Plots the average grade for all assessments in an assessment group over time.
    
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
    education_df = education_df[education_df["Assignment Name"] == assessment_filter]
    education_df = education_df[education_df["Grade"] != "EX"]
    education_df = education_df[education_df["Total"] != 0]
    
    # Type cast
    education_df["Grade"] = pd.to_numeric(education_df["Grade"])
    education_df["Total"] = pd.to_numeric(education_df["Total"])
    
    # Precompute some columns
    education_df["Percentage"] = education_df["Grade"] / education_df["Total"] * 100
    education_df["Semester"] = education_df["Season"] + " " + education_df["Year"].astype(str)
    
    # Helpful values
    course_code = f'{education_df.iloc[0]["Course Department"]} {str(education_df.iloc[0]["Course Number"])}'
    semesters_in_order = [x for x in semester_order(education_df).keys() if x in education_df["Semester"].unique()]

    # Plot figure
    distribution_fig = go.Figure(layout=dict(template='plotly'))    
    distribution_fig = px.histogram(
        education_df,
        x="Percentage",
        color="Semester",
        title=f"Grade Distribution for {assessment_filter} in {course_code}",
        marginal="box",
        height=600,
        category_orders={
            "Semester": semesters_in_order
        }
    )
    
    return distribution_fig

# Dropdown callbacks

@callback(
    Output(ID_COURSE_FILTER, "options"),
    Output(ID_COURSE_FILTER, "value"),
    Input(ID_EDUCATION_DATA, "data")
)
def update_dropdown_course_filter(education_data: str):
    """
    A callback for populating the course dropdown. 
    The labels in the dropdown are meant to be descriptive.
    The values are Course IDs, which can be used for filtering. 
    """
    education_df = pd.read_json(StringIO(education_data))
    course_ids = education_df[COLUMN_COURSE_ID].unique()
    options = []
    for course_id in course_ids:
        course_data = education_df[education_df[COLUMN_COURSE_ID] == course_id].iloc[0]
        label = f"{course_data['Course Department']} {course_data['Course Number']}: {course_data['Course Name']}"
        value = course_id
        options.append({"label": label, "value": value})
    return options, options[0]["value"]


@callback(
    Output(ID_ASSESSMENT_GROUP_FILTER, "options"),
    Output(ID_ASSESSMENT_GROUP_FILTER, "value"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_COURSE_FILTER, "value")
)
def update_dropdown_assessment_group_filter(education_data: str, course_filter: int):
    """
    A callback for populating the assessment group dropdown.
    The labels and values are the same. 
    """
    education_df = pd.read_json(StringIO(education_data))
    education_df = education_df[education_df[COLUMN_COURSE_ID] == course_filter]
    assessment_group_ids = education_df[COLUMN_ASSESSMENT_GROUP_ID].unique()
    options = []
    for assessment_group_id in assessment_group_ids:
        assessment_group_data = education_df[education_df[COLUMN_ASSESSMENT_GROUP_ID] == assessment_group_id].iloc[0]
        label = f"{assessment_group_data['Assessment Group Name']}"
        value = assessment_group_id
        options.append({"label": label, "value": value})
    options.sort(key=lambda x: x["label"])
    return options, options[0]["value"]


@callback(
    Output(ID_ASSESSMENT_FILTER, "options"),
    Output(ID_ASSESSMENT_FILTER, "value"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_COURSE_FILTER, "value"),
    Input(ID_ASSESSMENT_GROUP_FILTER, "value")
)
def update_dropdown_assessment_filter(education_data: str, course_filter: int, assessment_group_filter: int):
    """
    A callback for populating the assessment group dropdown.
    The labels and values are the same. 
    """
    education_df = pd.read_json(StringIO(education_data))
    education_df = education_df[education_df[COLUMN_COURSE_ID] == course_filter]
    education_df = education_df[education_df[COLUMN_ASSESSMENT_GROUP_ID] == assessment_group_filter]
    education_df = education_df[education_df["Total"] != 0]
    assessment_ids = education_df[COLUMN_ASSESSMENT_ID].unique()
    options = []
    for assessment_id in assessment_ids:
        assessment_id_data = education_df[education_df[COLUMN_ASSESSMENT_ID] == assessment_id].iloc[0]
        label = assessment_id_data[COLUMN_ASSESSMENT_NAME]
        value = assessment_id
        options.append({"label": label, "value": value})
    options.sort(key=lambda x: x["value"])
    return options, options[0]["value"]


layout = html.Div([
    dbc.Navbar(
        dbc.Container(
            [
                dcc.Dropdown(id=ID_COURSE_FILTER),
                dcc.Dropdown(id=ID_ASSESSMENT_GROUP_FILTER),
                dcc.Dropdown(id=ID_ASSESSMENT_FILTER)
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
        [dcc.Graph(id=ID_MISSING_ASSESSMENT_FIG)],
        type="graph"
    ),
    dcc.Markdown(
        """
        In addition, I find it helpful to look at average and median grades over
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
    dcc.Loading(
        [dcc.Graph(id=ID_GRADE_DISTRIBUTION_FIG)],
        type="graph"
    ),
    html.P(
        """
        If you liked these plots, I'd encourage you to browse the triangulation
        tab, which combines the grade data with some of the feedback I've gotten
        over the years. 
        """
    ),
    load_education_data()
])
