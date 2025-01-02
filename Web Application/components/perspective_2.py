import streamlit as st
import pandas as pd
import plotly.express as px
from utils.plot_helpers import cluster_profiles_interactive

def perspective_2_component():
    """
    Component for Activity and Engagement Perspective (Perspective 2).
    """
    st.title("Activity and Engagement Perspective")
    st.write("""
    The Activity and Engagement Perspective focuses on analyzing the frequency and timing of client orders, 
    providing insights into customer engagement patterns. This perspective helps to identify active periods, 
    client behavior across different times of the day, and overall activity levels, enabling better resource 
    allocation and targeted engagement strategies.
    """)


    # Load data
    df = pd.read_csv("data/df_profiling_final.csv")
    df_real_values = pd.read_csv("data/df_profiling_final_real_values.csv")

    # Features used in this perspective
    perspective_2_features = [
        'peak_days_num_orders', 'off_peak_days_num_orders',
        'morning_num_orders', 'afternoon_num_orders', 'evening_num_orders',
        'night_num_orders', 'activity_engagement_perspective'
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
        "".join([f"<li>{feature.replace('_', ' ').title()}</li>" for feature in perspective_2_features[:-1]]) +
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
    By applying these filters, you can explore subsets of clients based on their activity levels, such as those with orders 
    during peak or off-peak hours. Filtering provides a more focused view of engagement patterns within specific client segments.
    """)

    filter_criteria = {}

    for feature in perspective_2_features[:-1]:  # Exclude the cluster label column
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
    This section presents a parallel coordinates plot and a bar chart to analyze the numerical features used in clustering.

    The parallel coordinates plot represents the average value for each feature in each cluster, using the transformed 
    and scaled values. It is helpful to identify which cluster has higher or lower engagement levels for specific features. 
    However, keep in mind that these are not the real values, as they have been scaled for clustering purposes.

    The bar chart complements this analysis by showing the distribution of clients across the clusters, providing a clearer 
    understanding of the relative sizes of the clusters.
    """)
    #st.write("**Cluster Distribution and Cluster Means**:")
    st.write("**Legend**: Blue: Cluster 0, Orange: Cluster 1, Green: Cluster 2")

    # Generate interactive plots
    fig_parallel, fig_bar = cluster_profiles_interactive(df[perspective_2_features], "activity_engagement_perspective")

    # Display interactive plots
    #st.plotly_chart(fig_parallel, use_container_width=True)
    #st.plotly_chart(fig_bar, use_container_width=True)
