import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class AlertListenerThread(QThread):
    new_alert = pyqtSignal(dict)

    def run(self):
        # Continuously read from standard input
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                # If it's a JSON alert from the ML Engine
                data = json.loads(line)
                if data.get("alert_type") == "INTRUSION_DETECTED":
                    self.new_alert.emit(data)
            except json.JSONDecodeError:
                pass

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CAN-Sentinel Diagnostic Dashboard")
        self.setGeometry(100, 100, 1200, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar)

        title = QLabel("CAN-SENTINEL")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")

        sidebar_layout.addWidget(title)
        sidebar_layout.addWidget(QLabel("Dashboard"))
        sidebar_layout.addWidget(QLabel("CAN Monitoring"))
        sidebar_layout.addWidget(QLabel("Security Alerts"))
        sidebar_layout.addWidget(QLabel("ECU Status"))
        sidebar_layout.addWidget(QLabel("Analysis"))
        sidebar_layout.addStretch()

        # Main dashboard
        content = QWidget()
        content_layout = QVBoxLayout(content)

        heading = QLabel("Diagnostic Dashboard")
        heading.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.status = QLabel("System Status: Monitoring Live Traffic")
        self.status.setStyleSheet("font-size: 16px; color: green;")

        content_layout.addWidget(heading)
        content_layout.addWidget(self.status)

        # Dashboard cards
        cards_layout = QHBoxLayout()
        self.threat_level = QLabel("Threat Level\nNORMAL")
        self.alert_count = 0
        self.alert_card = QLabel("Security Alerts\n0")
        self.alert_card.setStyleSheet("font-size: 18px; padding: 20px; background-color: #f8f9fa; border: 1px solid #ddd; border-radius: 8px;")
        self.threat_level.setStyleSheet("font-size: 18px; padding: 20px; background-color: #f8f9fa; border: 1px solid #ddd; border-radius: 8px;")
        cards_layout.addWidget(self.alert_card)
        cards_layout.addWidget(self.threat_level)
        content_layout.addLayout(cards_layout)

        # Security Alerts Table
        alert_title = QLabel("Live Intrusion Alerts")
        alert_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        content_layout.addWidget(alert_title)

        self.traffic_table = QTableWidget()
        self.traffic_table.setColumnCount(5)
        self.traffic_table.setHorizontalHeaderLabels(
            ["Timestamp", "Component", "CAN ID", "Frequency (Hz)", "Status"]
        )
        self.traffic_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        content_layout.addWidget(self.traffic_table)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        # Start background listener
        self.listener = AlertListenerThread()
        self.listener.new_alert.connect(self.add_alert)
        self.listener.start()

    def add_alert(self, data):
        self.alert_count += 1
        self.alert_card.setText(f"Security Alerts\n{self.alert_count}")
        self.threat_level.setText("Threat Level\nHIGH")
        self.alert_card.setStyleSheet("font-size: 18px; padding: 20px; background-color: #ffebee; color: #c62828; border: 1px solid #ef9a9a; border-radius: 8px; font-weight: bold;")
        self.threat_level.setStyleSheet("font-size: 18px; padding: 20px; background-color: #f8f9fa; border: 1px solid #ddd; border-radius: 8px; font-weight: bold;")
        self.status.setText("System Status: INTRUSION DETECTED!")
        self.status.setStyleSheet("font-size: 16px; color: red; font-weight: bold;")

        row_position = self.traffic_table.rowCount()
        self.traffic_table.insertRow(row_position)

        self.traffic_table.setItem(row_position, 0, QTableWidgetItem(str(data.get("timestamp", ""))))
        
        # Highlight component clearly
        comp_item = QTableWidgetItem(str(data.get("component", "Unknown")))
        comp_item.setForeground(Qt.red)
        self.traffic_table.setItem(row_position, 1, comp_item)
        
        self.traffic_table.setItem(row_position, 2, QTableWidgetItem(str(data.get("can_id", ""))))
        self.traffic_table.setItem(row_position, 3, QTableWidgetItem(str(data.get("frequency", ""))))
        
        status_item = QTableWidgetItem(str(data.get("status", "ANOMALY")))
        status_item.setForeground(Qt.white)
        status_item.setBackground(Qt.red)
        self.traffic_table.setItem(row_position, 4, status_item)

app = QApplication(sys.argv)
window = Dashboard()
window.show()
sys.exit(app.exec_())
