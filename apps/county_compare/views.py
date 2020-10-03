import os

import streamlit as st

from apps.configs import STATES_FOLDER
from apps.county_compare.utils import CountyInfo
from apps.utils import fonts
from apps.viz import ChartTypes


def get_county(state):
    return os.listdir(STATES_FOLDER + state)


def view():
    # Select state
    states = os.listdir(STATES_FOLDER)
    first_state = st.selectbox("Select First State", states)
    second_state = st.selectbox("Select Second State", states)

    # select county
    first_county = st.selectbox("Select First County", get_county(first_state))
    second_county = st.selectbox("Select Second County", get_county(second_state))

    if first_county == second_county:
        st.error("Please select different counties!!")
        st.stop()

    font = st.selectbox("Select Font", fonts())

    bg_color = st.beta_color_picker("Background color", "#496D89")
    st.write("The current  background color is", bg_color)

    text_color = st.beta_color_picker("Text color", "#FFFFFF")
    st.write("The current text color is", text_color)

    chart = st.selectbox("Chart Types", ChartTypes.list())

    first_county_info = CountyInfo(
        first_county, first_state, bg_color, text_color, font, chart
    )
    second_county_info = CountyInfo(
        second_county, second_state, bg_color, text_color, font, chart
    )

    first_county_police_data, first_county_budget_df = first_county_info.get_data()
    second_county_police_data, second_county_budget_df = second_county_info.get_data()

    st.write(first_county_budget_df)
    st.write(second_county_budget_df)

    st.image(first_county_info.get_budget_for_year(), use_column_width=True)
    st.image(second_county_info.get_budget_for_year(), use_column_width=True)

    first_county_info.chart_display()
    second_county_info.chart_display()
