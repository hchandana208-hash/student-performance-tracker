
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Subject Performance Tracker", layout="wide")
st.title('Subject-Wise Performance Tracker')

# List of subjects requested
subjects = ['OOPS', 'DS', 'DBMS', 'PAI', 'CN', 'COA']

st.sidebar.header('Enter Subject Marks (%)')

# Collect past and present marks for each subject
data_list = []
for subject in subjects:
    st.sidebar.subheader(f'{subject}')
    past = st.sidebar.number_input(f'Past Mark - {subject}', min_value=0.0, max_value=100.0, value=75.0, step=1.0)
    present = st.sidebar.number_input(f'Present Mark - {subject}', min_value=0.0, max_value=100.0, value=70.0, step=1.0)
    data_list.append({
        'Subject': subject,
        'Past_Percentage': past,
        'Present_Percentage': present,
        'Difference': present - past
    })

data = pd.DataFrame(data_list)

# Overall calculations
avg_past = data['Past_Percentage'].mean()
avg_present = data['Present_Percentage'].mean()

def get_grade(score):
    if score >= 90: return 'A+'
    elif score >= 80: return 'A'
    elif score >= 70: return 'B'
    elif score >= 60: return 'C'
    else: return 'F'

# Layout metrics
col1, col2, col3 = st.columns(3)
col1.metric("Present Average", f"{avg_present:.2f}%", delta=f"{avg_present - avg_past:.2f}%")
col2.metric("Predicted Grade", get_grade(avg_present))
col3.metric("Past Average", f"{avg_past:.2f}%")

st.markdown("---")

# Identify weak spots (subjects where present mark is lower than past mark or below 50%)
weak_subjects = data[data['Difference'] < 0]['Subject'].tolist()
critical_subjects = data[data['Present_Percentage'] < 50]['Subject'].tolist()

if weak_subjects:
    st.warning(f"⚠️ **Weak Spots (Drop in performance):** {', '.join(weak_subjects)}")
if critical_subjects:
    st.error(f"🚨 **Critical Attention Needed (< 50%):** {', '.join(critical_subjects)}")
if not weak_subjects and not critical_subjects:
    st.success("🎉 **Great job!** You are maintaining or improving your performance across all subjects.")

# Data Table
st.subheader("Marks Summary")
st.dataframe(data[['Subject', 'Past_Percentage', 'Present_Percentage', 'Difference']], use_container_width=True)

# Graph Visualization
fig = go.Figure()
fig.add_trace(go.Bar(
    x=data['Subject'], 
    y=data['Past_Percentage'], 
    name='Past Marks (%)', 
    marker_color='rgb(158,202,225)'
))
fig.add_trace(go.Bar(
    x=data['Subject'], 
    y=data['Present_Percentage'], 
    name='Present Marks (%)', 
    marker_color='rgb(49,130,189)'
))

fig.update_layout(
    title='Subject-Wise Past vs Present Comparison',
    xaxis_title='Subjects',
    yaxis_title='Marks (%)',
    barmode='group',
    yaxis=dict(range=[0, 100])
)

st.plotly_chart(fig, use_container_width=True)