import os
import logging

from sqlalchemy.orm import load_only
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from api.mapping import statemap, statereversemap
import pandas as pd


application = Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(application)

""" SQLAlchemy model for states and counties """


class States(db.Model):
    __tablename__ = 'budget_data'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(50))
    county = db.Column(db.String(50))
    year = db.Column(db.String(4))
    item = db.Column(db.String(50))
    budget = db.Column(db.Float)
    source = db.Column(db.String(150))

    def __init__(self, state, countyname, year, item, budget, source):
        self.state = state
        self.countyname = countyname
        self.year = year
        self.item = item
        self.budget = budget
        self.source = source

    def __repr__(self):
        return self.state


""" Checks for addition/modification of counties in state folders """


def checkcounties(statesfolder):

    os.chdir(os.getcwd())
    for i in statesfolder:
        os.chdir(os.path.join(os.getcwd(), i))
        countieslist = set(os.listdir())

        existingcounties = db.session.query(States.county).filter(
            States.state == statereversemap(i)
        )

        existingcounties = {k[0] for k in existingcounties}

        countiesdiff = (
            countieslist - existingcounties
        )  # Checks the difference between the counties in the database and the folders for each state

        if len(countiesdiff) == 0:
            logging.info("No changes in counties")
        else:
            logging.info("Changes Detected: "+ str(countiesdiff))

        if len(countiesdiff) > 0:
            for j in countiesdiff:
                df = pd.read_csv(os.path.join(os.getcwd(), j, "budget.csv"))
                df.to_sql("states", con=db.engine, if_exists="append", index=False)
        os.chdir("..")
    os.chdir("..")


""" Checks for addition/modification of state folders """


def checkstates():
    statesfolder = set(os.listdir(os.getcwd()))

    existingstates = set(States.query.with_entities(States.state))

    existingstates = statemap(existingstates)

    statesdiff = (
        statesfolder - existingstates
    )  # Checks the difference between the states in the database and the folders

    if len(statesdiff) == 0:
        logging.info("No changes in states")

    elif len(statesdiff) > 0:
        logging.info("Changes in states detected: "+ str(statesdiff))
        for i in statesdiff:

            os.chdir(os.path.join(os.getcwd(), i))
            countieslist = os.listdir()
            for j in countieslist:
                df = pd.read_csv(os.path.join(os.getcwd(), j, "budget.csv"))
                df.to_sql("states", con=db.engine, if_exists="append", index=False)

            os.chdir("..")
    checkcounties(statesfolder)


""" API endpoint to get data with state and county as parameters """


@application.route("/getdata")
def getdata():
    state = request.args.get("state")
    if len(state) == 2:
        state = state.upper()
    else:
        state = statereversemap(state)[0]
    county = request.args.get("county")
    data = States.query.filter(
        States.state == state, States.county == county
        ).all()
    responsedata = dict()
    responsedata["state"] = state
    responsedata["county"] = county

    if data:
        for budget_row in data:
            responsedata[budget_row.item] = budget_row.budget

        responsedata["year"] = budget_row.year
        responsedata["source"] = budget_row.source
    else:
        responsedata['error'] = f'Nothing returned for the state/county combination.'

    return responsedata


@application.route("/health")
def health():
    return jsonify({"true": True})


if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)
    os.chdir("..")

    os.chdir(os.path.join(os.getcwd(), "data", "states"))
    db.create_all()
    db.session.commit()
    checkstates()
    loglevel = logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    application.run(host="0.0.0.0", port="9000")
