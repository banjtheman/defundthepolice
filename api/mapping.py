""" statereversemap() is used to map names of states to their corresponding string used in the ORM model
    For example: 'Virginia' to ('VA',)

    statemap() is used to map the string in ORM model to the name of states as seen in the data folder.
    For example: ('VA',) to Virginia

    This file can be removed in the future if the string for states in the CSV files and the names of the folders are same.
"""


def statereversemap(state):
    if state.lower() == "virginia":
        return ("VA",)
    elif state.lower() == "texas":
        return ("TX",)


def statemap(statesset):

    try:
        if statesset != None:
            statesset.remove(("TX",))
            statesset.add("Texas")
            statesset.remove(("VA",))
            statesset.add("Virginia")
        else:
            stateset = set()
    except:
        pass
    return statesset
