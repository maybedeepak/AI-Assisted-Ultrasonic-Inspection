from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar
)

from PySide6.QtCore import Qt


class SummaryPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Inspection Summary")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            color:#003366;
        """)

        self.result = QLabel("Status : Waiting for Inspection")
        self.result.setStyleSheet("""
            font-size:14px;
            font-weight:bold;
        """)

        self.confidence = QLabel("Confidence : -- %")

        self.confidence_bar = QProgressBar()
        self.confidence_bar.setRange(0, 100)
        self.confidence_bar.setValue(0)
        self.confidence_bar.setTextVisible(True)
        self.confidence_bar.setFormat("%p%")
        self.confidence_bar.setFixedHeight(20)

        self.reflectors = QLabel("Reflectors : --")
        self.thickness = QLabel("Estimated Thickness : -- mm")

        for widget in [
            title,
            self.result,
            self.confidence,
            self.confidence_bar,
            self.reflectors,
            self.thickness
        ]:
            layout.addWidget(widget)

        layout.addStretch()

        self.setLayout(layout)

    def update_summary(
        self,
        result,
        confidence,
        reflector_count,
        thickness
    ):

        self.result.setText(
            f"Result : {result}"
        )

        # Color the result text
        if "DEFECT" in result:
            self.result.setStyleSheet("""
                font-size:14px;
                font-weight:bold;
                color:#C62828;
            """)
        else:
            self.result.setStyleSheet("""
                font-size:14px;
                font-weight:bold;
                color:#2E7D32;
            """)

        self.confidence.setText(
            f"Confidence : {confidence:.1f}%"
        )

        self.confidence_bar.setValue(
            int(confidence)
        )

        # Progress bar color
        if confidence >= 80:
            color = "#2E7D32"      # Green
        elif confidence >= 60:
            color = "#F9A825"      # Yellow
        else:
            color = "#C62828"      # Red

        self.confidence_bar.setStyleSheet(f"""
        QProgressBar {{
            border:1px solid gray;
            border-radius:6px;
            text-align:center;
        }}

        QProgressBar::chunk {{
            background-color:{color};
            border-radius:6px;
        }}
        """)

        self.reflectors.setText(
            f"Reflectors : {reflector_count}"
        )

        self.thickness.setText(
            f"Estimated Thickness : {thickness:.2f} mm"
        )

    def reset(self):

        self.result.setText(
            "Status : Waiting for Inspection"
        )

        self.result.setStyleSheet("""
            font-size:14px;
            font-weight:bold;
            color:black;
        """)

        self.confidence.setText(
            "Confidence : -- %"
        )

        self.confidence_bar.setValue(0)

        self.reflectors.setText(
            "Reflectors : --"
        )

        self.thickness.setText(
            "Estimated Thickness : -- mm"
        )