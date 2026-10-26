from PySide6.QtWidgets import QWidget, QVBoxLayout

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class GraphPanel(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout(self)

        self.figure = Figure(figsize=(9, 4))

        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)

        self.figure.tight_layout(rect=[0, 0, 1, 0.95])

    def plot(self, data, features=None):

        self.ax.clear()

        time_us = data["Time"] * 1e6

        amp = data["Amplitude"]

        # --------------------------
        # A-Scan
        # --------------------------

        self.ax.plot(
             time_us,
             amp,
             color="#0066CC",
             linewidth=2.5,
             label="A-Scan Signal"
        )

        # --------------------------
        # Defect markers
        # --------------------------

        if features:

            defects = features.get("Defects", [])

            for i, defect in enumerate(defects):

                x = defect["time"] * 1e6
                y = defect["amplitude"]

                self.ax.scatter(
                     x,
                     y,
                     color="#D32F2F",
                     s=90,
                     edgecolors="black",
                     linewidths=0.8,
                     zorder=5,
                     label="Defect" if i == 0 else ""
                )

                self.ax.annotate(
                    f"D{i+1}\n{defect['depth_mm']:.1f} mm",
                    (x, y),
                    xytext=(0, 18),
                    textcoords="offset points",
                    ha="center",
                    fontsize=9,
                    color="red",
                    weight="bold"
                )

            # --------------------------
            # Backwall
            # --------------------------

            bw_time = features["Backwall_Time"] * 1e6
            bw_amp = features["Backwall_Amplitude"]

            self.ax.scatter(
                 bw_time,
                 bw_amp,
                 color="#2E7D32",
                 s=120,
                 edgecolors="black",
                 linewidths=1,
                 zorder=6,
                 label="Backwall Echo"
            )

            self.ax.annotate(
                "Backwall",
                (bw_time, bw_amp),
                xytext=(0, 20),
                textcoords="offset points",
                ha="center",
                fontsize=10,
                color="green",
                weight="bold"
            )

        # --------------------------
        # Styling
        # --------------------------

        self.ax.set_title(
             "AI-Assisted Ultrasonic A-Scan Inspection",
             fontsize=15,
             fontweight="bold",
             color="#003366",
             pad=15
        )

        self.ax.set_xlabel(
             "Time (µs)",
             fontsize=11,
             fontweight="bold"
        )

        self.ax.set_ylabel(
             "Normalized Amplitude",
             fontsize=11,
             fontweight="bold"
        )

        self.ax.grid(
             True,
             linestyle="--",
             linewidth=0.7,
             alpha=0.5
             )

        self.ax.set_ylim(-0.08, 1.05)
        self.ax.margins(x=0.02)

        self.ax.legend(
             loc="upper right",
             fontsize=9,
             frameon=True
        )

        self.canvas.draw()