import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

app=dash.Dash(__name__)

df=pd.read_csv("weatherfact.csv")

