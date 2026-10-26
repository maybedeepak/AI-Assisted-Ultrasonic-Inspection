import random
import numpy as np
import pandas as pd


# Ultrasonic longitudinal wave velocities (m/s)
VELOCITIES = {
    "Mild Steel": 5900,
    "Stainless Steel": 5790,
    "Aluminium": 6320,
}


def generate_signal(material="Mild Steel", thickness=None):

    velocity = VELOCITIES.get(material, 5900)

    if thickness is None:
        thickness = round(random.uniform(10, 50), 1)

    time = np.linspace(0, 25e-6, 2500)

    signal = np.random.normal(0, 0.015, len(time))

    defects = []

    defect_count = random.randint(0, 3)

    # ----------------------------
    # Generate defects
    # ----------------------------

    for _ in range(defect_count):

        depth = round(random.uniform(2, thickness - 2), 2)

        amplitude = round(random.uniform(0.45, 0.85), 2)

        defect_time = (2 * (depth / 1000)) / velocity

        signal += amplitude * np.exp(
            -((time - defect_time) ** 2)
            / (2 * (0.12e-6) ** 2)
        )

        defects.append({
            "depth_mm": depth,
            "time": defect_time,
            "amplitude": amplitude
        })

    # ----------------------------
    # Backwall echo
    # ----------------------------

    backwall_time = (2 * (thickness / 1000)) / velocity

    signal += 0.95 * np.exp(
        -((time - backwall_time) ** 2)
        / (2 * (0.12e-6) ** 2)
    )

    data = pd.DataFrame({
        "Time": time,
        "Amplitude": signal
    })

    metadata = {
        "Material": material,
        "Velocity_m_per_s": velocity,
        "Thickness_mm": thickness,
        "Defect_Count": defect_count,
        "Defects": defects,
        "Backwall_Depth_mm": thickness
    }

    return data, metadata