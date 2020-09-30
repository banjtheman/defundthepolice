import sys, argparse, logging
import json

import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

def bar_graph(df):

    st.info("Select which columns to display on the bar chart below which displays percent of budget")
    selectd_cols = st.multiselect('Select columns',list(df["item"]),list(df["item"]))
    df = df.loc[df['item'].isin(selectd_cols)]

    #x_col = st.selectbox("Select x axis for bar chart", df.columns)
    #xcol_string=x_col+":O"
    #if st.checkbox("Show as continuous?",key="bar_chart_x_is_cont"):
    x_col = "percent"
    xcol_string=x_col+":Q"
    y_col = "item"
    z_col = "percent"
    #y_col = st.selectbox("Select y axis for bar chart", df.columns)
    #z_col = st.selectbox("Select z axis for bar chart", df.columns)

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(x=xcol_string, y=y_col, color=z_col,tooltip=list(df.columns))
        #.interactive()
        #.properties(title="Defund The Police")
        .configure_title(fontSize=20,)
        .configure_axis(labelFontSize=10, titleFontSize=10)
        .configure_legend(labelFontSize=10, titleFontSize=10)
    )

    st.altair_chart(chart, use_container_width=True)
    #TODO figure out saving images
    #chart.save('chart.png')
    return chart