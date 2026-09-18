import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="2027 Master Gantt Chart", layout="wide")
st.title("📅 2027 Master Organizational Calendar & Program Timeline")

@st.cache_data
def load_data():
    df = pd.read_csv('2027 Calendar Planner - clickup.csv')
    df['Start Date'] = pd.to_datetime(df['Start Date'])
    df['End Date'] = pd.to_datetime(df['End Date'])
    
    df_2027 = df[(df['Start Date'] <= '2027-12-31') & (df['End Date'] >= '2027-01-01')].copy()
    
    def assign_section(cat):
        if cat in ['CAE', 'RISE', 'WPO']:
            return 'Section 1: RISE & CAE Events'
        elif cat in ['SIFP Grant', 'National Grant']:
            return 'Section 2: Grant Press Events'
        else:
            return 'Section 3: Program Cohorts & Masterclasses'
            
    df_2027['Section'] = df_2027['Category'].apply(assign_section)
    return df_2027.sort_values(by=['Section', 'Start Date'])

df = load_data()

st.sidebar.header("Interactive Filters")
selected_section = st.sidebar.multiselect("Filter by Section", options=df['Section'].unique(), default=df['Section'].unique())
selected_assignee = st.sidebar.multiselect("Filter by Assignee", options=df['Assignee'].dropna().unique(), default=df['Assignee'].dropna().unique())

filtered_df = df[(df['Section'].isin(selected_section)) & (df['Assignee'].isin(selected_assignee))]

color_map = {
    'Program': '#2563EB', 'CAE': '#EA580C', 'SIFP Grant': '#7C3AED',
    'National Grant': '#DB2777', 'RISE': '#059669', 'WPO': '#D97706', 'Break': '#6B7280'
}

fig = px.timeline(
    filtered_df, 
    x_start="Start Date", 
    x_end="End Date", 
    y="Item", 
    color="Category",
    hover_data=["Assignee", "Location", "Task Type"],
    color_discrete_map=color_map,
    title="Interactive 2027 Timeline Strategy"
)

fig.update_yaxes(autorange="reversed")
fig.update_layout(height=800, xaxis_title="2027 Timeline", yaxis_title="")

st.plotly_chart(fig, use_container_width=True)