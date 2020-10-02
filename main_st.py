import streamlit as st

from apps import home, county_compare

PAGES = {
    "Home": home.view,
    "County Compare": county_compare.view,
}


def show_menu():
    st.sidebar.title("Social Media Toolkit Generator")
    st.sidebar.header("Defund the Police")

    st.sidebar.markdown(
        "“Defund the police” means reallocating or redirecting funding away from the "
        "police department to other government agencies funded by the local municipality."
    )

    st.sidebar.markdown(
        "The goal of this tool is to highlight how much money local communities spend on "
        "Police, and then how reallocating funds can make a direct impact into their community"
    )

    # TODO add more "apps" such as county compare tool
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES.get(selection)
    page()


def main():
    show_menu()


if __name__ == "__main__":
    main()
