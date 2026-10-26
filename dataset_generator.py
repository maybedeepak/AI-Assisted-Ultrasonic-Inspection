import pandas as pd

from core.signal_generator import generate_signal
from core.feature_extractor import extract_features


dataset = []

NUMBER_OF_SAMPLES = 5000

for i in range(NUMBER_OF_SAMPLES):

    # 50% Defect
    if i % 2 == 0:

        signal = generate_signal(defect=True)

        features = extract_features(signal, label=1)

    # 50% No Defect
    else:

        signal = generate_signal(defect=False)

        features = extract_features(signal, label=0)

    dataset.append(features)


df = pd.DataFrame(dataset)

df.to_csv(
    "ai/training_dataset.csv",
    index=False
)

print("Dataset Created Successfully!")

print(df.head())