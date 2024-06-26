from io import StringIO
from operator import itemgetter
import re

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

from core.constants import *
from core.data import *

dash.register_page(
    __name__,
    path=ASSESSMENT_PAGE_PATH,
    name=ASSESSMENT_PAGE_NAME,
    title=ASSESSMENT_PAGE_TITLE
)

# Helper functions

def blank_plot() -> go.Figure:
    """
    A helpful function for getting an empty plot when no data is available.
    
    :return: a plotly figure with default features
    """
    return go.Figure(
        layout={
            "xaxis": {
                "visible": False
            },
            "yaxis": {
                "visible": False
            },
            "annotations": [
                {
                    "text": "No matching data found",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                            "size": 28
                    }
                }
            ]

        }
    )

# Graph Callbacks

@callback(
    Output(ID_GRADE_OVERVIEW_FIG, "figure"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_COURSE_FILTER, "value")
)
def render_grade_overview_figure(
    education_data: str, 
    course_filter: int
) -> go.Figure:
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
    education_df = education_df[education_df[COLUMN_GRADE] != "EX"]
    education_df = education_df[education_df[COLUMN_TOTAL] != 0]
    
    # Type cast
    education_df[COLUMN_GRADE] = pd.to_numeric(education_df[COLUMN_GRADE])
    education_df[COLUMN_TOTAL] = pd.to_numeric(education_df[COLUMN_TOTAL])
    
    # Precompute columns 
    education_df[COLUMN_PERCENTAGE] = education_df[COLUMN_GRADE] / education_df[COLUMN_TOTAL]
        
    # Perform analysis
    to_plot: pd.DataFrame = education_df.groupby(COLUMN_ASSESSMENT_GROUP_NAME)[COLUMN_PERCENTAGE].aggregate({
        "mean", 
        "median", 
        "count"
    })
    to_plot = to_plot.rename(
        columns={
            "mean": COLUMN_AVERAGE, 
            "median": COLUMN_MEDIAN,
            "count": COLUMN_COUNT
        }
    )
    
    # Helpful values
    course_code = f'{education_df.iloc[0][COLUMN_COURSE_DEPARTMENT]} {str(education_df.iloc[0][COLUMN_COURSE_NUMBER])}'
    
    # Plot figure
    grade_fig = go.Figure(layout=dict(template='plotly'))
    grade_fig = px.bar(
        to_plot,
        labels={
            "value": COLUMN_PERCENTAGE,
            "variable": "Metric",
        },
        barmode="group",
        text_auto=".0%",
        title=f"Overview of Course Grades by Type for {course_code}",
        hover_data=[COLUMN_COUNT],
        category_orders={
            "variable": METRIC_ORDER
        }
    )
    grade_fig.update_layout(
        yaxis_range=[0, 1.05],
        yaxis_tickformat=".0%"
    )
    
    return grade_fig


@callback(
    Output(ID_DETAILED_ASSESSMENT_GRADES_FIG, "figure"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_ASSESSMENT_GROUP_FILTER, "value"),
    Input(ID_COURSE_FILTER, "value")
)
def render_assessment_calculations_figure(
    education_data: str, 
    assessment_group_filter: int, 
    course_filter: int
) -> go.Figure:
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
    education_df = education_df[education_df[COLUMN_GRADE] != "EX"]
    education_df = education_df[education_df[COLUMN_TOTAL] != 0]
    
    # Type cast
    education_df[COLUMN_GRADE] = pd.to_numeric(education_df[COLUMN_GRADE])
    education_df[COLUMN_TOTAL] = pd.to_numeric(education_df[COLUMN_TOTAL])
    
    # Precompute columns 
    education_df[COLUMN_PERCENTAGE] = education_df[COLUMN_GRADE] / education_df[COLUMN_TOTAL]
    
    # Perform analysis
    to_plot = education_df.groupby(COLUMN_ASSESSMENT_NAME)[COLUMN_PERCENTAGE].aggregate({"mean", "median", "count"})
    
    # Helpful variables
    course_code = f'{education_df.iloc[0][COLUMN_COURSE_DEPARTMENT]} {str(education_df.iloc[0][COLUMN_COURSE_NUMBER])}'
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
        text_auto=".0%",
        title=f"Average and Median Grades for {assessment_group_name} in {course_code}",
        category_orders={
            COLUMN_ASSESSMENT_NAME: assignment_types
        },
        hover_data=["count"]
    )
    assignment_calculations_fig.update_layout(
        yaxis_range=[0, 1.05],
        yaxis_tickformat=".0%"
    )
    
    return assignment_calculations_fig


@callback(
    Output(ID_MISSING_ASSESSMENT_FIG, "figure"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_ASSESSMENT_GROUP_FILTER, "value"),
    Input(ID_COURSE_FILTER, "value")
)
def render_missing_assessments_figure(
    education_data: str, 
    assessment_group_filter: int, 
    course_filter: int
) -> go.Figure:
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
    education_df = education_df[education_df[COLUMN_GRADE] != "EX"]
    education_df = education_df[education_df[COLUMN_TOTAL] != 0]
    
    # Type cast
    education_df[COLUMN_GRADE] = pd.to_numeric(education_df[COLUMN_GRADE])
    
    # Helpful values
    course_code = f'{education_df.iloc[0][COLUMN_COURSE_DEPARTMENT]} {str(education_df.iloc[0][COLUMN_COURSE_NUMBER])}'
    assignment_types = education_df.sort_values(COLUMN_ASSESSMENT_ID)[COLUMN_ASSESSMENT_NAME].unique()
    assessment_group_name = education_df.iloc[0][COLUMN_ASSESSMENT_GROUP_NAME]
    
    # Helper function
    def number_missing(series):
        return len(series[series == 0])
    
    # Perform analysis
    to_plot = education_df.groupby(COLUMN_ASSESSMENT_NAME)[COLUMN_GRADE].agg(["count", number_missing])
    to_plot[COLUMN_PERCENT_MISSING] = to_plot["number_missing"] / to_plot["count"]
    
    # Plot figure
    missing_assignment_fig = go.Figure(layout=dict(template='plotly'))    
    missing_assignment_fig = px.bar(
        to_plot, 
        y=COLUMN_PERCENT_MISSING, 
        text_auto=".2%", 
        title=f"Percent of Missing {assessment_group_name} in {course_code}",
        category_orders={
            COLUMN_ASSESSMENT_NAME: assignment_types
        },
        hover_data=["count"]
    )
    missing_assignment_fig.update_layout(
        yaxis_range=[0, 1.05],
        yaxis_tickformat=".0%"
    )    
    
    return missing_assignment_fig

@callback(
    Output(ID_ASSESSMENT_TRENDS_FIG, "figure"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_ASSESSMENT_GROUP_FILTER, "value"),
    Input(ID_COURSE_FILTER, "value")
) 
def render_assessment_trends_figure(
    education_data: str, 
    assessment_group_filter: int, 
    course_filter: int
) -> go.Figure:
    """
    Plots the average grade for all assessments in an assessment group over time.
    
    :param education_data: the jsonified education dataframe
    :param course_filter: the course ID
    :param assessment_group_filter: the assessment group ID
    :return: the grade overview figure object
    """
    # Convert the data back into a dataframe
    education_df = pd.read_json(StringIO(education_data))
        
    # Filter
    education_df = education_df[education_df[COLUMN_COURSE_ID] == course_filter]
    education_df = education_df[education_df[COLUMN_ASSESSMENT_GROUP_ID] == assessment_group_filter]
    education_df = education_df[education_df[COLUMN_GRADE] != "EX"]
    education_df = education_df[education_df[COLUMN_TOTAL] != 0]
    
    # Type cast
    education_df[COLUMN_GRADE] = pd.to_numeric(education_df[COLUMN_GRADE])
    education_df[COLUMN_TOTAL] = pd.to_numeric(education_df[COLUMN_TOTAL])
    
    # Precompute some columns
    education_df[COLUMN_SEMESTER] = education_df[COLUMN_SEMESTER_SEASON] + " " + education_df[COLUMN_SEMESTER_YEAR].astype(str)
    education_df[COLUMN_PERCENTAGE] = education_df[COLUMN_GRADE] / education_df[COLUMN_TOTAL]
    
    # Helpful values
    course_code = f'{education_df.iloc[0][COLUMN_COURSE_DEPARTMENT]} {str(education_df.iloc[0][COLUMN_COURSE_NUMBER])}'
    assessment_group_name = education_df.iloc[0][COLUMN_ASSESSMENT_GROUP_NAME]

    # Perform analysis
    to_plot = education_df.groupby([
        COLUMN_SEMESTER_ID, 
        COLUMN_SEMESTER, 
        COLUMN_ASSESSMENT_NAME
    ]).agg({
        COLUMN_PERCENTAGE: "mean"
    }).reset_index()
    to_plot = to_plot.sort_values(by=COLUMN_SEMESTER_ID)
    
    # Plot figure
    trend_fig = go.Figure(layout=dict(template='plotly'))    
    trend_fig = px.line(
        to_plot,
        x=COLUMN_SEMESTER,
        y=COLUMN_PERCENTAGE,
        color=COLUMN_ASSESSMENT_NAME,
        markers=True,
        title=f"Average Grades for {assessment_group_name} in {course_code} by Semester",
        category_orders={
            COLUMN_SEMESTER: SEMESTER_ORDER,
            COLUMN_ASSESSMENT_NAME: ASSESSMENT_ORDER
        },
    ) 
    trend_fig.update_layout(
        yaxis_range=[0, 1.05],
        yaxis_tickformat=".0%"
    )
    
    return trend_fig


@callback(
    Output(ID_ASSESSMENT_GROUP_TIME_FIG, "figure"),
    Input(ID_ASSIGNMENT_SURVEY_DATA, "data"),
    Input(ID_ASSESSMENT_GROUP_FILTER, "value"),
    Input(ID_COURSE_FILTER, "value")
) 
def render_assessment_times_figure(
    assignment_survey_data: str, 
    assessment_group_filter: int, 
    course_filter: int
) -> go.Figure:
    """
    Creates a figure of the average and median time spent on each assignment.
    
    :param assignment_survey_data: the dataframe of all the data from the assignment survey
    :param assignment_group_filter: the assignment type (i.e., Homework or Project)
    :param course_filter: the course for which to create the time figure (e.g., CSE 2221: Software 1)
    """
    # Convert the data back into a dataframe
    assignment_survey_df = pd.read_json(StringIO(assignment_survey_data))
        
    # Filter
    assignment_survey_df = assignment_survey_df[assignment_survey_df[COLUMN_COURSE_ID] == course_filter]
    assignment_survey_df = assignment_survey_df[assignment_survey_df[COLUMN_ASSESSMENT_GROUP_ID] == assessment_group_filter]
    assignment_survey_df = assignment_survey_df[assignment_survey_df[COLUMN_TIME_TAKEN].notnull()]
    
    # Exit early
    if len(assignment_survey_df) == 0:
        return blank_plot()
    
    # Helpful variables
    assessment_group = assignment_survey_df[assignment_survey_df[COLUMN_ASSESSMENT_GROUP_ID] == assessment_group_filter].iloc[0][COLUMN_ASSESSMENT_GROUP_NAME]
    
    # Analysis
    to_plot = assignment_survey_df.groupby(COLUMN_ASSESSMENT_NAME).agg({COLUMN_TIME_TAKEN: ["mean", "median", "std", "count"], COLUMN_ASSESSMENT_ID: "first"})
    to_plot = to_plot.sort_values(by=(COLUMN_ASSESSMENT_ID, "first"))
    to_plot.columns = to_plot.columns.map(' '.join)
    to_plot = to_plot.reset_index()
    to_plot["Bar Labels"] = to_plot["Time Taken median"].apply(lambda x: f"{x:.01f} hrs")

    # Plot figure
    time_fig = go.Figure(layout=dict(template='plotly'))    
    time_fig = px.bar(
        to_plot,
        x=COLUMN_ASSESSMENT_NAME,
        y="Time Taken median",
        text="Bar Labels",
        title=f"Median Time to Complete {assessment_group}",
        labels={
            "Time Taken median": "Median Time Taken",
            "Time Taken count": "Number of Reviews"
        },
        hover_data=[
            "Time Taken count"
        ]
    )
    time_fig.update_layout(
        yaxis_ticksuffix="hrs"
    )

    return time_fig


@callback(
    Output(ID_VALUE_FIG, "figure"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_ASSIGNMENT_SURVEY_DATA, "data"),
    Input(ID_ASSESSMENT_GROUP_FILTER, "value"),
    Input(ID_COURSE_FILTER, "value")
) 
def render_value_figure(
    education_data: str, 
    assignment_survey_data: str, 
    assessment_group_filter: int, 
    course_filter: int
) -> go.Figure:
    """
    Creates a figure of expected amount of points a student could get for an
    hour of their time. 
    
    :param assignment_survey_data: the dataframe of all the data from the assignment survey
    :param assignment_group_filter: the assignment type (i.e., Homework or Project)
    :param course_filter: the course for which to create the time figure (e.g., CSE 2221: Software 1)
    """
    # Convert the data back into a dataframe
    assignment_survey_df = pd.read_json(StringIO(assignment_survey_data))
    education_df = pd.read_json(StringIO(education_data))
        
    # Filter
    assignment_survey_df = assignment_survey_df[assignment_survey_df[COLUMN_COURSE_ID] == course_filter]
    assignment_survey_df = assignment_survey_df[assignment_survey_df[COLUMN_ASSESSMENT_GROUP_ID] == assessment_group_filter]
    assignment_survey_df = assignment_survey_df[assignment_survey_df[COLUMN_TIME_TAKEN].notnull()]
    education_df = education_df[education_df[COLUMN_COURSE_ID] == course_filter]
    education_df = education_df[education_df[COLUMN_ASSESSMENT_GROUP_ID] == assessment_group_filter]
    education_df = education_df[education_df[COLUMN_GRADE] != "EX"]
    education_df = education_df[education_df[COLUMN_TOTAL] != 0]
    
    # Exit early
    if len(assignment_survey_df) == 0:
        return blank_plot()
    
    # Type cast
    education_df[COLUMN_GRADE] = pd.to_numeric(education_df[COLUMN_GRADE])
    education_df[COLUMN_TOTAL] = pd.to_numeric(education_df[COLUMN_TOTAL])
        
    # Precompute columns 
    education_df[COLUMN_PERCENTAGE] = education_df[COLUMN_GRADE] / education_df[COLUMN_TOTAL]
  
    # Helpful variables
    assessment_group = assignment_survey_df[assignment_survey_df[COLUMN_ASSESSMENT_GROUP_ID] == assessment_group_filter].iloc[0][COLUMN_ASSESSMENT_GROUP_NAME] 
    
    # Analysis
    to_plot_survey = assignment_survey_df.groupby([
        COLUMN_ASSESSMENT_NAME, 
        COLUMN_ASSESSMENT_ID
    ]).agg({
        COLUMN_TIME_TAKEN: ["mean", "median", "std", "count"]
    })
    to_plot_survey.columns = to_plot_survey.columns.map(' '.join)
    to_plot_survey = to_plot_survey.reset_index()
    to_plot_scores = education_df.groupby([
        COLUMN_ASSESSMENT_NAME, 
        COLUMN_ASSESSMENT_ID
    ]).agg({
        COLUMN_PERCENTAGE: ["mean", "median", "count"]
    })
    to_plot_scores.columns = to_plot_scores.columns.map(' '.join)
    to_plot_scores = to_plot_scores.reset_index()
    to_plot = pd.merge(to_plot_scores, to_plot_survey, on=[COLUMN_ASSESSMENT_ID, COLUMN_ASSESSMENT_NAME])
    to_plot["Median % Earned Per Hour of Work"] = to_plot["Percentage median"] / to_plot["Time Taken median"]
    to_plot = to_plot.sort_values(COLUMN_ASSESSMENT_ID)
    
    # Plot figure
    value_fig = go.Figure(layout=dict(template='plotly'))
    value_fig = px.bar(
        to_plot,
        x=COLUMN_ASSESSMENT_NAME,
        y="Median % Earned Per Hour of Work",
        title=f"Median Expected Value Of {assessment_group}",
        text_auto=".0%"
    )
    value_fig.update_layout(
        yaxis_tickformat=".0%",
    )
    value_fig.update_yaxes(
        autorangeoptions={
            "include": [0, 1]
        }
    )
    
    return value_fig


@callback(
    Output(ID_GRADE_DISTRIBUTION_FIG, "figure"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_ASSESSMENT_GROUP_FILTER, "value"),
    Input(ID_COURSE_FILTER, "value"),
    Input(ID_ASSESSMENT_FILTER, "value")
)
def render_grade_distribution_figure(
    education_data: str, 
    assessment_group_filter: int, 
    course_filter: int, 
    assessment_filter: int
) -> go.Figure:
    """
    Plots the average grade for all assessments in an assessment group over time.
    
    :param education_data: the jsonified education dataframe
    :param course_filter: the course ID
    :param assessment_group_filter: the assessment group ID
    :return: the grade overview figure object
    """
    # Convert the data back into a dataframe
    education_df = pd.read_json(StringIO(education_data))
        
    # Filter
    education_df = education_df[education_df[COLUMN_COURSE_ID] == course_filter]
    education_df = education_df[education_df[COLUMN_ASSESSMENT_GROUP_ID] == assessment_group_filter]
    education_df = education_df[education_df[COLUMN_ASSESSMENT_ID] == assessment_filter]
    education_df = education_df[education_df[COLUMN_GRADE] != "EX"]
    education_df = education_df[education_df[COLUMN_TOTAL] != 0]
    
    # Type cast
    education_df[COLUMN_GRADE] = pd.to_numeric(education_df[COLUMN_GRADE])
    education_df[COLUMN_TOTAL] = pd.to_numeric(education_df[COLUMN_TOTAL])
    
    # Precompute some columns
    education_df[COLUMN_PERCENTAGE] = education_df[COLUMN_GRADE] / education_df[COLUMN_TOTAL] * 100
    education_df[COLUMN_SEMESTER] = education_df[COLUMN_SEMESTER_SEASON] + " " + education_df[COLUMN_SEMESTER_YEAR].astype(str)
    
    # Helpful values
    course_code = f'{education_df.iloc[0][COLUMN_COURSE_DEPARTMENT]} {str(education_df.iloc[0][COLUMN_COURSE_NUMBER])}'
    semesters_in_order = [s for s in SEMESTER_ORDER if s in education_df[COLUMN_SEMESTER].unique()]
    assessment_name = education_df.iloc[0][COLUMN_ASSESSMENT_NAME]

    # Plot figure
    distribution_fig = go.Figure(layout=dict(template='plotly'))    
    distribution_fig = px.histogram(
        education_df,
        x=COLUMN_PERCENTAGE,
        color=COLUMN_SEMESTER,
        title=f"Grade Distribution for {assessment_name} in {course_code}",
        marginal="box",
        height=600,
        category_orders={
            COLUMN_SEMESTER: semesters_in_order
        }
    )
    distribution_fig.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("count", "Count")))
    distribution_fig.update_layout(
        yaxis_title_text = "Count"
    )
    
    return distribution_fig

# Dropdown callbacks

@callback(
    Output(ID_COURSE_FILTER, "options"),
    Output(ID_COURSE_FILTER, "value"),
    Input(ID_EDUCATION_DATA, "data")
)
def update_dropdown_course_filter(
    education_data: str
) -> tuple[list[dict], int]:
    """
    A callback for populating the course dropdown. 
    The labels in the dropdown are meant to be descriptive.
    The values are Course IDs, which can be used for filtering. 
    
    :param education_data: the education data
    :return: the options and start value for a dropdown
    """
    education_df = pd.read_json(StringIO(education_data))
    course_ids = education_df[COLUMN_COURSE_ID].unique()
    options = []
    for course_id in course_ids:
        course_data = education_df[education_df[COLUMN_COURSE_ID] == course_id].iloc[0]
        label = f"{course_data[COLUMN_COURSE_DEPARTMENT]} {course_data[COLUMN_COURSE_NUMBER]}: {course_data[COLUMN_COURSE_NAME]}"
        value = course_id
        options.append({"label": label, "value": value})
    options.sort(key=itemgetter("label"))
    return options, options[0]["value"]


@callback(
    Output(ID_ASSESSMENT_GROUP_FILTER, "options"),
    Output(ID_ASSESSMENT_GROUP_FILTER, "value"),
    Input(ID_EDUCATION_DATA, "data"),
    Input(ID_COURSE_FILTER, "value")
)
def update_dropdown_assessment_group_filter(
    education_data: str, 
    course_filter: int
) -> tuple[list[dict], int]:
    """
    A callback for populating the assessment group dropdown.
    The labels and values are the same. 
    
    :param education_data: the education data
    :param course_filter: the current course
    :return: the options and start value for a dropdown
    """
    education_df = pd.read_json(StringIO(education_data))
    education_df = education_df[education_df[COLUMN_COURSE_ID] == course_filter]
    assessment_group_ids = education_df[COLUMN_ASSESSMENT_GROUP_ID].unique()
    options = []
    for assessment_group_id in assessment_group_ids:
        assessment_group_data = education_df[education_df[COLUMN_ASSESSMENT_GROUP_ID] == assessment_group_id].iloc[0]
        label = f"{assessment_group_data[COLUMN_ASSESSMENT_GROUP_NAME]} ({assessment_group_data[COLUMN_ASSESSMENT_GROUP_WEIGHT]}% Weight)"
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
def update_dropdown_assessment_filter(
    education_data: str, 
    course_filter: int, 
    assessment_group_filter: int
) -> tuple[list[dict], int]:
    """
    A callback for populating the assessment group dropdown.
    The labels and values are the same. 
    
    :param: the education data
    :param course_filter: the current course
    :param assessment_group_filter: the current assessment group
    :return: the options and start value for a dropdown
    """
    education_df = pd.read_json(StringIO(education_data))
    education_df = education_df[education_df[COLUMN_COURSE_ID] == course_filter]
    education_df = education_df[education_df[COLUMN_ASSESSMENT_GROUP_ID] == assessment_group_filter]
    education_df = education_df[education_df[COLUMN_TOTAL] != 0]
    assessment_ids = education_df[COLUMN_ASSESSMENT_ID].unique()
    options = []
    for assessment_id in assessment_ids:
        totals = education_df[education_df[COLUMN_ASSESSMENT_ID] == assessment_id][COLUMN_TOTAL].unique()
        points = f"{totals[0]} Points" if len(totals) == 1 else "Varies"
        assessment_id_data = education_df[education_df[COLUMN_ASSESSMENT_ID] == assessment_id].iloc[0]
        assessment_name: str = assessment_id_data[COLUMN_ASSESSMENT_NAME]
        label = f"{assessment_name} ({points})"
        value = assessment_id
        options.append({"label": label, "value": value})
    options.sort(key=itemgetter("label"))
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
        used in my classes. Note: all of the assessments on this
        page are averaged to include the missing assignments as well as all
        submissions, which almost certainly lowers the overall averages.
        Likewise, some averages, such as exams, are actually inflated due to 
        grade replacement. Future work will be done to show this nuance in more 
        detail.
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
    dcc.Markdown(
        """
        The last few plots I'd like to sneak into this section actually 
        integrates student reviews of the assessments. To start, here's a plot
        of the time students claim they spend on each assessment. Depending on 
        which filters you use, **this plot may show up empty**. I only started 
        collecting time data for software 1 and 2. Future work will be done
        to include exam time, since I now track that as well. 
        """  
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_ASSESSMENT_GROUP_TIME_FIG)],
        type="graph"
    ),
    html.P(
        """
        Up next, I want to share a more interesting plot I've crafted
        that looks to combine the estimated time data with the median scores.
        I call it the value plot because it shows the amount of percentage 
        points a student can expect to get for an hour of their time. Again, 
        if there is no time related data, you will not see a plot.
        """  
    ),
     dcc.Loading(
        [dcc.Graph(id=ID_VALUE_FIG)],
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
    load_education_data(),
    load_assignment_survey_data()
])
