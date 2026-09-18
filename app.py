import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🦓 2027 Sawmurai Gantt Chart", layout="wide")
st.title("🦓 2027 Calendar")

@st.cache_data
def load_data():
    df = pd.read_csv('2027 Calendar Planner - clickup.csv')
    df['Start Date'] = pd.to_datetime(df['Start Date'])
    df['End Date'] = pd.to_datetime(df['End Date'])
    
    # Filter for 2027 tasks
    df_2027 = df[(df['Start Date'] <= '2027-12-31') & (df['End Date'] >= '2027-01-01')].copy()
    
    # Add 1 day offset so 1-day milestones render with visible width in Plotly
    df_2027['Plot_End_Date'] = df_2027['End Date'] + pd.Timedelta(days=1)
    
    # Formatted Date Range string for hover tooltip
    def format_date_range(row):
        s = row['Start Date'].strftime('%b %d, %Y')
        e = row['End Date'].strftime('%b %d, %Y')
        return s if s == e else f"{s} - {e}"
        
    df_2027['Date Range'] = df_2027.apply(format_date_range, axis=1)
    
    # Categorization Tiers
    def assign_section(cat):
        if cat in ['CAE', 'RISE', 'WPO']:
            return 'Section 1: RISE & CAE Events'
        elif cat in ['SIFP Grant', 'National Grant']:
            return 'Section 2: Grant Press Events'
        else:
            return 'Section 3: Program Cohorts & Masterclasses'
            
    df_2027['Section'] = df_2027['Category'].apply(assign_section)
    
    # Section Ordering
    section_order = {
        'Section 1: RISE & CAE Events': 1,
        'Section 2: Grant Press Events': 2,
        'Section 3: Program Cohorts & Masterclasses': 3
    }
    df_2027['Section_Order'] = df_2027['Section'].map(section_order)
    
    return df_2027.sort_values(by=['Section_Order', 'Start Date', 'End Date'], ascending=[True, True, True])

df = load_data()

# Sidebar Interactive Filters
st.sidebar.header("Interactive Filters")
selected_section = st.sidebar.multiselect("Filter by Section", options=df['Section'].unique(), default=df['Section'].unique())
selected_assignee = st.sidebar.multiselect("Filter by Assignee", options=df['Assignee'].dropna().unique(), default=df['Assignee'].dropna().unique())

filtered_df = df[(df['Section'].isin(selected_section)) & (df['Assignee'].isin(selected_assignee))]

# Color Scheme
color_map = {
    'Program': '#2563EB', 'CAE': '#EA580C', 'SIFP Grant': '#7C3AED',
    'National Grant': '#DB2777', 'RISE': '#059669', 'WPO': '#D97706', 'Break': '#6B7280'
}

# Generate Plotly Gantt Chart
fig = px.timeline(
    filtered_df, 
    x_start="Start Date", 
    x_end="Plot_End_Date", 
    y="Item", 
    color="Category",
    hover_data={
        "Plot_End_Date": False,
        "Date Range": True,
        "Assignee": True,
        "Location": True,
        "Task Type": True
    },
    color_discrete_map=color_map,
    title="Interactive 2027 Timeline Strategy"
)

fig.update_yaxes(autorange="reversed")
fig.update_layout(height=850, xaxis_title="2027 Timeline", yaxis_title="")

st.plotly_chart(fig, use_container_width=True)
