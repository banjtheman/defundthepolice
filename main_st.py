import streamlit as st

from apps import home, county_compare

PAGES = {
    "Home": home.view,
    "County Compare": county_compare.view,
}


def show_menu():
    st.sidebar.title("Social Media Toolkit Generator")
    st.sidebar.header("Defund the Police")

    dark_theme = st.sidebar.checkbox("Dark theme")
    if dark_theme:
        show_dark_theme()
    else:
        show_light_theme()

    st.sidebar.markdown(
        "“Defund the police” means reallocating or redirecting funding away from the "
        "police department to other government agencies funded by the local municipality."
    )

    st.sidebar.markdown(
        "The goal of this tool is to highlight how much money local communities spend on "
        "Police, and then how reallocating funds can make a direct impact into their community"
    )

    # TODO add more "apps" such as county compare tool
    selection = st.sidebar.selectbox("Go To", list(PAGES.keys()))
    page = PAGES.get(selection)
    page()


def show_dark_theme():
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


def show_light_theme():
    hide_streamlit_style = """
                <title> Half Explot </title>
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                .sidebar .sidebar-content {background-image: linear-gradient(180deg,#ff6b6b,#ffe66d);}
                .btn-outline-secondary {
                border-color: #09ab3b85;
                color: #000000;
                }
                body {
                color: #000000;
                text-align: left;
                background-color: #fffff;
                }
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def main():
    show_menu()


if __name__ == "__main__":
    main()
