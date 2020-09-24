import json
import glob
import os
import locale

import pandas as pd
import streamlit as st


STATES_FOLDER = "data/states/"

# set currency

locale.setlocale(locale.LC_ALL, "")


def main():
    st.header("Defund the police")

    # Select state
    states = os.listdir(STATES_FOLDER)
    state = st.selectbox("Select State", states)

    # select county
    counties = os.listdir(STATES_FOLDER + state)
    county = st.selectbox("Select County", counties)

    # read budget.csv
    budget_csv_path = STATES_FOLDER + state + "/" + county + "/budget.csv"
    budget_df = pd.read_csv(budget_csv_path, index_col=False)
    st.write(budget_df)

    # get police budget
    police_df = budget_df.loc[budget_df["item"] == "Police"]
    police_json = police_df.reset_index().to_json(orient="records")
    police_data = json.loads(police_json)[0]
    #st.write(police_data)

    # Show budget for year
    money = locale.currency(police_data["budget"], grouping=True)
    header_string = (
        "For "
        + str(police_data["year"])
        + " "
        + str(county)
        + " county,"
        + str(state)
        + " has a police budget of "
        + str(money)
    )
    st.header(header_string)

    st.write("source: " + str(police_data["source"]))
    defund = st.slider("Defund %", 0, 100, 20)

    defund_decmial = float(defund / 100)
    reinvest_money = float(police_data["budget"]) * defund_decmial
    reinvest_money_string = locale.currency(reinvest_money, grouping=True)

    investments = ["healthcare", "social programs", "education"]
    realocate = st.selectbox("Reinvest", investments)

    realoc_str = (
        "By defunding the police by "
        + str(defund)
        + "% we can invest "
        + reinvest_money_string
        + " into "
        + realocate
    )

    st.header(realoc_str)


    #based on input show what we can do...


if __name__ == "__main__":
    main()
