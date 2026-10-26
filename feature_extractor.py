from core.signal_processing import detect_peaks


def extract_features(data, metadata=None, label=0):

    peaks = detect_peaks(data)

    signal = data["Amplitude"].values

    # Statistical features
    max_amp = float(signal.max())
    mean_amp = float(signal.mean())
    std_amp = float(signal.std())

    velocity = 5900
    thickness = 0

    if metadata is not None:
        velocity = metadata.get("Velocity_m_per_s", velocity)
        thickness = metadata.get("Thickness_mm", 0)

    defects = []

    # First reflector
    if len(peaks) > 0:

        first_peak = peaks[0]

        defect_time = float(data["Time"].iloc[first_peak])
        defect_amp = float(signal[first_peak])

    else:

        defect_time = 0.0
        defect_amp = 0.0

    # Defect list (exclude backwall)
    for peak in peaks[:-1]:

        time = float(data["Time"].iloc[peak])

        depth = (time * velocity * 1000) / 2

        defects.append({

            "time": time,
            "amplitude": float(signal[peak]),
            "depth_mm": round(depth, 2)

        })

    # Backwall
    if len(peaks) > 0:

        last_peak = peaks[-1]

        backwall_time = float(data["Time"].iloc[last_peak])

        backwall_amp = float(signal[last_peak])

        measured_thickness = (
            backwall_time * velocity * 1000
        ) / 2

    else:

        backwall_time = 0.0
        backwall_amp = 0.0
        measured_thickness = 0.0

    return {

        "Peak_Count": len(peaks),

        "Defect_Time": defect_time,
        "Defect_Amplitude": defect_amp,

        "Backwall_Time": backwall_time,
        "Backwall_Amplitude": backwall_amp,
        "Backwall_Depth_mm": round(measured_thickness, 2),

        "Max_Amplitude": max_amp,
        "Mean_Amplitude": mean_amp,
        "Std_Amplitude": std_amp,

        "Velocity": velocity,
        "Thickness": thickness,

        "Defects": defects,

        "Label": label
    }