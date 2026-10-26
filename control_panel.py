from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QDoubleSpinBox,
)


class ControlPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # -------------------------
        # Title
        # -------------------------

        title = QLabel("AI Ultrasonic\nInspection System")
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)
        title.setWordWrap(True)

        layout.addWidget(title)

        # -------------------------
        # Material
        # -------------------------

        material_label = QLabel("Material")

        self.material_box = QComboBox()

        self.material_box.addItems([
            "Mild Steel",
            "Stainless Steel",
            "Aluminium"
        ])

        layout.addWidget(material_label)
        layout.addWidget(self.material_box)

        # -------------------------
        # Thickness
        # -------------------------

        thickness_label = QLabel("Thickness (mm)")

        self.thickness_box = QDoubleSpinBox()

        self.thickness_box.setRange(5, 300)

        self.thickness_box.setValue(25)

        self.thickness_box.setSuffix(" mm")

        layout.addWidget(thickness_label)
        layout.addWidget(self.thickness_box)

        # -------------------------
        # Buttons
        # -------------------------

        self.generate_btn = QPushButton("Generate Test Signal")

        self.analyze_btn = QPushButton("Analyze")

        self.upload_btn = QPushButton("Upload CSV")

        self.export_btn = QPushButton("Export Report")

        for button in [
            self.generate_btn,
            self.analyze_btn,
            self.upload_btn,
            self.export_btn
        ]:
            button.setMinimumHeight(45)
            layout.addWidget(button)

        layout.addStretch()

        self.setLayout(layout)