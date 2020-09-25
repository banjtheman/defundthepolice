import json
import glob
import os
import locale
import textwrap
import math

import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

STATES_FOLDER = "data/states/"

# set currency
try:
    locale.setlocale(locale.LC_ALL,'en_US.UTF-8')
except:
    

    cmd = "locale-gen en_US.UTF-8"
    os.system(cmd)
    #locale.setlocale(1,'en_US.UTF-8')
    os.environ["LANG "] = "en_US.UTF-8"
    os.environ["LANGUAGE "] = "en_US:en"
    os.environ["LC_ALL"] = "en_US.UTF-8"
    locale.setlocale(1,'en_US.UTF-8')

def draw_image(text ,bg_color,text_color,font):
    image_width = 600
    image_height = 335
    img = Image.new('RGB', (image_width, image_height), color = bg_color)
    canvas  = ImageDraw.Draw(img)
    font = ImageFont.truetype(font, size=24)
    pad = -25
    #print(text)
    for line in text:
        #print(line)

        #canvas.textsize(text, font=font)
        #canvas.text((10,10), text, fill=(255, 255, 0))
        text_width, text_height = canvas.textsize(line, font=font)
        
        x_pos = int((image_width - text_width) / 2)
        y_pos = int((image_height - text_height) / 2) + pad
        canvas.text((x_pos, y_pos), line, font=font, fill=text_color)
        pad += text_height + 5

    return img


def create_budget_json(state,county):
    # read budget.csv
    budget_csv_path = STATES_FOLDER + state + "/" + county + "/budget.csv"
    budget_df = pd.read_csv(budget_csv_path, index_col=False)
    #st.write(budget_df)

    # get police budget
    police_df = budget_df.loc[budget_df["item"] == "Police"]
    police_json = police_df.reset_index().to_json(orient="records")
    police_data = json.loads(police_json)[0]

    return police_data



def make_investment_image(investment,reinvest_money,bg_color,text_color,font):


    if investment == "Education":
        cpu_cost = 500.0
        laptops = int(math.ceil( reinvest_money / cpu_cost))

        laptops_string = str(locale.currency(laptops, symbol=False, grouping=True)).replace(".00","")
        text = "That translates to "+ laptops_string + " laptops for our community" 
        wrapped_string = textwrap.wrap(text, width=30)
        image = draw_image(wrapped_string,bg_color,text_color,font)

        st.image(image, use_column_width=True)
        st.write("*500 dollar laptops")
    
    #TODO add in extra investments

def main():
    st.header("Defund the police")

    # Select state
    states = os.listdir(STATES_FOLDER)
    state = st.selectbox("Select State", states)

    # select county
    counties = os.listdir(STATES_FOLDER + state)
    county = st.selectbox("Select County", counties)

    police_data = create_budget_json(state,county)
    #st.write(police_data)

    # Show budget for year
    money = locale.currency(police_data["budget"], grouping=True)
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
    #st.header(wrapped_string)

    fonts = glob.glob("fonts/*")
    font = st.selectbox("Select Font", fonts)


    bg_color = st.beta_color_picker('Background color', '#496D89')
    st.write('The current  background color is', bg_color)

    text_color = st.beta_color_picker('Text color', '#FFFFFF')
    st.write('The current text color is', text_color)


    image = draw_image(wrapped_string,bg_color,text_color,font)

    st.image(image, use_column_width=True)

    st.write("source: " + str(police_data["source"]))
    defund = st.slider("Defund %", 0, 100, 20)

    defund_decmial = float(defund / 100)
    reinvest_money = float(police_data["budget"]) * defund_decmial
    reinvest_money_string = locale.currency(reinvest_money, grouping=True)

    investments = ["Education","Healthcare", "Social Programs"]
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
    #st.header(realoc_str)
    image = draw_image(wrapped_string,bg_color,text_color,font)

    st.image(image, use_column_width=True)

    #based on input show what we can do...
    make_investment_image(realocate,reinvest_money,bg_color,text_color,font)
    
    


if __name__ == "__main__":
    main()
