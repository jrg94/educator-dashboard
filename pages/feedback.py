import string
from collections import Counter
from io import StringIO

import dash
import nltk
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html
from nltk.corpus import stopwords

from core.constants import *
from core.data import *
from core.utils import *

dash.register_page(
    __name__,
    path=FEEDBACK_PATH,
    name=FEEDBACK_NAME,
    title=FEEDBACK_TITLE
)

# Helper functions

def create_course_eval_fig(course_eval_data, question, axes_labels):
    """
    TODO: remove this at some point when we redo the site again
    """
    colors = dict(zip(axes_labels, COLORS_SATISFACTION.values()))
    question_data = course_eval_data.melt(
        id_vars=[item for item in course_eval_data.columns if question not in item],
        var_name="Question",
        value_name="Response"
    )
    question_data = question_data[question_data["Response"].notna()]
    question_fig = go.Figure(layout=dict(template='plotly'))
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

# Graph callbacks

@callback(
    Output(ID_SEI_RATINGS_FIG, "figure"),
    Input(ID_SEI_DATA, "data")
)
def render_sei_ratings_figure(sei_ratings_history: str):
    """
    Creates an SEI data figure showing all of the SEI data results over "time", 
    where time is a categorical semester string that is added to the SEI data. 
    There are four lines in this plot to compare against my SEI data (i.e., the 
    department, college, and university).
    
    :param sei_ratings_history: the raw SEI data as a dataframe
    :return: the resulting SEI figure
    """
    # Convert the data back into a dataframe
    sei_ratings_df = pd.read_json(StringIO(sei_ratings_history))
        
    # Precompute columns 
    sei_ratings_df["Semester"] = sei_ratings_df[COLUMN_SEMESTER_SEASON] + " " + sei_ratings_df[COLUMN_SEMESTER_YEAR].astype(str)
    
    # Helpful values
    semesters_in_order = semester_order(sei_ratings_df)
    
    # Prioritize maximum semesterly scores
    sei_ratings_df = sei_ratings_df.iloc[sei_ratings_df.groupby(["Semester", COLUMN_QUESTION_ID, COLUMN_COHORT])["Mean"].agg(pd.Series.idxmax)]
    sei_ratings_df = sei_ratings_df.sort_values(by="Semester", key=lambda col: col.map(lambda x: semesters_in_order[x]))
        
    # Plot figure
    sei_fig = go.Figure(layout=dict(template='plotly'))    
    sei_fig = px.line(
        sei_ratings_df, 
        x="Semester", 
        y="Mean", 
        color="Cohort", 
        facet_col="SEI Question", 
        facet_col_wrap=2, 
        markers=True, 
        title="Student Evaluation of Instruction Trends by Cohort",
        category_orders={
            "Semester": list(semesters_in_order.keys()),
            "Cohort": ["Instructor", "Department", "College", "University"]
        },
        height=800
    )
    sei_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    
    return sei_fig


@callback(
    Output(ID_SEI_COMMENTS_FIG, "figure"),
    Input(ID_SEI_COMMENTS_DATA, "data")
)
def render_sei_comments_figure(sei_comments_history: str):
    """
    Creates an SEI top words figure, which is generated from the comments
    data.
    
    :param sei_comments_history: the SEI comments data
    :return: the resulting SEI comments figure
    """
    # Convert the data back into a dataframe
    sei_comments_df = pd.read_json(StringIO(sei_comments_history))
    
    # Installs needed corpus data
    try:
        nltk.data.find('tokenizers/punkt')
    except:
        nltk.download('punkt')
        
    try:
        nltk.data.find('corpora/stopwords')
    except:
        nltk.download('stopwords')
    
    # Tokenizes the comments and computes their counts
    results = Counter()
    sei_comments_df["Comment"].str.lower().apply(nltk.word_tokenize).apply(results.update)
    word_counts = pd.DataFrame.from_dict(results, orient="index").reset_index()
    word_counts = word_counts.rename(columns={"index": "Word", 0:"Count"}) 
    
    # Removes stop words and punctuation from the totals
    stop = stopwords.words("english")
    word_counts = word_counts[~word_counts["Word"].isin(stop)]
    word_counts = word_counts[~word_counts["Word"].isin(list(string.punctuation))]
    word_counts = word_counts[~word_counts["Word"].str.contains("'")]
    
    # Sorts and pulls the top words
    top_count = 40
    word_counts = word_counts.sort_values(by="Count", ascending=False)
    word_counts = word_counts.head(top_count)
    word_counts = word_counts.sort_values(by="Count")
    
    # Plot figure
    sei_comment_fig = go.Figure(layout=dict(template='plotly'))    
    sei_comment_fig = px.bar(
        word_counts,
        x="Count",
        y="Word",
        title=f"Top {top_count} Most Common Words in SEI Comments",
        height=800
    )
    
    return sei_comment_fig


@callback(
    Output(ID_EVAL_COURSE_CONTENT_FIG, "figure"),
    Input(ID_COURSE_EVAL_DATA, "data")
)
def render_course_content_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_course_eval_fig(df, "Course content", SCALE_LIKERT)


@callback(
    Output(ID_EVAL_SKILL_FIG, "figure"),
    Input(ID_COURSE_EVAL_DATA, "data")
)
def render_skill_and_responsiveness_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_course_eval_fig(df, "Skill and responsiveness", SCALE_LIKERT)


@callback(
    Output(ID_EVAL_CONTRIBUTION_FIG, "figure"),
    Input(ID_COURSE_EVAL_DATA, "data")
)
def render_course_content_figure(jsonified_data):
    df = pd.read_json(StringIO(jsonified_data))
    return create_course_eval_fig(
        df,
        "Contribution to learning",
        SCALE_LIKERT_ALT
    )


layout = html.Div([
    html.H1("Feedback"),
    html.P(
        """
        As an educator, I spend a lot of time assessing my students. 
        Periodically, I give my students a chance to evaluate me. This page is 
        reserved for all of the data related to student evaluations of me.
        """
    ),
    html.H2("Student Evaluations of Instruction"),
    dcc.Markdown(
        """
        Each semester, the university asks students to fill out a survey about 
        the instruction for the course. These data are anonymized and provided 
        as averages for each question. Here is the breakdown of my scores 
        against the scores for various cohorts including my department, my 
        college, and my university.
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_SEI_RATINGS_FIG)],
        type="graph"
    ),
    html.P(
        """
        Also, as a qualitative researcher, I find the comments themselves to be 
        more meaningful. Therefore, here's a plot of the most frequent terms in 
        my SEI comments. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_SEI_COMMENTS_FIG)],
        type="graph"
    ),
    html.H2("Course Evaluation Survey Data"),
    dcc.Markdown(
        """
        At the end of each semester, I ask students to give me feedback on the 
        course. These data are collected through a Google Form. Questions are 
        broken down into different areas which include feedback on course 
        content, my skill and responsiveness, and the course's contribution to 
        learning.
        """
    ),
    html.H3('Course Content'),
    html.P(
        """
        One way the course was evaluated was by asking students to rate their 
        satisfaction with the course content. In short, there are four questions 
        that I ask that cover topics that range from learning objectives to
        organization. Generally, the students that choose to fill out the course 
        survey seem to be satisfied with the course content. For example, at 
        this time, there have been no "strongly disagree" responses. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_EVAL_COURSE_CONTENT_FIG)],
        type="graph"
    ),
    html.H3("Skill and Responsiveness of the Instructor"),
    html.P(
        """
        Another way the course was evaluated was by asking students to rate 
        their satisfaction with the instructor, me. This time around, I ask six 
        questions which range from satisfaction with time usage to satisfaction
        with grading. Again, students are generally happy with my instruction. 
        In fact, they're often more happy with my instruction than the course 
        content itself. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_EVAL_SKILL_FIG)],
        type="graph"
    ),
    html.H3("Contribution to Learning"),
    dcc.Markdown(
        """
        Yet another way the course was evaluated was by asking students how much 
        they felt the course contributed to their learning. In this section of 
        the survey, I ask students four questions that attempt to chart how much
        students felt they learned over the course of the semester. In general, 
        students believe they learned a great deal, with most students reporting 
        only a fair amount of knowledge coming into the course and a very good
        amount of knowledge at the end of the course. 
        """
    ),
    dcc.Loading(
        [dcc.Graph(id=ID_EVAL_CONTRIBUTION_FIG)],
        type="graph"
    ),
    load_sei_data(),
    load_sei_comments_data(),
    load_course_eval_data()
])
