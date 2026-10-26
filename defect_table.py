from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtWidgets import QHeaderView


class DefectTable(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Detected Reflectors")
        title.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
        """)

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "No",
            "Depth (mm)",
            "Time (µs)",
            "Amplitude"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.verticalHeader().setVisible(False)

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionMode(
            QTableWidget.NoSelection
        )

        layout.addWidget(title)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def update_table(self, defects):

        self.table.setRowCount(len(defects))

        for row, defect in enumerate(defects):

            self.table.setItem(
                row, 0,
                QTableWidgetItem(str(row + 1))
            )

            self.table.setItem(
                row, 1,
                QTableWidgetItem(f"{defect['depth_mm']:.2f}")
            )

            self.table.setItem(
                row, 2,
                QTableWidgetItem(f"{defect['time']*1e6:.2f}")
            )

            self.table.setItem(
                row, 3,
                QTableWidgetItem(f"{defect['amplitude']:.2f}")
            )

    def clear(self):

        self.table.setRowCount(0)