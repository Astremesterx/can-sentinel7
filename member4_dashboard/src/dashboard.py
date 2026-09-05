import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
    QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor

class AlertListenerThread(QThread):
    new_alert = pyqtSignal(dict)

    def run(self):
        for line in sys.stdin:
            line = line.strip()
            if not line: continue
            try:
                data = json.loads(line)
                if data.get("alert_type") == "INTRUSION_DETECTED":
                    self.new_alert.emit(data)
            except json.JSONDecodeError:
                pass

class ECUWidget(QFrame):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border: 2px solid #333333;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        layout = QVBoxLayout(self)
        
        self.title = QLabel(name.upper())
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #aaaaaa; font-weight: bold; font-size: 14px; border: none;")
        
        self.status = QLabel("SECURE")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("color: #00e676; font-weight: bold; font-size: 18px; border: none;")
        
        layout.addWidget(self.title)
        layout.addWidget(self.status)

    def set_compromised(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #3b0000;
                border: 2px solid #ff1744;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.title.setStyleSheet("color: #ff5252; font-weight: bold; font-size: 14px; border: none;")
        self.status.setStyleSheet("color: #ff1744; font-weight: bold; font-size: 18px; border: none;")
        self.status.setText("COMPROMISED")

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAN-Sentinel | Vehicle Diagnostics")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #0d0d0d; color: #ffffff; font-family: 'Segoe UI', Arial;")

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("CAN-SENTINEL ACTIVE DIAGNOSTICS")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #00e676; margin-bottom: 20px; letter-spacing: 2px;")
        main_layout.addWidget(header)

        # ECU Grid Diagram
        grid_layout = QGridLayout()
        self.ecus = {
            "Engine": ECUWidget("Engine"),
            "Brakes": ECUWidget("Brakes"),
            "Steering": ECUWidget("Steering"),
            "Speed": ECUWidget("Speed"),
            "Temperature": ECUWidget("Temperature")
        }
        
        grid_layout.addWidget(self.ecus["Engine"], 0, 1)
        grid_layout.addWidget(self.ecus["Steering"], 1, 0)
        grid_layout.addWidget(self.ecus["Speed"], 1, 1)
        grid_layout.addWidget(self.ecus["Brakes"], 1, 2)
        grid_layout.addWidget(self.ecus["Temperature"], 2, 1)
        
        main_layout.addLayout(grid_layout)

        # Alert Summary
        self.alert_status = QLabel("SYSTEM STATUS: NORMAL")
        self.alert_status.setAlignment(Qt.AlignCenter)
        self.alert_status.setStyleSheet("font-size: 20px; font-weight: bold; color: #00e676; margin-top: 20px; margin-bottom: 10px;")
        main_layout.addWidget(self.alert_status)

        # Alert Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Component", "CAN ID", "Frequency (Hz)", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                gridline-color: #333333;
                border: none;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #2a2a2a;
                color: #ffffff;
                font-weight: bold;
                border: 1px solid #333333;
                padding: 5px;
            }
        """)
        main_layout.addWidget(self.table)

        self.listener = AlertListenerThread()
        self.listener.new_alert.connect(self.add_alert)
        self.listener.start()

    def add_alert(self, data):
        self.alert_status.setText("SYSTEM STATUS: INTRUSION DETECTED")
        self.alert_status.setStyleSheet("font-size: 20px; font-weight: bold; color: #ff1744; margin-top: 20px; margin-bottom: 10px;")
        
        comp_name = data.get("component", "Unknown")
        if comp_name in self.ecus:
            self.ecus[comp_name].set_compromised()

        row = self.table.rowCount()
        self.table.insertRow(row)
        
        def make_item(text, color="#ffffff", bg="#1e1e1e"):
            item = QTableWidgetItem(str(text))
            item.setForeground(QColor(color))
            item.setBackground(QColor(bg))
            return item

        self.table.setItem(row, 0, make_item(data.get("timestamp", "")))
        self.table.setItem(row, 1, make_item(comp_name, color="#ff5252"))
        self.table.setItem(row, 2, make_item(data.get("can_id", "")))
        self.table.setItem(row, 3, make_item(data.get("frequency", "")))
        self.table.setItem(row, 4, make_item("ANOMALY", color="#ffffff", bg="#b71c1c"))
        
        self.table.scrollToBottom()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
