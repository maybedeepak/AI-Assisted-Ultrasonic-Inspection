import pandas as pd


def load_csv(filename):
    """
    Load an ultrasonic A-Scan CSV file.

    Required columns:
        Time
        Amplitude
    """

    data = pd.read_csv(filename)

    required = ["Time", "Amplitude"]

    for column in required:
        if column not in data.columns:
            raise ValueError(
                f"Missing required column: {column}"
            )

    return data