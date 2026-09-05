import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
    QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor

class AlertListenerThread(QThread):
    new_alert = pyqtSignal(dict)

    def run(self):
        for line in sys.stdin:
            line = line.strip()
            if not line: continue
            try:
                data = json.loads(line)
                if data.get('alert_type') == 'INTRUSION_DETECTED':
                    self.new_alert.emit(data)
            except json.JSONDecodeError:
                pass

class ECUWidget(QFrame):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.init_ui()
        
        # Timer to automatically reset the status if no attacks are seen for 2 seconds
        self.reset_timer = QTimer()
        self.reset_timer.setSingleShot(True)
        self.reset_timer.timeout.connect(self.set_normal)

    def init_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #121212;
                border: 2px solid #00e676;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        layout = QVBoxLayout(self)
        
        # Clear existing layout if re-initializing
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        self.title = QLabel(self.name.upper())
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 16px; border: none;")
        
        self.status = QLabel("NORMAL")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("color: #00e676; font-weight: bold; font-size: 20px; border: none; letter-spacing: 1px;")
        
        layout.addWidget(self.title)
        layout.addWidget(self.status)

    def set_compromised(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #3b0000;
                border: 2px solid #ff1744;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        self.title.setStyleSheet("color: #ffcccc; font-weight: bold; font-size: 16px; border: none;")
        self.status.setStyleSheet("color: #ff1744; font-weight: bold; font-size: 20px; border: none; letter-spacing: 1px;")
        self.status.setText("ATTACK FOUND")
        
        # Restart the 2-second countdown timer every time an attack packet arrives
        self.reset_timer.start(2000)

    def set_normal(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #121212;
                border: 2px solid #00e676;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        self.title.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 16px; border: none;")
        self.status.setStyleSheet("color: #00e676; font-weight: bold; font-size: 20px; border: none; letter-spacing: 1px;")
        self.status.setText("NORMAL")

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAN-Sentinel | Vehicle Diagnostics")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #080808; color: #ffffff; font-family: 'Segoe UI', Arial;")

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header
        header = QLabel("CAN-SENTINEL ACTIVE DIAGNOSTICS")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 32px; font-weight: bold; color: #00e676; letter-spacing: 3px;")
        main_layout.addWidget(header)

        # ECU Grid Diagram
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
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

        # Global Alert Summary
        self.alert_status = QLabel("SYSTEM STATUS: ALL SYSTEMS NORMAL")
        self.alert_status.setAlignment(Qt.AlignCenter)
        self.alert_status.setStyleSheet("font-size: 22px; font-weight: bold; color: #00e676; margin-top: 10px;")
        main_layout.addWidget(self.alert_status)
        
        self.global_timer = QTimer()
        self.global_timer.setSingleShot(True)
        self.global_timer.timeout.connect(self.set_global_normal)

        # Alert Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Component", "CAN ID", "Frequency (Hz)", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #121212;
                color: #dddddd;
                gridline-color: #222222;
                border: 1px solid #333333;
                border-radius: 5px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #1a1a1a;
                color: #ffffff;
                font-weight: bold;
                border: 1px solid #222222;
                padding: 8px;
            }
        """)
        main_layout.addWidget(self.table)

        self.listener = AlertListenerThread()
        self.listener.new_alert.connect(self.add_alert)
        self.listener.start()

    def set_global_normal(self):
        self.alert_status.setText("SYSTEM STATUS: ALL SYSTEMS NORMAL")
        self.alert_status.setStyleSheet("font-size: 22px; font-weight: bold; color: #00e676; margin-top: 10px;")

    def add_alert(self, data):
        self.alert_status.setText("SYSTEM STATUS: ACTIVE CYBERATTACK DETECTED!")
        self.alert_status.setStyleSheet("font-size: 22px; font-weight: bold; color: #ff1744; margin-top: 10px; background-color: #3b0000; border-radius: 5px; padding: 5px;")
        self.global_timer.start(2500)
        
        comp_name = data.get("component", "Unknown")
        if comp_name in self.ecus:
            self.ecus[comp_name].set_compromised()

        row = self.table.rowCount()
        self.table.insertRow(row)
        
        def make_item(text, color="#ffffff", bg="#121212"):
            item = QTableWidgetItem(str(text))
            item.setForeground(QColor(color))
            item.setBackground(QColor(bg))
            item.setTextAlignment(Qt.AlignCenter)
            return item

        self.table.setItem(row, 0, make_item(data.get("timestamp", "")))
        self.table.setItem(row, 1, make_item(comp_name, color="#ff5252"))
        self.table.setItem(row, 2, make_item(data.get("can_id", "")))
        self.table.setItem(row, 3, make_item(data.get("frequency", "")))
        self.table.setItem(row, 4, make_item("ATTACK", color="#ffffff", bg="#b71c1c"))
        
        self.table.scrollToBottom()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
