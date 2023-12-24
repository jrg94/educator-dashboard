import string
from collections import Counter

import nltk
import pandas as pd
import plotly
import plotly.express as px
from constants import (assignment_type, avg_time, during_emotions_column,
                       median_time, post_emotions_column, pre_emotions_column,
                       project_review_col, review_count, rubric_heading,
                       satisfaction_colors, satisfaction_mapping, std_time)
from nltk.corpus import stopwords


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
    try:
        nltk.data.find('tokenizers/punkt')
    except:
        nltk.download('punkt')
        
    try:
        nltk.data.find('stopwords')
    except:
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


def create_course_eval_fig(course_eval_data, question, axes_labels):
    colors = dict(zip(axes_labels, satisfaction_colors.values()))
    question_data = course_eval_data.melt(
        id_vars=[item for item in course_eval_data.columns if question not in item],
        var_name="Question",
        value_name="Response"
    )
    question_data = question_data[question_data["Response"].notna()]
    question_fig = px.histogram(
        question_data, 
        x="Response", 
        color="Response", 
        facet_col="Question", 
        facet_col_wrap=2, 
        category_orders=dict(Response=axes_labels),
        text_auto=True,
        title=f"{question} by Subquestion".title(),
        color_discrete_map=colors
    )
    question_fig.for_each_annotation(lambda a: a.update(text=a.text[a.text.find("[")+1:a.text.find("]")]))
    return question_fig


def create_value_fig(grade_data, assignment_survey_data, assignment, max_score):
    assignment_score_data = [name for name in grade_data.columns if assignment in name]
    assignment_calculations = grade_data[assignment_score_data].agg(["mean", "median"]).T
    assignment_time_data = assignment_survey_data[assignment_survey_data[assignment_type] == "Project"]
    assignment_time_data = assignment_time_data.drop_duplicates(subset=[project_review_col]).sort_values(by=project_review_col)
    assignment_time_data["Project #"] = "Project #" + assignment_time_data[project_review_col].astype(int).astype(str)
    assignment_time_data = assignment_time_data.set_index(f"{assignment} #")[median_time]
    assignment_aggregate_data = assignment_calculations.join(assignment_time_data)
    assignment_aggregate_data = assignment_aggregate_data.rename(columns={'mean': f'Average Score/{max_score}', 'median': f'Median Score/{max_score}'})
    assignment_aggregate_data["Points per Hour"] = assignment_aggregate_data[f"Median Score/{max_score}"] / assignment_aggregate_data["Median Time (hours)"]
    assignment_aggregate_data["Minutes per Point"] = assignment_aggregate_data["Median Time (hours)"] / assignment_aggregate_data[f"Median Score/{max_score}"] * 60
    assignment_aggregate_data = assignment_aggregate_data.reset_index()
    assignment_expected_time_fig = px.bar(
        assignment_aggregate_data,
        x="index",
        y="Points per Hour",
        labels={
            "index": "Project Name",
            "Points per Hour": "Median Points/Hour of Work",
        },
        text_auto=".2s",
        title="Expected Value Per Project"
    )
    assignment_expected_time_fig.update_layout(showlegend=False)
    assignment_expected_effort_fig = px.bar(
        assignment_aggregate_data,
        x="index",
        y="Minutes per Point",
        labels={
            "index": "Project Name",
            "Minutes per Point": "Median Minutes of Work/Point",
        },
        text_auto=".2s",
        title="Expected Effort Per Project"
    )
    assignment_expected_effort_fig.update_layout(showlegend=False)
    return assignment_expected_time_fig, assignment_expected_effort_fig


def create_correlation_fig(grade_data, correlating_factor, label):
    grade_overview = generate_grade_overview(grade_data)

    total_scores = grade_overview["Exams"] * .6 \
        + grade_overview["Homeworks"] * .06 \
        + grade_overview["Projects"] * .3 \
        + grade_overview["Participation"] * .04

    correlation = {
        "Grades": total_scores,
        label: grade_data[correlating_factor]
    }

    return px.scatter(
        pd.DataFrame(correlation),
        y="Grades",
        x=label,
        trendline="ols",
        title=f"Grades vs {label}"
    )


def generate_grade_overview(grade_data):
    grade_data = grade_data[grade_data["Date"] != "2020-05-07"]
    exam_columns = [name for name in grade_data.columns if "Exam" in name]
    homework_columns = [name for name in grade_data.columns if "Homework" in name]
    project_columns = [name for name in grade_data.columns if "Project" in name]
    participation_columns = [name for name in grade_data.columns if "Participation" in name]

    exam_grades = grade_data[exam_columns].sum(axis=1) / (100 * 3) * 100
    homework_grades = grade_data[homework_columns].sum(axis=1) / (2 * 22) * 100
    project_grades = grade_data[project_columns].sum(axis=1) / (10 * 11) * 100
    participation_grades = grade_data[participation_columns].sum(axis=1) / (4 * 1) * 100

    overview_dict = {
        "Exams": exam_grades,
        "Homeworks": homework_grades,
        "Projects": project_grades,
        "Participation": participation_grades
    }

    return pd.DataFrame(overview_dict)


def create_grades_fig(grade_data):
    assignment_calculations = generate_grade_overview(grade_data).agg(["mean", "median"]).T
    row_count = len(grade_data.index)
    assignment_calculations["count"] = {
        "Exams": row_count * 3,
        "Projects": row_count * 11,
        "Homeworks": row_count * 22,
        "Participation": row_count
    }
    grade_fig = px.bar(
        assignment_calculations,
        labels={
            "index": "Assignment Type",
            "value": "Grade/100%",
            "variable": "Metric",
            "mean": "Average",
            "median": "Median",
            "count": "Estimated Count"
        },
        barmode="group",
        title=f"Overview of Course Grades by Type",
        hover_data=["count"]
    )
    return grade_fig


def create_assignment_fig(grade_data, assignment, total):
    assignment_data = [name for name in grade_data.columns if assignment in name]
    assignment_calculations = grade_data[assignment_data].agg(["mean", "median"]).T
    assignment_calculations.rename(columns={'mean': 'Average', 'median': 'Median'}, inplace=True)
    assignment_calculations_fig = px.bar(
        assignment_calculations,
        labels={
            "index": "Project Name",
            "value": f"Grade/{total}",
            "variable": "Metric",
            "mean": "Average",
            "median": "Median"
        },
        barmode='group',
        text_auto=".2s",
        title=f"Average and Median {assignment} Grades".title()
    )
    return assignment_calculations_fig


def create_missing_assignment_fig(grade_data, assignment):
    missing_assignment_data = (grade_data == 0).sum() / len(grade_data) * 100
    missing_assignment_data = missing_assignment_data.reset_index()
    missing_assignment_data.rename(columns={'index': 'Assignment', 0: 'Percent Missing'}, inplace=True)
    missing_assignment_data = missing_assignment_data.loc[missing_assignment_data["Assignment"].str.contains(assignment)]
    missing_assignment_fig = px.bar(
        missing_assignment_data, 
        x="Assignment", 
        y="Percent Missing", 
        text_auto=".2s", 
        title=f"Percent of Missing {assignment}s"
    )
    return missing_assignment_fig


def create_project_trend_fig(grade_data: pd.DataFrame, assignment: str):
    """
    Creates a semesterly line graph for each assignment of a
    particular type (e.g., Exam, Project, Homework, etc.)
    """
    trend_data = grade_data.groupby("Date").mean(numeric_only=True)[[item for item in grade_data if assignment in item]]
    trend_data = trend_data.reset_index().melt(
        id_vars="Date",
        var_name="Assignment", 
        value_name="Average Score"
    ).dropna()
    
    trend_fig = px.line(
        trend_data,
        x="Date",
        y="Average Score",
        color="Assignment",
        markers=True,
        title=f"Average {assignment} Score by Date"
    )
    return trend_fig

