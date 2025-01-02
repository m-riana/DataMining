import joblib
import pandas as pd

def predict_cluster(inputs):
    model = joblib.load("models/decision_tree_model.pkl")  # Load pre-trained model
    input_df = pd.DataFrame([inputs])
    return model.predict(input_df)[0]
  