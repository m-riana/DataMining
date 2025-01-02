import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from utils.plot_helpers import cluster_profiles_interactive


def perspective_1_component():
    """
    Component for Value and Preference Perspective (Perspective 1).
    """
    st.title("Value and Preference Perspective")

    st.write("""
    The Value and Preference Perspective focuses on understanding client behavior and preferences based on spending 
    patterns and preferences for specific types of vendors. This perspective was selected to group clients into clusters 
    that reflect their value to the business and their preference for certain vendor types, enabling targeted marketing 
    strategies and personalized offers.
    """)

    # Load data
    #df = pd.read_csv("/Users/joaohenriques/Desktop/Mestrados/Data Science Nova IMS/My docs/Data Mining/Project/DM_Project/Web Application/data/df_profiling_final.csv")
    #df_real_values = pd.read_csv("/Users/joaohenriques/Desktop/Mestrados/Data Science Nova IMS/My docs/Data Mining/Project/DM_Project/Web Application/data/df_profiling_final_real_values.csv")

    df = pd.read_csv("data/df_profiling_final.csv")
    df_real_values = pd.read_csv("data/df_profiling_final_real_values.csv")



    # Features used in this perspective
    perspective_1_features = [
        'tot_money_spent_per_client', 'avg_money_spent_per_order',
        'avg_products_per_order', 'tot_non_chain_orders',
        'percent_chain_orders', 'num_unique_cuisines_tried',
        'value_preference_perspective'
    ]

    st.header("Features used for clustering")

    st.markdown(
        """
        <div style="background-color:#f9f9f9; 
                    padding:20px; 
                    border-radius:10px; 
                    font-size:18px; 
                    font-weight:normal; 
                    color:#333;">
            <p>The following features were used to create the clusters:</p>
            <ul>
        """ +
        "".join([f"<li>{feature.replace('_', ' ').title()}</li>" for feature in perspective_1_features[:-1]]) +
        """
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Filter data - now placed directly on the page
    st.header("Filter Data")
    st.write("""
    This section allows you to filter the dataset based on specific criteria for the numerical features used in this perspective. 
    You can apply filters to narrow down the data to focus on clients meeting certain conditions, such as spending below 
    a specific quartile threshold.
    """)
    filter_criteria = {}

    for feature in perspective_1_features[:-1]:  # Exclude the cluster label column
        q1, q2, q3 = df_real_values[feature].quantile([0.25, 0.5, 0.75])

        options = [
            "No Filtering Selected",
            f"Smaller than {q1:.2f} (Q1)",
            f"Smaller than {q2:.2f} (Q2)",
            f"Smaller than {q3:.2f} (Q3)",
        ]

        filter_criteria[feature] = st.selectbox(
            f"Select filter for {feature.replace('_', ' ').title()}",
            options
        )

    # Apply filtering logic
    filtered_df = df_real_values.copy()
    for feature, selected_option in filter_criteria.items():
        if "Smaller than" in selected_option:
            upper = float(selected_option.split("Smaller than ")[1].split(" ")[0])
            filtered_df = filtered_df[filtered_df[feature] <= upper]

    # Display total number of clients after filtering
    st.markdown(
        f"""
        <div style="background-color:#f9f9f9; 
                    padding:20px; 
                    border-radius:10px; 
                    text-align:center; 
                    font-size:24px; 
                    font-weight:bold; 
                    color:#333;">
            Total Number of Clients: {len(filtered_df)}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Cluster profiling
    st.header("Cluster Profiling")
    st.write("""
    This section presents a parallel coordinates plot and a bar chart to analyze the numerical features used in this perspective.

    The parallel coordinates plot represents the average value for each feature in each cluster, using the transformed 
    and scaled values. It is helpful to identify which cluster has a higher or lower average for specific features. 
    However, keep in mind that these are not the real values, as they have been scaled for clustering purposes.

    The bar chart complements this analysis by showing the distribution of clients across the clusters, providing a clearer 
    understanding of the relative sizes of the clusters.
    """)

    #st.write("**Cluster Distribution and Cluster Means**:")
    st.write("**Legend**: Blue: Cluster 0, Orange: Cluster 1, Green: Cluster 2")

    #cluster_profiles(df[perspective_1_features],label_columns=["value_preference_perspective"],figsize=(15, 10))

    # Generate interactive plots
    fig_parallel, fig_bar = cluster_profiles_interactive(df[perspective_1_features], "value_preference_perspective")

