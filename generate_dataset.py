import pandas as pd

from core.signal_generator import generate_signal
from core.feature_extractor import extract_features


ROWS = 5000

dataset = []

for i in range(ROWS):

    data, metadata = generate_signal()

    label = 1 if metadata["Defect_Count"] > 0 else 0

    features = extract_features(
        data,
        metadata,
        label
    )

    amplitudes = data["Amplitude"]

    dataset.append({

        "Peak_Count":
            features["Peak_Count"],

        "Max_Amplitude":
            amplitudes.max(),

        "Mean_Amplitude":
            amplitudes.mean(),

        "Std_Amplitude":
            amplitudes.std(),

        "Backwall_Amplitude":
            features["Backwall_Amplitude"],

        "Thickness":
            features["Backwall_Depth_mm"],

        "Label":
            label

    })

df = pd.DataFrame(dataset)

df.to_csv(
    "datasets/ut_dataset.csv",
    index=False
)

print(df.head())

print()

print("Dataset Created Successfully")

print(f"Samples : {len(df)}")