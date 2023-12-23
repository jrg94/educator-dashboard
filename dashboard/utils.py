import pandas as pd
import plotly.express as px

from constants import std_time, review_count, avg_time, median_time, pre_emotions_column, during_emotions_column, post_emotions_column, project_review_col, rubric_heading, satisfaction_mapping, satisfaction_colors


def create_time_fig(assignment_survey_data: pd.DataFrame, col: str):
    """
    Creates a figure of the average and median time spent
    on each assignment.
    
    :param assignment_survey_data: the dataframe of all the data from the assignment survey
    :param col: the column from which to render the time figure (e.g., project or homework)
    """
    to_plot = assignment_survey_data \
        .drop_duplicates(subset=[col]) \
        .dropna(subset=[col]) \
        .sort_values(by=col)
    to_plot = to_plot.melt(
        id_vars=[item for item in to_plot.columns if item not in [avg_time, median_time]],
        var_name="Metric",
        value_name="Time (hours)"
    )
    time_fig = px.bar(
        to_plot,
        x=col,
        y="Time (hours)",
        color="Metric",
        text_auto=".2s",
        barmode='group',
        title="Average and Median Assignment Time",
        error_y=std_time,
        hover_data=[review_count]
    )
    time_fig.update_traces(
        textfont_size=12, 
        textangle=0,
        textposition="inside", 
        insidetextanchor="start", 
        cliponaxis=False
    )
    return time_fig

def create_emotions_fig(assignment_survey_data: pd.DataFrame, col: str):
    """
    Creates a plot of the emotions data for the different kinds of assignments.
    
    :param assignment_survey_data: the dataframe of all the data from the assignment survey
    :param col: the column from which to render the emotions figure (e.g., project or homework)
    """
    emotions_data = assignment_survey_data.explode(pre_emotions_column)
    emotions_data = emotions_data.explode(during_emotions_column)
    emotions_data = emotions_data.explode(post_emotions_column)
    emotions_data = emotions_data[emotions_data[pre_emotions_column].isin(["Joy", "Hope", "Hopelessness", "Relief", "Anxiety"])]
    emotions_data = emotions_data[emotions_data[during_emotions_column].isin(["Enjoyment", "Anger", "Frustration", "Boredom"])]
    emotions_data = emotions_data[emotions_data[post_emotions_column].isin(["Joy", "Pride", "Gratitude", "Sadness", "Shame", "Anger"])]
    emotions_data = emotions_data.groupby(col)[[pre_emotions_column, during_emotions_column, post_emotions_column]].value_counts() 
    emotions_data = emotions_data.reset_index().melt(id_vars=col, value_vars=[pre_emotions_column, during_emotions_column, post_emotions_column])
    emotions_data = emotions_data.replace({
        pre_emotions_column: "Pre-Assignment",
        during_emotions_column: "During Assignment",
        post_emotions_column: "Post-Assignment"
    })
    emotions_figure = px.histogram(
        emotions_data,
        x="value",
        color="variable",
        facet_col=col,
        facet_col_wrap=2,
        labels={
        "value": 'Emotion'    
        }
    )
    emotions_figure.for_each_annotation(lambda a: a.update(text=f'Homework {a.text.split("=")[-1].split(".")[0]}'))
    return emotions_figure


def create_rubric_overview_fig(assignment_survey_data: pd.DataFrame):
    assignment_survey_data[rubric_heading] = assignment_survey_data[rubric_heading].map(satisfaction_mapping)
    data = assignment_survey_data[rubric_heading].value_counts().rename_axis("Response").reset_index(name="Number of Reviews")
    rubric_fig = px.bar(
        data, 
        x="Response",
        y="Number of Reviews",
        color="Response",
        category_orders={"Response": list(satisfaction_mapping.values())},
        text_auto=True,
        title="Project Rubric Satisfaction Overview",
        color_discrete_map=satisfaction_colors
    )
    return rubric_fig


def create_rubric_breakdown_fig(assignment_survey_data: pd.DataFrame):
    assignment_survey_data[rubric_heading] = assignment_survey_data[rubric_heading].map(satisfaction_mapping)
    data = assignment_survey_data.groupby(project_review_col)[rubric_heading] \
        .value_counts() \
        .unstack() \
        .reset_index() \
        .melt(id_vars=[project_review_col], var_name="Response", value_name="Number of Reviews") \
        .dropna() 
    rubric_breakdown_fig = px.bar(
        data, 
        x="Response",
        y="Number of Reviews",
        color="Response",
        facet_col=project_review_col, 
        facet_col_wrap=2,
        text_auto=True,
        category_orders={
            "Response": list(satisfaction_mapping.values()),
            project_review_col: list(range(1, 12))
        },
        labels={
            rubric_heading: 'Response',
        },
        title="Rubric Satisfaction By Project",
        color_discrete_map=satisfaction_colors
    )
    rubric_breakdown_fig.for_each_annotation(lambda a: a.update(text=f'Project {a.text.split("=")[-1]}'))
    return rubric_breakdown_fig


def create_rubric_scores_fig(assignment_survey_data: pd.DataFrame):
    rubric_scores = assignment_survey_data.groupby(project_review_col)[rubric_heading].agg(["mean", "count"])
    rubric_scores_fig = px.bar(
        rubric_scores, 
        y="mean", 
        color="count",
        labels={
        "mean": "Average Score (out of 5)",
        "count": "Number of Reviews"
        },
        text_auto=".3s",
        title="Project Rubric Satisfaction Scores",
        color_continuous_scale=px.colors.sequential.Viridis
    )
    return rubric_scores_fig
