import os
import textwrap
import math

import streamlit as st
from PIL import Image, ImageDraw, ImageFont

from apps.configs import STATES_FOLDER
from apps.utils import draw_image, create_budget_json, fonts
from apps.viz import ChartDisplay, ChartTypes

st.set_option("deprecation.showfileUploaderEncoding", False)


def make_investment_image(investment, reinvest_money, bg_color, text_color, font):
    if investment == "Education":
        cpu_cost = 500.0
        laptops = int(math.ceil(reinvest_money / cpu_cost))

        laptops_string = str(f"{laptops:,}")
        text = "That translates to " + laptops_string + " laptops for our community"
        wrapped_string = textwrap.wrap(text, width=30)
        image = draw_image(wrapped_string, bg_color, text_color, font)

        st.image(image, use_column_width=True)
        st.write("*500 dollar laptops")

    # TODO add in extra investments


def get_concat_v_cut(im1, im2):
    dst = Image.new("RGB", (min(im1.width, im2.width), im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def bar_chart_banner(bar_chart, state, county, bg_color, font, text, text_color):
    # lets make simple image
    image_width = 600
    image_height = 200
    img = Image.new("RGB", (image_width, image_height), color=bg_color)
    canvas = ImageDraw.Draw(img)
    font = ImageFont.truetype(font, size=24)
    pad = -25
    starter = 40
    # print(text)
    for line in text:
        # print(line)

        # canvas.textsize(text, font=font)
        # canvas.text((10,10), text, fill=(255, 255, 0))
        text_width, text_height = canvas.textsize(line, font=font)

        x_pos = int((image_width - text_width) / 2)
        y_pos = starter + pad
        canvas.text((x_pos, y_pos), line, font=font, fill=text_color)
        pad += text_height + 5

    dst = get_concat_v_cut(img, bar_chart)
    st.image(dst)


def view():
    st.header("Select Community")

    # Select state
    states = os.listdir(STATES_FOLDER)
    state = st.selectbox("Select State", states)

    # select county
    counties = os.listdir(STATES_FOLDER + state)
    county = st.selectbox("Select County", counties)

    police_data, budget_df = create_budget_json(state, county)
    st.write(budget_df)

    # Show budget for year
    money = "$" + f'{police_data["budget"]:,}'
    header_string = (
        # "For "
        # + str(police_data["year"])
        # + " "
        str(county)
        + " County, "
        + str(state)
        + " has a police budget of "
        + str(money)
    )
    wrapped_string = textwrap.wrap(header_string, width=30)
    # st.header(wrapped_string)

    font = st.selectbox("Select Font", fonts())

    bg_color = st.beta_color_picker("Background color", "#496D89")
    st.write("The current  background color is", bg_color)

    text_color = st.beta_color_picker("Text color", "#FFFFFF")
    st.write("The current text color is", text_color)

    image = draw_image(wrapped_string, bg_color, text_color, font)

    st.image(image, use_column_width=True)

    st.write("source: " + str(police_data["source"]))
    defund = st.slider("Defund %", 0, 100, 20)

    defund_decmial = float(defund / 100)
    reinvest_money = float(police_data["budget"]) * defund_decmial
    reinvest_money_string = "$" + f"{int(reinvest_money):,}"

    investments = ["Education", "Healthcare", "Social Programs"]
    realocate = st.selectbox("Reinvest", investments)

    realoc_str = (
        "By defunding the police by "
        + str(defund)
        + "% we can invest "
        + reinvest_money_string
        + " into "
        + realocate
    )

    wrapped_string = textwrap.wrap(realoc_str, width=30)
    # st.header(realoc_str)
    image = draw_image(wrapped_string, bg_color, text_color, font)

    st.image(image, use_column_width=True)

    # based on input show what we can do...
    make_investment_image(realocate, reinvest_money, bg_color, text_color, font)

    # TODO make this another "app" in sidebar for users to select
    selected_chart = st.selectbox("Chart Types", ChartTypes.list())
    ChartDisplay(data=budget_df, chart=selected_chart).get_chart()

    wrapped_string = textwrap.wrap(header_string + "\n" + realoc_str, width=30)
    uploaded_file = st.file_uploader("Choose an Image File")
    if uploaded_file is not None:
        try:
            bar_chart = Image.open(uploaded_file)
            bar_chart_banner(
                bar_chart, state, county, bg_color, font, wrapped_string, text_color
            )
        except Exception as error:
            st.error(error)

    hide_streamlit_style = """
                <title> Half Explot </title>
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                .sidebar .sidebar-content {background-image: linear-gradient(180deg,#4CA1AF,#2c3e50);}
                .btn-outline-secondary {
                border-color: #09ab3b85;
                color: #f9f9f9;
                }
                body {
                color: #fafafa;
                text-align: left;
                background-color: #262730;
                }
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
