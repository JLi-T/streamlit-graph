import streamlit as st
import plotly.express as px
import pandas as pd
import json

# data 1
with open('./data/population.json') as j:
    json_data = json.load(j)

df = pd.DataFrame(json_data)

fig = px.scatter(
    df,
    x="year",
    y="people",
    color="sex",
    size="age",
    hover_data=["age"],
)

event = st.plotly_chart(fig, key="year", on_select="rerun", use_container_width=True)

############################################################
# data 2
with open('./data/systems.json') as s:
    json_data = json.load(s)

sys = pd.DataFrame(json_data)

fig = px.scatter(
    sys,
    x="year",
    y="users",
    color="system",
    size="age",
    hover_data=["age"],
)

event = st.plotly_chart(fig, key="color", on_select="rerun", use_container_width=True)

############################################################
# data 3
with open('./data/ice.json') as s:
    json_data = json.load(s)

sys = pd.DataFrame(json_data)

fig = px.scatter(
    sys,
    x="year",
    y="popularity",
    color="flavor",
    hover_data=["flavor"],
)

event = st.plotly_chart(fig, key="flavor", on_select="rerun", use_container_width=True)

############################################################
#bar
import plotly.graph_objects as go

with open('./data/systems.json') as s:
    json_data = json.load(s)

windows_data = [entry['users'] for entry in json_data if entry['system']== 'Windows']
mac_data = [entry['users'] for entry in json_data if entry['system']== 'Mac']
linux_data = [entry['users'] for entry in json_data if entry['system']== 'Linux']

# Group data together
hist_data = [sum(windows_data), sum(mac_data), sum(linux_data)]

group_labels = ['windows', 'mac', 'linux']

# Create distplot with custom bin_size
fig = go.Figure(data=[
    go.Bar(name="Users", x=group_labels, y=hist_data)
])

fig.update_layout(
    title='Number of Users by System',
    xaxis_title='System',
    yaxis_title='Number of Users',
    barmode='group'
)

# Plot!
st.plotly_chart(fig, use_container_width=True)

# ############################################################
# 3d
import plotly.graph_objects as G
import numpy as N
 
 
n = 100
 
figure = G.Figure(data=[G.Mesh3d(x=(55*N.random.randn(n)),
                   y=(50*N.random.randn(n)),
                   z=(25*N.random.randn(n)),
                   opacity=0.8,
                   color='rgba(244,22,100,0.6)'
                  )])
 
 
 
figure.show()

# ############################################################
import plotly.express as px

df = px.data.gapminder()

fig = px.scatter(
    df.query("year==2007"),
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
)

tab1, tab2 = st.tabs(["Streamlit theme", "Plotly native theme"])
with tab1:
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    st.plotly_chart(fig, theme=None, use_container_width=True)