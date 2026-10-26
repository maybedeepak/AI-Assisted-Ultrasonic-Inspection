import os
import sys

import joblib
import pandas as pd


def resource_path(relative_path):
    """
    Returns the correct path whether running
    from Python or from a PyInstaller EXE.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Load trained AI model
model = joblib.load(
    resource_path("models/random_forest.pkl")
)


def predict(features):
    """
    Predict defect using the trained Random Forest model.
    """

    feature_vector = pd.DataFrame([{
        "Peak_Count": features["Peak_Count"],
        "Max_Amplitude": features["Max_Amplitude"],
        "Mean_Amplitude": features["Mean_Amplitude"],
        "Std_Amplitude": features["Std_Amplitude"],
        "Backwall_Amplitude": features["Backwall_Amplitude"],
        "Thickness": features["Backwall_Depth_mm"]
    }])

    prediction = model.predict(feature_vector)[0]

    confidence = (
        model.predict_proba(feature_vector).max() * 100
    )

    return int(prediction), float(confidence)