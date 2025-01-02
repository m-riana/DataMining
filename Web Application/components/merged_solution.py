import streamlit as st
import pandas as pd
from utils.plot_helpers import cluster_profiles_interactive_merged
import matplotlib.pyplot as plt

def cluster_composition_and_count_categorical(df, feature, label_column):
    """
    Plot bar charts showing both the absolute count and percentage composition of a categorical feature for each cluster.

    Parameters:
    - df: DataFrame containing categorical features and cluster labels.
    - feature: The categorical feature to analyze.
    - label_column: Column with cluster labels.
    """
    # Create subplots
    fig, axes = plt.subplots(1, 2, figsize=(16, 8), constrained_layout=True)

    # Absolute count
    cluster_counts = pd.crosstab(df[label_column], df[feature])
    cluster_counts.plot(kind="bar", stacked=False, cmap="tab10", ax=axes[0], legend=False)
    axes[0].set_title(f"Count Distribution by {feature} in Clusters")
    axes[0].set_xlabel("Cluster")
    axes[0].set_ylabel("Count")

    # Percentage composition
    cluster_comp = pd.crosstab(df[label_column], df[feature], normalize="index") * 100
    cluster_comp.plot(kind="bar", stacked=True, cmap="tab10", ax=axes[1], legend=False)
    axes[1].set_title(f"Cluster Composition by {feature}")
    axes[1].set_xlabel("Cluster")
    axes[1].set_ylabel("Percentage (%)")

    # Single legend for both plots
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        title=feature,
        loc="upper center",
        ncol=len(labels),
        bbox_to_anchor=(0.8, 1.15),  # Adjusted for position: slightly higher and to the right
    )

    # Stop x-axis rotation
    for ax in axes:
        ax.tick_params(axis="x", rotation=0)

    # Adjust layout and return the figure
    plt.suptitle(f"Analysis of {feature}", fontsize=16)
    return fig











def merged_solution_component():
    """
    Merged Solution Component
    """
    st.title("Merged Solution")

    # Introduction to the Merged Solution
    st.write("""
        After merging the two perspectives, we used a hierarchical clustering approach to perform 
        post-clustering refinement. This process reduced the initial nine clusters after merging 
        to three clusters in our final solution. These three clusters represent the merged view 
        of our dataset and form the basis for the analyses below.
    """)

    # Load data
    df = pd.read_csv("data/df_profiling_final.csv")
    df_real_values = pd.read_csv("data/df_profiling_final_real_values.csv")

    # Debug: Print the column names in the DataFrame
    print("Hello \n {df.columns}")

    # Section for Most Important Features
    st.header("Most Important Features")
    st.write("""
        To determine the most important features, we used a Semi-Supervised Learning technique 
        with a Decision Tree algorithm. The following features were identified as the most important 
        in determining cluster membership:
    """)
    st.markdown("""
    - **Off Peak Days Number of Orders**
    - **Night Number of Orders**
    - **Peak Days Number of Orders**
    - **Evening Number of Orders**
    - **Afternoon Number of Orders**
    """)

    # Features used in this perspective
    merged_perspective_features = [
        'tot_money_spent_per_client', 'avg_money_spent_per_order',
        'avg_products_per_order', 'tot_non_chain_orders',
        'percent_chain_orders', 'num_unique_cuisines_tried', 'peak_days_num_orders', 'off_peak_days_num_orders',
        'morning_num_orders', 'afternoon_num_orders', 'evening_num_orders',
        'night_num_orders', "merged_labels"
    ]

    # Cluster profiling for numerical features
    st.header("Profiling for Numerical Features used in Clustering")
    st.write("""
        This section presents a parallel coordinates plot and a bar chart to analyze the numerical features used in clustering. 

        The parallel coordinates plot represents the average value for each feature in each cluster, using the transformed 
        and scaled values. It is helpful to identify which cluster has a higher or lower average for specific features. 
        However, keep in mind that these are not the real values, as they have been scaled for clustering purposes.

        The bar chart complements this analysis by showing the distribution of clients across the clusters, providing a clearer 
        understanding of the relative sizes of the clusters.
    """)
    #st.write("**Cluster Distribution and Cluster Means**:")
    st.write("**Legend**: Blue: Cluster 0, Orange: Cluster 1, Green: Cluster 2")
    st.write(
        """
        **Feature Names Abbreviations**:
        - tot_money_spent_per_client: TMP
        - avg_money_spent_per_order: AMS
        - avg_products_per_order: APO
        - tot_non_chain_orders: NCO
        - percent_chain_orders: %_CH
        - num_unique_cuisines_tried: UC_tried
        - peak_days_num_orders: PD_orders
        - off_peak_days_num_orders: OPD_orders
        - morning_num_orders: M_orders
        - afternoon_num_orders: A_orders
        - evening_num_orders: E_orders
        - night_num_orders: N_orders
        """
    )

    # Generate interactive plots using the updated function
    fig_parallel, fig_bar = cluster_profiles_interactive_merged(df[merged_perspective_features], "merged_labels")

    # Display the plots
    # st.plotly_chart(fig_parallel, use_container_width=True, key="parallel_chart_merged_solution")
    # st.plotly_chart(fig_bar, use_container_width=True, key="bar_chart_merged_solution")

    # Profiling for Categorical Features
    st.header("Profiling for Categorical Features")
    st.write("""
        This section provides an analysis of categorical features across clusters. 
        Select a feature from the dropdown menu to view its count distribution and 
        percentage composition for each cluster. These visualizations reveal the categorical 
        preferences and trends within each cluster.
    """)

    categorical_features = [
        'last_promo',
        'payment_method_combined',
        'city',
        'purchased_American',
        'purchased_Asian',
        'purchased_Beverages',
        'purchased_Cafe',
        'purchased_Chicken Dishes',
        'purchased_Chinese',
        'purchased_Desserts',
        'purchased_Healthy',
        'purchased_Indian',
        'purchased_Italian',
        'purchased_Japanese',
        'purchased_Noodle Dishes',
        'purchased_OTHER',
        'purchased_Street Food / Snacks',
        'purchased_Thai',
        'client_behavior_cuisine_preference',
        'client_behavior_peak_preference',
        'client_behavior_chain_preference'
    ]
    print(df.columns)

    selected_feature = st.selectbox("Select a Categorical Feature", categorical_features)

    if selected_feature:
        st.subheader(f"Analysis of {selected_feature}")
        fig = cluster_composition_and_count_categorical(df_real_values, selected_feature, "merged_labels")
        st.pyplot(fig)
