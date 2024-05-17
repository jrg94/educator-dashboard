import pandas as pd
import plotly.express as px

# Data URLS
URL_ASSESSMENTS = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/assessments/assessments.csv"
URL_ASSESSMENT_GRADES = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/assessments/grades.csv"
URL_ASSESSMENT_GROUPS = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/assessments/groups.csv"
URL_ASSESSMENT_REVIEWS = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/assessments/reviews.csv"
URL_COURSES = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/lookup-tables/courses.csv"
URL_COURSE_SECTIONS = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/lookup-tables/sections.csv"
URL_EVALUATION_SURVEY_HISTORY = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/raw-data/evaluation-survey-history.csv"
URL_SEI_COMMENTS = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/student-evaluations-of-instruction/comments.csv"
URL_SEI_COHORT_SCORES = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/student-evaluations-of-instruction/cohort-scores.csv"
URL_SEI_QUESTIONS = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/student-evaluations-of-instruction/questions.csv"
URL_SEI_INSTRUCTOR_SCORES = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/student-evaluations-of-instruction/instructor-scores.csv"
URL_SEI_REPORTS = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/student-evaluations-of-instruction/reports.csv"
URL_SEMESTERS = "https://raw.githubusercontent.com/jrg94/personal-data/main/education/lookup-tables/semesters.csv"

# Page constants
HOME_PAGE_PATH = "/"
HOME_PAGE_NAME = "Home"
HOME_PAGE_TITLE = "The Educator Dashboard"

ASSESSMENT_PAGE_PATH = "/assessment"
ASSESSMENT_PAGE_NAME = "Assessment"
ASSESSMENT_PAGE_TITLE = f"{HOME_PAGE_TITLE}: {ASSESSMENT_PAGE_NAME}"

FEEDBACK_PAGE_PATH = "/feedback"
FEEDBACK_PAGE_NAME = "Feedback"
FEEDBACK_PAGE_TITLE = f"{HOME_PAGE_TITLE}: {FEEDBACK_PAGE_NAME}"

HISTORY_PAGE_PATH = "/history"
HISTORY_PAGE_NAME = "History"
HISTORY_PAGE_TITLE = f"{HOME_PAGE_TITLE}: {HISTORY_PAGE_NAME}"

# Column headings
COLUMN_ASSESSMENT_ID = "Assessment ID"
COLUMN_ASSESSMENT_GROUP_ID = "Assessment Group ID"
COLUMN_ASSESSMENT_GROUP_NAME = "Assessment Group Name"
COLUMN_ASSESSMENT_GROUP_WEIGHT = "Assessment Group Weight"
COLUMN_ASSESSMENT_NAME = "Assessment Name"
COLUMN_COHORT = "Cohort"
COLUMN_COMMENT = "Comment"
COLUMN_COURSE_DEPARTMENT = "Course Department"
COLUMN_COURSE_ID = "Course ID"
COLUMN_COURSE_NAME = "Course Name"
COLUMN_COURSE_NUMBER = "Course Number"
COLUMN_COURSE_TYPE = "Course Type"
COLUMN_DATE_TIME = "DateTime"
COLUMN_EDUCATOR_TITLE = "Educator Title"
COLUMN_ENROLLMENT_TOTAL = "Enrollment Total"
COLUMN_GRADE = "Grade"
COLUMN_MEAN = "Mean"
COLUMN_SECTION_BUILDING = "Section Building"
COLUMN_SECTION_ID = "Section ID"
COLUMN_SECTION_ROOM_NUMBER = "Section Room Number"
COLUMN_SECTION_START_TIME = "Section Start Time"
COLUMN_SEMESTER_ID = "Semester ID"
COLUMN_SEMESTER_SEASON = "Semester Season"
COLUMN_SEMESTER_YEAR = "Semester Year"
COLUMN_QUESTION = "SEI Question"
COLUMN_QUESTION_ID = "SEI Question ID"
COLUMN_REPORT_ID = "SEI Report ID"
COLUMN_TIMESTAMP = "Timestamp"
COLUMN_TIME_TAKEN = "Time Taken"
COLUMN_TOTAL = "Total"

# Analysis headings
COLUMN_AVERAGE = "Average"
COLUMN_COUNT = "Count"
COLUMN_CUMULATIVE_ENROLLMENT_TOTAL = "Cumulative Enrollment Total"
COLUMN_CLASSROOM = "Classroom"
COLUMN_MEDIAN = "Median"
COLUMN_PERCENTAGE = "Percentage"
COLUMN_PERCENT_MISSING = "Percent Missing"
COLUMN_SEMESTER = "Semester"
COLUMN_WORD = "Word"

# Data IDs
ID_ASSIGNMENT_SURVEY_DATA = "assignment-survey-data"
ID_COURSE_EVAL_DATA = "course-eval-data"
ID_EDUCATION_DATA = "education"
ID_HISTORY_DATA = "history"
ID_SEI_DATA = "sei-data"
ID_SEI_COMMENTS_DATA = "sei-comments-data"

# Assessment figure IDs
ID_ASSESSMENT_GROUP_TIME_FIG = "assessment-group-time-fig"
ID_ASSESSMENT_TRENDS_FIG = "assessment-trends"
ID_DETAILED_ASSESSMENT_GRADES_FIG = "detailed-assessment-grades"
ID_GRADE_OVERVIEW_FIG = "grade-overview"
ID_GRADE_DISTRIBUTION_FIG = "grade-distribution"
ID_MISSING_ASSESSMENT_FIG = "missing-assessments"
ID_VALUE_FIG = "value-to-time-ratio-fig"

# Feedback figure IDs
ID_SEI_RATINGS_FIG = "sei-ratings"
ID_SEI_COMMENTS_FIG = "sei-comments"
ID_EVAL_COURSE_CONTENT_FIG = "course-content"
ID_EVAL_SKILL_FIG = "skill-and-responsiveness"
ID_EVAL_CONTRIBUTION_FIG = "contribution-to-learning"

# History figure IDs
ID_ROOM_COUNTS_FIG = "room-counts"
ID_TIME_COUNTS_FIG = "time-counts"
ID_STUDENT_COUNTS_FIG = "student-counts"
ID_COURSE_HISTORY_LIST = "course-list"

# Filter IDs
ID_COURSE_FILTER = "course-filter"
ID_ASSESSMENT_GROUP_FILTER = "assessment-group-filter"
ID_ASSESSMENT_FILTER = "assessment-filter"

# Category orders constants
ASSESSMENT_ORDER = pd.read_csv(URL_ASSESSMENTS)[COLUMN_ASSESSMENT_NAME]
COHORT_ORDER = ["Instructor", "Department", "College", "University"]
METRIC_ORDER = [COLUMN_AVERAGE, COLUMN_MEDIAN]
SEMESTER_ORDER = pd.read_csv(URL_SEMESTERS)[
    [COLUMN_SEMESTER_SEASON, COLUMN_SEMESTER_YEAR]
].astype(str).apply(" ".join, axis=1)
QUESTION_ORDER = pd.read_csv(URL_SEI_QUESTIONS)[COLUMN_QUESTION]


# TODO: remove these and rely on the data tables
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
