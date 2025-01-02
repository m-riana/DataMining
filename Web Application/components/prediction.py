import streamlit as st
import numpy as np
from joblib import load

# Load the trained model
model = load("models/decision_tree_model.pkl")

# Define the required features
required_features = [
    'tot_money_spent_per_client',
    'avg_money_spent_per_order',
    'avg_products_per_order',
    'tot_non_chain_orders',
    'percent_chain_orders',
    'num_unique_cuisines_tried',
    'peak_days_num_orders',
    'off_peak_days_num_orders',
    'morning_num_orders',
    'afternoon_num_orders',
    'evening_num_orders',
    'night_num_orders'
]

# Prediction Component
def prediction_component():
    st.title("Cluster Prediction")
    st.write("""
    This section allows you to predict the cluster for a new client. 
    We used a Semi-Supervised Learning approach with a Decision Tree model, trained on the final dataset with 
    the merged cluster labels. By providing the required inputs, you can determine the cluster that best fits 
    the new client's profile.
    """)

    # Collect user inputs
    st.write("Please provide the following information to predict to which cluster the new client belongs to:")
    user_inputs = {}

    for feature in required_features:
        user_inputs[feature] = st.number_input(
            f"Enter value for {feature}:",
            value=0.0,  # Default value
            format="%.2f"
        )
    
    # Convert inputs to a numpy array for prediction
    input_values = np.array([user_inputs[feature] for feature in required_features]).reshape(1, -1)

    # Make a prediction when the user clicks the button
    if st.button("Predict Cluster"):
        prediction = model.predict(input_values)
        st.success(f"The predicted cluster is: **Cluster {prediction[0]}**")
