from core.feature_extractor import extract_features
from core.predictor import predict


class InspectionController:
    """
    Handles the complete inspection pipeline.
    """

    def analyze(self, data, metadata):

        features = extract_features(
            data,
            metadata,
            label=0
        )

        prediction, confidence = predict(features)

        result = (
            "DEFECT DETECTED"
            if prediction == 1
            else "NO DEFECT"
        )

        return {
            "features": features,
            "prediction": prediction,
            "confidence": confidence,
            "result": result,
            "reflector_count": len(features.get("Defects", [])),
            "thickness": features.get("Backwall_Depth_mm", 0)
        }