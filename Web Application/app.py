"""
import streamlit as st
from components.perspective_1 import perspective_1_component
from components.perspective_2 import perspective_2_component
from components.merged_solution import merged_solution_component
from components.prediction import prediction_component

st.set_page_config(page_title="Data Mining Project", layout="wide")

def main():
    st.sidebar.title("Navigation")
    options = ["Value and Preference Perspective", "Activity and Engagement Perspective", "Merged Solution", "Prediction"]
    choice = st.sidebar.radio("Go to:", options)

    if choice == "Value and Preference Perspective":
        perspective_1_component()
    elif choice == "Activity and Engagement Perspective":
        perspective_2_component()
    elif choice == "Merged Solution":
        merged_solution_component()
    elif choice == "Prediction":
        prediction_component()

if __name__ == "__main__":
    main()

"""

import streamlit as st
from components.home_page import home_page_component
from components.perspective_1 import perspective_1_component
from components.perspective_2 import perspective_2_component
from components.merged_solution import merged_solution_component
from components.prediction import prediction_component

def main():
    # Sidebar navigation
    st.sidebar.title("Navigation")
    options = [
        "Home Page",
        "Value and Preference Perspective",
        "Activity and Engagement Perspective",
        "Merged Solution",
        "Prediction"
    ]

    # Sidebar radio button for navigation
    choice = st.sidebar.radio("Go to:", options)

    # Render the selected page
    if choice == "Home Page":
        home_page_component()
    elif choice == "Value and Preference Perspective":
        perspective_1_component()
    elif choice == "Activity and Engagement Perspective":
        perspective_2_component()
    elif choice == "Merged Solution":
        merged_solution_component()
    elif choice == "Prediction":
        prediction_component()

if __name__ == "__main__":
    main()

