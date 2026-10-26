from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
    QMessageBox,
    QStatusBar,
)

from ui.control_panel import ControlPanel
from ui.graph_panel import GraphPanel
from ui.summary_panel import SummaryPanel
from ui.defect_table import DefectTable

from core.signal_generator import generate_signal
from core.data_loader import load_csv
from core.inspection_controller import InspectionController

from report_generator import create_report


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "AI-Assisted Ultrasonic Inspection System"
        )

        self.resize(1450, 850)

        self.session = {
            "data": None,
            "metadata": None,
            "features": None,
            "prediction": None,
            "confidence": None,
        }
        self.controller = InspectionController()
        self.setup_ui()

    # -------------------------------------------------------
    # Build User Interface
    # -------------------------------------------------------

    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # ------------------------------------------
        # Left Panel
        # ------------------------------------------

        self.control_panel = ControlPanel()

        main_layout.addWidget(
            self.control_panel,
            1
        )

        # ------------------------------------------
        # Right Panel
        # ------------------------------------------

        right_layout = QVBoxLayout()

        self.graph_panel = GraphPanel()

        right_layout.addWidget(
            self.graph_panel,
            3
        )

        bottom_layout = QHBoxLayout()

        self.summary_panel = SummaryPanel()

        self.defect_table = DefectTable()

        bottom_layout.addWidget(
            self.summary_panel,
            1
        )

        bottom_layout.addWidget(
            self.defect_table,
            2
        )

        right_layout.addLayout(
            bottom_layout,
            2
        )

        main_layout.addLayout(
            right_layout,
            4
        )

        # ------------------------------------------
        # Status Bar
        # ------------------------------------------

        self.status = QStatusBar()

        self.setStatusBar(
            self.status
        )

        self.status.showMessage(
            "Ready"
        )

        # ------------------------------------------
        # Button Connections
        # ------------------------------------------

        self.control_panel.generate_btn.clicked.connect(
            self.generate_signal
        )

        self.control_panel.upload_btn.clicked.connect(
            self.upload_csv
        )

        self.control_panel.analyze_btn.clicked.connect(
            self.analyze_signal
        )

        self.control_panel.export_btn.clicked.connect(
            self.export_report
        )

    # -------------------------------------------------------
    # Generate Inspection Simulation
    # -------------------------------------------------------

    def generate_signal(self):

        try:

            material = self.control_panel.material_box.currentText()

            thickness = self.control_panel.thickness_box.value()

            data, metadata = generate_signal(
             material=material,
             thickness=thickness
          )

            self.session["data"] = data
            self.session["metadata"] = metadata

            self.graph_panel.plot(data, None)

            self.summary_panel.reset()

            self.defect_table.clear()

            self.status.showMessage(
                "Inspection simulation generated successfully."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Simulation Error",
                str(e)
            )

    # -------------------------------------------------------
    # Upload CSV
    # -------------------------------------------------------

    def upload_csv(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV",
            "",
            "CSV Files (*.csv)"
        )

        if not filename:
            return

        try:

            data = load_csv(filename)

            self.session["data"] = data
            self.session["metadata"] = None

            self.graph_panel.plot(data, None)

            self.summary_panel.reset()

            self.defect_table.clear()

            self.status.showMessage(
                "CSV loaded successfully."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "CSV Error",
                str(e)
            )
    # -------------------------------------------------------
    # Analyze Inspection
    # -------------------------------------------------------

    def analyze_signal(self):

        if self.session["data"] is None:

            QMessageBox.warning(
                self,
                "No Data",
                "Generate a signal or upload a CSV first."
            )

            return

        try:

            inspection = self.controller.analyze(
                 self.session["data"],
                 self.session["metadata"]
            )

            features = inspection["features"]
            prediction = inspection["prediction"]
            confidence = inspection["confidence"]

            self.session["features"] = features
            self.session["prediction"] = inspection["prediction"]
            self.session["confidence"] = inspection["confidence"]

            self.graph_panel.plot(
                 self.session["data"],
                 features
            )

            result = inspection["result"]
            reflector_count = inspection["reflector_count"]
            thickness = inspection["thickness"]

            self.summary_panel.update_summary(
                result=result,
                confidence=confidence,
                reflector_count=reflector_count,
                thickness=thickness
            )

            self.defect_table.update_table(
                features.get("Defects", [])
            )

            self.status.showMessage(
                "Inspection completed successfully."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Analysis Error",
                str(e)
            )

    # -------------------------------------------------------
    # Export PDF Report
    # -------------------------------------------------------

    def export_report(self):

        if self.session["data"] is None:

            QMessageBox.warning(
                self,
                "No Data",
                "Nothing to export."
            )

            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report",
            "inspection_report.pdf",
            "PDF Files (*.pdf)"
        )

        if not filename:
            return

        try:

            graph_path = "inspection_graph.png"

            self.graph_panel.figure.savefig(
                graph_path,
                dpi=150
            )

            result = (
                "DEFECT DETECTED"
                if self.session["prediction"] == 1
                else "NO DEFECT"
            )

            create_report(
                filename=filename,
                result=result,
                confidence=self.session["confidence"],
                features=self.session["features"],
                graph_path=graph_path
            )

            QMessageBox.information(
                self,
                "Report Created",
                "Inspection report exported successfully."
            )

            self.status.showMessage(
                "Report exported successfully."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Export Error",
                str(e)
            )