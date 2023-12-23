import pandas as pd
import plotly.express as px

from constants import std_time, review_count, avg_time, median_time

def create_time_fig(assignment_survey_data: pd.DataFrame, col: str):
  """
  Creates a figure of the average and median time spent
  on each assignment.
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
  print(to_plot)
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
  time_fig.update_traces(textfont_size=12, textangle=0, textposition="inside", insidetextanchor="start", cliponaxis=False)
  return time_fig