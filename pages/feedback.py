from io import StringIO

import dash
import pandas as pd
from dash import Input, Output, callback, dcc, html

from core.constants import *
from core.data import *
from core.utils import *

dash.register_page(
    __name__,
    path='/feedback',
    name="Feedback",
    title="The Educator Dashboard: Evaluation"
)


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
    sei_ratings_df["Semester"] = sei_ratings_df["Season"] + " " + sei_ratings_df["Year"].astype(str)
    
    # Helpful values
    semesters_in_order = semester_order(sei_ratings_df)
    
    # Prioritize maximum semesterly scores
    sei_ratings_df = sei_ratings_df.iloc[sei_ratings_df.groupby(["Semester", "Question ID", "Group"])["Mean"].agg(pd.Series.idxmax)]
    sei_ratings_df = sei_ratings_df.sort_values(by="Semester", key=lambda col: col.map(lambda x: semesters_in_order[x]))
        
    # Plot figure
    sei_fig = go.Figure(layout=dict(template='plotly'))    
    sei_fig = px.line(
        sei_ratings_df, 
        x="Semester", 
        y="Mean", 
        color="Group", 
        facet_col="Question", 
        facet_col_wrap=2, 
        markers=True, 
        title="Student Evaluation of Instruction Trends by Cohort",
        category_orders={
            "Semester": list(semesters_in_order.keys())
        },
        height=600
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
    
    # Sorts and pulls the top 25 words
    word_counts = word_counts.sort_values(by="Count", ascending=False)
    word_counts = word_counts.head(25)
    word_counts = word_counts.sort_values(by="Count")
    
    # Plot figure
    sei_comment_fig = go.Figure(layout=dict(template='plotly'))    
    sei_comment_fig = px.bar(
        word_counts,
        x="Count",
        y="Word",
        title="Top 25 Most Common Words in SEI Comments",
        height=600
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
    # TODO: I should add a plot showing the scores for all four questions with an additional
    # plot showing the trajectory of learning over the semester.
    dcc.Loading(
        [dcc.Graph(id=ID_EVAL_CONTRIBUTION_FIG)],
        type="graph"
    ),
    load_sei_data(),
    load_sei_comments_data(),
    load_course_eval_data()
])
