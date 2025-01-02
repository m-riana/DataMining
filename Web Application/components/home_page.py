import streamlit as st

def home_page_component():
    """
    Home Page Component
    """
    st.title("Home Page")

    # Overview of the project
    st.header("Overview of the Project")
    st.write(
    """
    Considering the ever-increasing competitiveness in the food delivery business, our team was hired by ABCDEats Inc. 
    to analyze their customer-collected data and develop a data-driven marketing strategy. The goal was to analyze customer 
    data, segment clients into meaningful groups using ML clustering algorithms, and provide actionable insights to enhance 
    targeted marketing campaigns and service personalization.

    To achieve this, a dataset of 31,888 clients, collected over three months from three cities, was extensively analyzed. 
    Based on the company's marketing requirements, two distinct segmentation perspectives were defined: 
    **Value and Preference** and **Activity and Engagement**. After applying data preprocessing and feature engineering 
    techniques, clustering algorithms were used to create initial segmentations for each perspective. 
    The K-means algorithm, with three clusters for each perspective, proved to be the most effective. Following the segmentation, a final merged solution was obtained with three final clusters.

    This web application consolidates our findings and provides ABCDEats with a user-friendly interface to explore the 
    segmentation insights. It allows for:
    - **Cluster Profiling**: To analyze customer segments based on their behavior and preferences.
    - **Prediction Module**: To classify new clients into clusters, enabling data-driven onboarding strategies.

    The application allows the company's marketing team to make informed decisions, improve customer satisfaction, 
    and overall business efficiency.
    """
    )

    # Components of the Web Application
    st.header("Components of the Web Application")

    st.subheader("1. Value and Preference Perspective")
    st.write(
        """
        In this section, users will explore features related to customer value and preference 
        that were used for clustering. Users can filter the dataset based on specific criteria 
        and view the cluster profiling through interactive visualizations. These include a parallel 
        coordinates plot showing the average value of each feature per cluster and a bar chart 
        displaying the distribution of clients across clusters.
        """
    )

    st.subheader("2. Activity and Engagement Perspective")
    st.write(
        """
        This section focuses on customer activity and engagement features used in clustering. 
        Users can apply filters to customize the dataset and analyze the cluster profiling through 
        interactive visualizations. The visualizations include a parallel coordinates plot representing 
        the average feature values for each cluster and a bar chart that illustrates the distribution 
        of clients within the clusters.
        """
    )

    st.subheader("3. Merged Solution")
    st.write(
        """
        This section allows the user to analyze the final clustering solution after merging 
        the perspectives. Users will see two main profiling sections:

        - **Profiling for Numerical Features used in Clustering**: This includes a parallel 
          coordinates plot of average feature values for each cluster and a bar chart showing 
          the number of clients per cluster.
        - **Profiling for Categorical Features**: Users can select categorical features to 
          view a count distribution bar plot and a stacked bar plot showing the percentage 
          composition of clusters for each categorical feature.
        """
    )


    st.subheader("4. Prediction")
    st.write(
        """
        In this section, users can input specific values for the features used in clustering 
        and receive a prediction for the cluster to which a new client belongs. This tool uses 
        a semi-supervised decision tree model trained on the final merged dataset. Users will input 
        feature values and click a button to get the predicted cluster, enabling practical applications 
        of the clustering results.
        """
    )

    # Group Members
    st.header("Group Members")
    st.write(
        """
        - João Henriques, 20240499 
        - Julia Karpienia, 20240514 
        - Maria Radix, 20240687 
        - Mariana Sousa, 20240516 
        """
    )
