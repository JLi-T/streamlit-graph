import streamlit as st
from fpdf import FPDF
import base64
import plotly.express as px
import pandas as pd
import json
from io import StringIO
import tempfile


with open('./data/systems.json') as s:
    json_data = json.load(s)

sys = pd.DataFrame(json_data)

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

# download in html
buffer = StringIO()
fig.write_html(buffer, include_plotlyjs='cdn')
html_bytes = buffer.getvalue().encode()

st.download_button(
    label='download graph in html',
    data=html_bytes,
    file_name='graph.html',
    mime='text/html'
)

# pdf

# report_text = st.text_input("Report Text")

export_as_pdf = st.button("Export graph as pdf")

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

if export_as_pdf:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.image(html_bytes, 10,10,100)
    
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")

    st.markdown(html, unsafe_allow_html=True)


    