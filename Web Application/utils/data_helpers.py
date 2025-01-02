import pandas as pd

def load_data(filepath):
    return pd.read_csv(filepath)


def filter_data_by_quartile(data, filters):
    """
    Filters data based on quartile selections for each feature.

    Parameters:
    - data: DataFrame
    - filters: Dict containing feature names as keys and selected ranges as values

    Returns:
    - Filtered DataFrame
    """
    for feature, selected_range in filters.items():
        q1, q2, q3 = data[feature].quantile([0.25, 0.5, 0.75])
        min_val, max_val = data[feature].min(), data[feature].max()

        if "Between" in selected_range:
            if f"{min_val:.2f}" in selected_range:
                data = data[data[feature] <= q1]
            elif f"{q1:.2f}" in selected_range:
                data = data[(data[feature] > q1) & (data[feature] <= q2)]
            elif f"{q2:.2f}" in selected_range:
                data = data[(data[feature] > q2) & (data[feature] <= q3)]
            elif f"{q3:.2f}" in selected_range:
                data = data[data[feature] > q3]

    return data
