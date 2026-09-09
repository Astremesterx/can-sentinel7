import sys
import json
import csv
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
    QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
    QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor

class AlertListenerThread(QThread):
    new_alert = pyqtSignal(dict)

    def run(self):
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
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
        self.attack_count = 0
        self.last_freq = 0.0

        # Timer to automatically reset the visual alert status if no attacks are seen for 2.5 seconds
        self.reset_timer = QTimer()
        self.reset_timer.setSingleShot(True)
        self.reset_timer.timeout.connect(self.set_normal)

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #121212;
                border: 2px solid #00e676;
                border-radius: 10px;
                padding: 12px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        # Clear existing layout if re-initializing
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.title = QLabel(self.name.upper())
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 15px; border: none;")

        self.status = QLabel("NORMAL")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("color: #00e676; font-weight: bold; font-size: 20px; border: none; letter-spacing: 1px;")

        self.counter_lbl = QLabel(f"Attacks Logged: {self.attack_count}")
        self.counter_lbl.setAlignment(Qt.AlignCenter)
        self.counter_lbl.setStyleSheet("color: #888888; font-size: 11px; border: none;")

        layout.addWidget(self.title)
        layout.addWidget(self.status)
        layout.addWidget(self.counter_lbl)

    def set_compromised(self, freq=0.0):
        self.attack_count += 1
        self.last_freq = freq

        self.setStyleSheet("""
            QFrame {
                background-color: #3b0000;
                border: 2px solid #ff1744;
                border-radius: 10px;
                padding: 12px;
            }
        """)
        self.title.setStyleSheet("color: #ffcccc; font-weight: bold; font-size: 15px; border: none;")
        self.status.setStyleSheet("color: #ff1744; font-weight: bold; font-size: 20px; border: none; letter-spacing: 1px;")
        self.status.setText("ATTACK FOUND")

        self.counter_lbl.setStyleSheet("color: #ff8a80; font-weight: bold; font-size: 11px; border: none;")
        self.counter_lbl.setText(f"Attacks Logged: {self.attack_count} ({freq:.1f} Hz)")

        # Restart the 2.5-second countdown timer
        self.reset_timer.start(2500)

    def set_normal(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #121212;
                border: 2px solid #00e676;
                border-radius: 10px;
                padding: 12px;
            }
        """)
        self.title.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 15px; border: none;")
        self.status.setStyleSheet("color: #00e676; font-weight: bold; font-size: 20px; border: none; letter-spacing: 1px;")
        self.status.setText("NORMAL")
        self.counter_lbl.setStyleSheet("color: #888888; font-size: 11px; border: none;")
        self.counter_lbl.setText(f"Attacks Logged: {self.attack_count}")

    def reset_stats(self):
        self.attack_count = 0
        self.set_normal()

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAN-Sentinel | Automotive ECU Threat Intelligence & Diagnostics")
        self.setGeometry(80, 80, 1260, 840)
        self.setStyleSheet("background-color: #0a0a0a; color: #ffffff; font-family: 'Segoe UI', Arial, sans-serif;")

        self.total_incidents = 0
        self.peak_frequency = 0.0
        self.incident_history = []

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(15)

        # Header Title
        header = QLabel("CAN-SENTINEL ACTIVE THREAT INTELLIGENCE")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #00e676; letter-spacing: 3px;")
        main_layout.addWidget(header)

        # Telemetry Stat Bar
        telemetry_frame = QFrame()
        telemetry_frame.setStyleSheet("background-color: #151515; border: 1px solid #282828; border-radius: 8px; padding: 6px;")
        telemetry_layout = QHBoxLayout(telemetry_frame)

        self.stat_incidents = QLabel("Total Incidents: 0")
        self.stat_incidents.setStyleSheet("font-size: 14px; font-weight: bold; color: #00e676;")

        self.stat_threat_level = QLabel("Threat Level: DEFCON 5 (NOMINAL)")
        self.stat_threat_level.setStyleSheet("font-size: 14px; font-weight: bold; color: #00e676;")

        self.stat_peak_freq = QLabel("Peak Anomaly Freq: 0.0 Hz")
        self.stat_peak_freq.setStyleSheet("font-size: 14px; font-weight: bold; color: #888888;")

        telemetry_layout.addWidget(self.stat_incidents)
        telemetry_layout.addStretch()
        telemetry_layout.addWidget(self.stat_threat_level)
        telemetry_layout.addStretch()
        telemetry_layout.addWidget(self.stat_peak_freq)

        main_layout.addWidget(telemetry_frame)

        # ECU Schematic Grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(12)

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

        # Global Alert Banner
        self.alert_status = QLabel("SYSTEM STATUS: ALL SYSTEMS NOMINAL")
        self.alert_status.setAlignment(Qt.AlignCenter)
        self.alert_status.setStyleSheet("font-size: 18px; font-weight: bold; color: #00e676; padding: 6px; border-radius: 5px;")
        main_layout.addWidget(self.alert_status)

        self.global_timer = QTimer()
        self.global_timer.setSingleShot(True)
        self.global_timer.timeout.connect(self.set_global_normal)

        # Live Incident Log Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Target Component", "CAN ID", "Anomaly Freq (Hz)", "Classification"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #121212;
                color: #dddddd;
                gridline-color: #222222;
                border: 1px solid #333333;
                border-radius: 6px;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #1a1a1a;
                color: #ffffff;
                font-weight: bold;
                border: 1px solid #222222;
                padding: 6px;
            }
        """)
        main_layout.addWidget(self.table)

        # Bottom Controls: Export & Reset
        btn_layout = QHBoxLayout()

        self.btn_export = QPushButton("Export Incident Report (.CSV)")
        self.btn_export.setStyleSheet("""
            QPushButton {
                background-color: #1e3a8a;
                color: #ffffff;
                border: 1px solid #3b82f6;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2563eb; }
        """)
        self.btn_export.clicked.connect(self.export_report)

        self.btn_reset = QPushButton("Reset Statistics")
        self.btn_reset.setStyleSheet("""
            QPushButton {
                background-color: #262626;
                color: #cccccc;
                border: 1px solid #404040;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #404040; color: #ffffff; }
        """)
        self.btn_reset.clicked.connect(self.reset_all)

        btn_layout.addWidget(self.btn_export)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_reset)

        main_layout.addLayout(btn_layout)

        # Background Listener
        self.listener = AlertListenerThread()
        self.listener.new_alert.connect(self.add_alert)
        self.listener.start()

    def set_global_normal(self):
        self.alert_status.setText("SYSTEM STATUS: ALL SYSTEMS NOMINAL")
        self.alert_status.setStyleSheet("font-size: 18px; font-weight: bold; color: #00e676; padding: 6px; border-radius: 5px;")
        self.stat_threat_level.setText("Threat Level: DEFCON 5 (NOMINAL)")
        self.stat_threat_level.setStyleSheet("font-size: 14px; font-weight: bold; color: #00e676;")

    def add_alert(self, data):
        self.total_incidents += 1
        freq = float(data.get("frequency", 0.0))
        if freq > self.peak_frequency:
            self.peak_frequency = freq
            self.stat_peak_freq.setText(f"Peak Anomaly Freq: {self.peak_frequency:.1f} Hz")

        self.stat_incidents.setText(f"Total Incidents: {self.total_incidents}")
        self.stat_threat_level.setText("Threat Level: DEFCON 1 (ACTIVE INTRUSION)")
        self.stat_threat_level.setStyleSheet("font-size: 14px; font-weight: bold; color: #ff1744;")

        self.alert_status.setText("ALERT: ACTIVE CYBERATTACK IN PROGRESS!")
        self.alert_status.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff; background-color: #b71c1c; padding: 6px; border-radius: 5px;")
        self.global_timer.start(3000)

        comp_name = data.get("component", "Unknown")
        if comp_name in self.ecus:
            self.ecus[comp_name].set_compromised(freq)

        # Log to incident history
        record = {
            "timestamp": data.get("timestamp", str(time.time())),
            "component": comp_name,
            "can_id": data.get("can_id", ""),
            "frequency": freq,
            "status": "ANOMALY"
        }
        self.incident_history.append(record)

        # Sliding window for table (keep max 200 rows for high performance)
        if self.table.rowCount() >= 200:
            self.table.removeRow(0)

        row = self.table.rowCount()
        self.table.insertRow(row)

        def make_item(text, color="#ffffff", bg="#121212"):
            item = QTableWidgetItem(str(text))
            item.setForeground(QColor(color))
            item.setBackground(QColor(bg))
            item.setTextAlignment(Qt.AlignCenter)
            return item

        self.table.setItem(row, 0, make_item(record["timestamp"]))
        self.table.setItem(row, 1, make_item(comp_name, color="#ff5252"))
        self.table.setItem(row, 2, make_item(record["can_id"]))
        self.table.setItem(row, 3, make_item(f"{freq:.2f}"))
        self.table.setItem(row, 4, make_item("ANOMALY", color="#ffffff", bg="#b71c1c"))

        self.table.scrollToBottom()

    def export_report(self):
        if not self.incident_history:
            QMessageBox.information(self, "Export Report", "No incident alerts have been recorded yet.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Save Incident Report", "can_sentinel_incident_report.csv", "CSV Files (*.csv)")
        if not filename:
            return

        try:
            with open(filename, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["timestamp", "component", "can_id", "frequency", "status"])
                writer.writeheader()
                writer.writerows(self.incident_history)
            QMessageBox.information(self, "Export Report", f"Successfully exported {len(self.incident_history)} incident records to:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export report: {e}")

    def reset_all(self):
        self.total_incidents = 0
        self.peak_frequency = 0.0
        self.incident_history.clear()
        self.table.setRowCount(0)
        self.stat_incidents.setText("Total Incidents: 0")
        self.stat_peak_freq.setText("Peak Anomaly Freq: 0.0 Hz")
        self.set_global_normal()
        for ecu in self.ecus.values():
            ecu.reset_stats()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
