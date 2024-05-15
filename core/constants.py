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

# Column headings
COLUMN_ASSESSMENT_ID = "Assessment ID"
COLUMN_ASSESSMENT_GROUP_ID = "Assessment Group ID"
COLUMN_ASSESSMENT_GROUP_NAME = "Assessment Group Name"
COLUMN_ASSESSMENT_NAME = "Assessment Name"
COLUMN_COHORT = "Cohort"
COLUMN_COURSE_DEPARTMENT = "Course Department"
COLUMN_COURSE_ID = "Course ID"
COLUMN_COURSE_NUMBER = "Course Number"
COLUMN_GRADE = "Grade"
COLUMN_SECTION_ID = "Section ID"
COLUMN_SEMESTER_ID = "Semester ID"
COLUMN_SEMESTER_SEASON = "Semester Season"
COLUMN_SEMESTER_YEAR = "Semester Year"
COLUMN_QUESTION_ID = "SEI Question ID"
COLUMN_REPORT_ID = "SEI Report ID"
COLUMN_TOTAL = "Total"

# Data IDs
ID_ASSIGNMENT_SURVEY_DATA = "assignment-survey-data"
ID_COURSE_EVAL_DATA = "course-eval-data"
ID_EDUCATION_DATA = "education"
ID_HISTORY_DATA = "history"
ID_SEI_DATA = "sei-data"
ID_SEI_COMMENTS_DATA = "sei-comments-data"

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

# History figure IDs
ID_TIME_COUNTS_FIG = "time-counts"

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
