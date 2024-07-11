# imports
import streamlit as st

import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

import pandas as pd
import json
from io import StringIO

from fpdf import FPDF
import base64
import tempfile

############################################################
# color
pio.templates.default = "plotly"
# change colors using (in fig)

    # color_discrete_sequence=[
    #     "#0068c9",
    #     "#83c9ff",
    #     "#ff2b2b",
    #     "#ffabab",
    #     "#29b09d",
    #     "#7defa1",
    #     "#ff8700",
    #     "#ffd16a",
    #     "#6d3fc0",
    #     "#d5dae5",
    # ],

############################################################
# functions
def load_json(path):
    with open(path) as s:
        return json.load(s)
    
def download_links(graph, title):

    def download_html(fig, name):
        buffer = StringIO()
        fig.write_html(buffer, include_plotlyjs='cdn')
        html_bytes = buffer.getvalue().encode()

        st.download_button(
            label=f"download {name} graph as html",
            data=html_bytes,
            file_name=f"graph-{name}.html",
            mime='text/html'
        )

    def download_pdf(fig, name):
        def save_temp(fig):
            tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            fig.write_image(tmpfile.name)
            return tmpfile.name
        
        tmpfile_path = save_temp(fig)

        export_pdf = st.button(f"download {name} graph as pdf")

        def create_download_link(val, filename):
            b64 = base64.b64encode(val)
            return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'
        
        if export_pdf:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 24)
            # change the size if needed
            pdf.image(tmpfile_path, 5,5,200)    
            html = create_download_link(pdf.output(dest="S").encode("latin-1"), f"graph-{name}")
            st.markdown(html, unsafe_allow_html=True)

    download_html(graph, title)
    download_pdf(graph, title)
    # create a divider line
    st.markdown("***")

############################################################
# graphs
# data 1
data1 = load_json('./data/population.json')
df = pd.DataFrame(data1)

fig = px.scatter(
    df,
    title="Population data",
    x="year",
    y="people",
    color="sex",
    size="age",
    hover_data=["age"],
)

event = st.plotly_chart(fig, key="year", on_select="rerun", use_container_width=True)
download_links(fig, "population")

# data 2
data2 = load_json('./data/systems.json')
df = pd.DataFrame(data2)

sys = pd.DataFrame(data2)

fig = px.scatter(
    sys,
    title="Systems",
    x="year",
    y="users",
    color="system",
    size="age",
    hover_data=["age"],
)

event = st.plotly_chart(fig, key="color", on_select="rerun", use_container_width=True)
download_links(fig, "systems")

# data 3
data3 = load_json('./data/ice.json')
df = pd.DataFrame(data3)

sys = pd.DataFrame(data3)

fig = px.scatter(
    sys,
    title="Ice cream flavors",
    x="year",
    y="popularity",
    color="flavor",
    hover_data=["flavor"],
)

event = st.plotly_chart(fig, key="flavor", on_select="rerun", use_container_width=True)
download_links(fig, "ice-cream")

#bar

data4 = load_json('./data/systems.json')
df = pd.DataFrame(data4)

windows_data = [entry['users'] for entry in data4 if entry['system']== 'Windows']
mac_data = [entry['users'] for entry in data4 if entry['system']== 'Mac']
linux_data = [entry['users'] for entry in data4 if entry['system']== 'Linux']

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

st.plotly_chart(fig, use_container_width=True)
download_links(fig, "systems-bar")

# 3d
# import plotly.graph_objects as G
# import numpy as N
 
 
# n = 100
 
# figure = G.Figure(data=[G.Mesh3d(x=(55*N.random.randn(n)),
#                    y=(50*N.random.randn(n)),
#                    z=(25*N.random.randn(n)),
#                    opacity=0.8,
#                    color='rgba(244,22,100,0.6)'
#                   )])
 
# figure.show()

# world data

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
download_links(fig, "world-population")