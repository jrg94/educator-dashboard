import plotly.express as px

# Data URLS
URL_ASSIGNMENT_GROUP_LOOKUP = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/assignment-group-lookup.csv"
URL_ASSIGNMENT_LOOKUP = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/assignment-lookup.csv"
URL_ASSIGNMENT_SURVEY_HISTORY = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/assignment-survey-history.csv"
URL_COURSE_LOOKUP = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/course-lookup.csv"
URL_EVALUATION_SURVEY_HISTORY = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/evaluation-survey-history.csv"
URL_GRADING_HISTORY = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/grading-history.csv"
URL_SEI_COMMENTS_HISTORY = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/sei-comments-history.csv"
URL_SEI_QUESTIONS_LOOKUP = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/sei-questions-lookup.csv"
URL_SEI_RATINGS_HISTORY = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/sei-ratings-history.csv"
URL_TEACHING_HISTORY = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/teaching-history.csv"

# Column headings
COLUMN_RUBRIC = 'On a scale from 1 to 5, how satisfied are you with the rubric for this project?'
COLUMN_PROJECT_REVIEW = "Which project are you reviewing (enter a # between 1 and 11)?"
COLUMN_HOMEWORK_REVIEW = "Which homework assignment are you reviewing (enter a # between 1 and 37)?"
COLUMN_CLASS_REVIEW = "Which of the following classes is this assignment for?"
COLUMN_PRE_EMOTIONS = "Which of the following emotions did you experience **before** starting this project (select all that apply)?"
COLUMN_DURING_EMOTIONS = "Which of the following emotions did you experience while completing this project (select all that apply)?"
COLUMN_POST_EMOTIONS = "Which of the following emotions did you experience **after** completing this project (select all that apply)?"
COLUMN_TIME = "How much time did you spend on this assignment in hours?"
COLUMN_ASSIGNMENT_TYPE = "Are you reviewing a project or a homework assignment?"

# Added column headings
COLUMN_AVERAGE_TIME = "Average Time (hours)"
COLUMN_MEDIAN_TIME = "Median Time (hours)"
COLUMN_REVIEW_COUNT = "Number of Reviews"
COLUMN_STANDARD_DEVIATION = "Standard Deviation (hours)"

# Assignment survey filter values
FILTER_SOFTWARE_1 = "CSE 2221: Software 1"
FILTER_SOFTWARE_2 = "CSE 2231: Software 2"

# Data IDs
ID_ASSIGNMENT_SURVEY_DATA = "assignment-survey-data"
ID_SEI_DATA = "sei-data"
ID_SEI_COMMENTS_DATA = "sei-comments-data"
ID_COURSE_EVAL_DATA = "course-eval-data"
ID_CSE_2221_GRADE_DATA = "cse2221-grade-data"
ID_CSE_2231_GRADE_DATA = "cse2231-grade-data"
ID_EDUCATION_DATA = "history"

# Assessment figure IDs
ID_ASSESSMENT_GROUP_TIME_FIG = "assessment-group-time-fig"
ID_GRADE_OVERVIEW_FIG = "grade-overview"
ID_DETAILED_ASSESSMENT_GRADES_FIG = "detailed-assessment-grades"
ID_ASSESSMENT_TRENDS_FIG = "assessment-trends"
ID_MISSING_ASSESSMENT_FIG = "missing-assessments"
ID_GRADE_DISTRIBUTION_FIG = "grade-distribution"

# Feedback figure IDs
ID_SEI_RATINGS_FIG = "sei-ratings"
ID_SEI_COMMENTS_FIG = "sei-comments"
ID_EVAL_COURSE_CONTENT_FIG = "course-content"
ID_EVAL_SKILL_FIG = "skill-and-responsiveness"
ID_EVAL_CONTRIBUTION_FIG = "contribution-to-learning"

# Filter IDs
ID_COURSE_FILTER = "course-filter"
ID_ASSESSMENT_GROUP_FILTER = "assessment-group-filter"
ID_ASSESSMENT_FILTER = "assessment-filter"

# Various mappings for charts
MAPPING_SATISFACTION = {
    1: 'Very Dissatisfied',
    2: 'Dissatisfied',
    3: 'Neutral',
    4: 'Satisfied',
    5: 'Very Satisfied'
}
SCALE_LIKERT = [
    "Strongly disagree", 
    "Disagree",
    "Neutral", 
    "Agree",
    "Strongly agree"
]
SCALE_LIKERT_ALT = [
    "Poor", 
    "Fair", 
    "Satisfactory", 
    "Very good", 
    "Excellent"
]
COLORS_SATISFACTION = dict(zip(
    MAPPING_SATISFACTION.values(),
    px.colors.sequential.Viridis[::2]
))
