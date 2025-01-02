import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

def plot_cluster_distributions(data, cluster_column):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x=cluster_column, data=data, ax=ax)
    st.pyplot(fig)

def plot_cluster_averages(data, cluster_column):
    fig, ax = plt.subplots(figsize=(12, 8))
    data.groupby(cluster_column).mean().plot(kind="bar", ax=ax)
    st.pyplot(fig)

def plot_numerical_profile(data, cluster_column):
    fig, ax = plt.subplots(figsize=(12, 8))
    data.groupby(cluster_column).mean().plot(kind="line", ax=ax)
    st.pyplot(fig)

def plot_categorical_profile(data, cluster_column, feature):
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    sns.countplot(x=feature, hue=cluster_column, data=data, ax=axes[0])
    data.groupby(cluster_column)[feature].value_counts(normalize=True).unstack().plot(kind="bar", stacked=True, ax=axes[1])
    st.pyplot(fig)



# main 
def cluster_profiles_interactive(df, cluster_column="value_preference_perspective"):
    # Calculate cluster means
    cluster_means = df.groupby(cluster_column).mean().reset_index()

    # Define discrete color mapping
    cluster_colors = {0: "blue", 1: "orange", 2: "green"}

    # Dropdown within the component
    st.subheader("Select Cluster to Highlight")
    cluster_options = [None] + list(cluster_colors.keys())  # Include "None" option
    selected_cluster = st.selectbox(
        "Cluster", cluster_options, format_func=lambda x: f"Cluster {x}" if x is not None else "None", key="select_cluster"
    )

    # Bar Chart for Cluster Sizes
    cluster_counts = df[cluster_column].value_counts().reset_index()
    cluster_counts.columns = ["Cluster", "Count"]

    # Apply highlighting logic
    def get_color_map(selected_cluster, color_mapping, values):
        if selected_cluster is None:
            return [color_mapping[v] for v in values]  # Default colors
        return [color_mapping[v] if v == selected_cluster else "lightgrey" for v in values]

    # Prepare color maps for both plots
    parallel_colors = get_color_map(selected_cluster, cluster_colors, cluster_means[cluster_column])
    bar_colors = get_color_map(selected_cluster, cluster_colors, cluster_counts["Cluster"])

    # Parallel Coordinates Plot for Cluster Means
    if selected_cluster is None:
        fig_parallel = px.parallel_coordinates(
            cluster_means,
            dimensions=df.columns[:-1],  # Feature columns
            color=cluster_means[cluster_column],
            color_continuous_scale=["blue", "orange", "green"],
            title="Cluster Means"
        )
    else:
        fig_parallel = px.parallel_coordinates(
            cluster_means,
            dimensions=df.columns[:-1],
            color=cluster_means[cluster_column].map(lambda x: selected_cluster if x == selected_cluster else -1),
            color_continuous_scale=["lightgrey", cluster_colors[selected_cluster]],
            title="Cluster Means"
        )

    # Adjust y-axis tick values
    global_y_min = min(fig_parallel.data[0].dimensions[0]["values"])
    global_y_max = max(fig_parallel.data[0].dimensions[0]["values"])
    for i, dim in enumerate(fig_parallel.data[0].dimensions):
        if i == 0:  # First axis: keep tick values
            dim["tickvals"] = [global_y_min, (global_y_min + global_y_max) / 2, global_y_max]
            dim["ticktext"] = [f"{global_y_min:.2f}", f"{(global_y_min + global_y_max) / 2:.2f}", f"{global_y_max:.2f}"]
        else:  # Remove ticks for all other axes
            dim["tickvals"] = []

    fig_parallel.update_layout(
        margin=dict(l=150, r=50, t=80, b=50),
        title=dict(y=0.95, x=0, xanchor="left", yanchor="top"),
        coloraxis_showscale=False,
        font=dict(size=12, color="black")
    )

    # Update Bar Chart for Cluster Sizes
    fig_bar = px.bar(
        cluster_counts,
        x="Cluster",
        y="Count",
        text="Count",
        title="Cluster Distribution"
    )
    fig_bar.update_traces(
        marker_color=bar_colors,
        textposition="outside"
    )
    fig_bar.update_layout(
        xaxis=dict(title="Cluster", tickfont=dict(size=12, color="black")),
        yaxis=dict(title="Number of Clients", tickfont=dict(size=12, color="black")),
        showlegend=False,
        margin=dict(l=50, r=50, t=30, b=50)
    )

    # Display plots in Streamlit
    st.plotly_chart(fig_parallel, use_container_width=True, key="parallel_chart")
    st.plotly_chart(fig_bar, use_container_width=True, key="bar_chart")

    return fig_parallel, fig_bar








def cluster_profiles_interactive_merged(df, cluster_column="value_preference_perspective"):
    # Calculate cluster means
    cluster_means = df.groupby(cluster_column).mean().reset_index()

    # Define discrete color mapping
    cluster_colors = {0: "blue", 1: "orange", 2: "green"}

    # Dropdown within the component
    st.subheader("Select Cluster to Highlight")
    cluster_options = [None] + list(cluster_colors.keys())  # Include "None" option
    selected_cluster = st.selectbox(
        "Cluster", cluster_options, format_func=lambda x: f"Cluster {x}" if x is not None else "None", key="select_cluster"
    )

    # Bar Chart for Cluster Sizes
    cluster_counts = df[cluster_column].value_counts().reset_index()
    cluster_counts.columns = ["Cluster", "Count"]

    # Apply highlighting logic
    def get_color_map(selected_cluster, color_mapping, values):
        if selected_cluster is None:
            return [color_mapping[v] for v in values]  # Default colors
        return [color_mapping[v] if v == selected_cluster else "lightgrey" for v in values]

    # Prepare color maps for both plots
    parallel_colors = get_color_map(selected_cluster, cluster_colors, cluster_means[cluster_column])
    bar_colors = get_color_map(selected_cluster, cluster_colors, cluster_counts["Cluster"])  # Define bar_colors

    # Abbreviate column names
    abbreviation_map = {
        'tot_money_spent_per_client': 'TMP',
        'avg_money_spent_per_order': 'AMS',
        'avg_products_per_order': 'APO',
        'tot_non_chain_orders': 'NCO',
        'percent_chain_orders': '%_CH',
        'num_unique_cuisines_tried': 'UC_tried',
        'peak_days_num_orders': 'PD_orders',
        'off_peak_days_num_orders': 'OPD_orders',
        'morning_num_orders': 'M_orders',
        'afternoon_num_orders': 'A_orders',
        'evening_num_orders': 'E_orders',
        'night_num_orders': 'N_orders'
    }
    abbreviated_dimensions = [abbreviation_map.get(col, col) for col in df.columns[:-1]]

    # Parallel Coordinates Plot for Cluster Means
    if selected_cluster is None:
        fig_parallel = px.parallel_coordinates(
            cluster_means,
            dimensions=df.columns[:-1],  # Feature columns
            labels={col: abbreviation_map.get(col, col) for col in df.columns[:-1]},
            color=cluster_means[cluster_column],
            color_continuous_scale=["blue", "orange", "green"],
            title="Cluster Means"
        )
    else:
        fig_parallel = px.parallel_coordinates(
            cluster_means,
            dimensions=df.columns[:-1],
            labels={col: abbreviation_map.get(col, col) for col in df.columns[:-1]},
            color=cluster_means[cluster_column].map(lambda x: selected_cluster if x == selected_cluster else -1),
            color_continuous_scale=["lightgrey", cluster_colors[selected_cluster]],
            title="Cluster Means"
        )

    # Adjust y-axis tick values
    global_y_min = min(fig_parallel.data[0].dimensions[0]["values"])
    global_y_max = max(fig_parallel.data[0].dimensions[0]["values"])
    for i, dim in enumerate(fig_parallel.data[0].dimensions):
        if i == 0:  # First axis: keep tick values
            dim["tickvals"] = [global_y_min, (global_y_min + global_y_max) / 2, global_y_max]
            dim["ticktext"] = [f"{global_y_min:.2f}", f"{(global_y_min + global_y_max) / 2:.2f}", f"{global_y_max:.2f}"]
        else:  # Remove ticks for all other axes
            dim["tickvals"] = []

    # Increase plot width
    fig_parallel.update_layout(
        width=1500,  # Adjust width to stretch the plot
        margin=dict(l=30, r=30, t=80, b=50),
        title=dict(y=0.95, x=0, xanchor="left", yanchor="top"),
        coloraxis_showscale=False,
        font=dict(size=12, color="black")
    )

    # Update Bar Chart for Cluster Sizes
    fig_bar = px.bar(
        cluster_counts,
        x="Cluster",
        y="Count",
        text="Count",
        title="Cluster Distribution"
    )
    fig_bar.update_traces(
        marker_color=bar_colors,  # Reference bar_colors here
        textposition="outside"
    )
    fig_bar.update_layout(
        xaxis=dict(title="Cluster", tickfont=dict(size=12, color="black")),
        yaxis=dict(title="Number of Clients", tickfont=dict(size=12, color="black")),
        showlegend=False,
        margin=dict(l=50, r=50, t=30, b=50)
    )

    # Display plots in Streamlit
    st.plotly_chart(fig_parallel, use_container_width=False, key="parallel_chart")  # Disable container width to honor explicit width
    st.plotly_chart(fig_bar, use_container_width=True, key="bar_chart")

    return fig_parallel, fig_bar
