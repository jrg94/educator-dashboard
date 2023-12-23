from collections import Counter
import string
import pandas as pd
import plotly.express as px
import plotly
import nltk
from nltk.corpus import stopwords

from constants import std_time, review_count, avg_time, median_time, pre_emotions_column, during_emotions_column, post_emotions_column, project_review_col, rubric_heading, satisfaction_mapping, satisfaction_colors


def _semester_order(data: pd.DataFrame):
    """
    Returns a sorted list of semesters in the expected order 
    (e.g., [Autumn 2018, Spring 2019, Autumn 2019, Spring 2020, ...]).
    
    It works by parsing the semester string and calculating a
    sortable numeric value where the year is used unless
    the semester is in the autumn, in which case the year + .5
    is used. 

    :param data: the DataFrame provided by the user with an assumed Semester column
    :return: a list of sorted semesters
    """
    return sorted(
        data["Semester"].unique(), 
        key=lambda x: int(x.split()[1]) + (.5 if x.split()[0] == "Autumn" else 0)
    )


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

def create_sei_fig(sei_data: pd.DataFrame) -> plotly.graph_objs.Figure:
    """
    Creates an SEI data figure showing all of the SEI
    data results over "time", where time is a categorical
    semester string that is added to the SEI data. There
    are four lines in this plot to compare against my
    SEI data (i.e., the department, college, and university).
    
    :param sei_data: the raw SEI data as a dataframe
    :return: the resulting SEI figure
    """
    sei_data["Semester"] = sei_data["Season"] + " " + sei_data["Year"].astype(str)
    sei_fig = px.line(
        sei_data, 
        x="Semester", 
        y="Mean", 
        color="Group", 
        facet_col="Question", 
        facet_col_wrap=2, 
        markers=True, 
        title="Student Evaluation of Instruction Trends by Cohort",
        category_orders={
        "Semester": _semester_order(sei_data)
        },
        hover_data=["Course"]
    )
    sei_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return sei_fig

def create_sei_comment_fig(sei_comments: pd.DataFrame) -> plotly.graph_objs.Figure:
    # Installs needed corpus data
    nltk.download('punkt')
    nltk.download('stopwords')
    
    # Tokenizes the comments and computes their counts
    results = Counter()
    sei_comments["Comment"].str.lower().apply(nltk.word_tokenize).apply(results.update)
    word_counts = pd.DataFrame.from_dict(results, orient="index").reset_index()
    word_counts = word_counts.rename(columns={"index": "Word", 0:"Count"}) 
    
    # Removes stop words and punctuation from the totals
    stop = stopwords.words("english")
    word_counts = word_counts[~word_counts["Word"].isin(stop)]
    word_counts = word_counts[~word_counts["Word"].isin(list(string.punctuation))]
    word_counts = word_counts[~word_counts["Word"].str.contains("'")]
    
    # Sorts and pulls the top 25 words
    word_counts = word_counts.sort_values(by="Count", ascending=False)
    word_counts = word_counts.head(25)
    word_counts = word_counts.sort_values(by="Count")
    sei_comment_fig = px.bar(
        word_counts,
        x="Count",
        y="Word",
        height=1000,
        title="Top 25 Most Common Words in SEI Comments"
    )
    return sei_comment_fig
