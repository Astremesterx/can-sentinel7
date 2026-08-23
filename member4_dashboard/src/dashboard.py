import sys

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from PyQt5.QtCore import Qt


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

        dashboard = QLabel("Dashboard")
        can_monitoring = QLabel("CAN Monitoring")
        alerts = QLabel("Security Alerts")
        ecu_status = QLabel("ECU Status")
        analysis = QLabel("Analysis")

        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(30)
        sidebar_layout.addWidget(dashboard)
        sidebar_layout.addWidget(can_monitoring)
        sidebar_layout.addWidget(alerts)
        sidebar_layout.addWidget(ecu_status)
        sidebar_layout.addWidget(analysis)
        sidebar_layout.addStretch()

        # Main dashboard
        content = QWidget()
        content_layout = QVBoxLayout(content)

        heading = QLabel("Diagnostic Dashboard")
        heading.setStyleSheet("font-size: 24px; font-weight: bold;")

        status = QLabel("System Status: Monitoring")
        status.setStyleSheet("font-size: 16px;")

        content_layout.addWidget(heading)
        content_layout.addWidget(status)

        # Dashboard cards
        cards_layout = QHBoxLayout()

        can_card = QLabel("CAN Messages\n0")
        ecu_card = QLabel("ECUs Online\n0")
        alert_card = QLabel("Security Alerts\n0")

        cards_layout.addWidget(can_card)
        cards_layout.addWidget(ecu_card)
        cards_layout.addWidget(alert_card)

        content_layout.addLayout(cards_layout)

        # CAN traffic matrix
        traffic_title = QLabel("Live CAN Traffic Matrix")
        traffic_title.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        content_layout.addWidget(traffic_title)

        traffic_table = QTableWidget()
        traffic_table.setColumnCount(5)
        traffic_table.setHorizontalHeaderLabels(
            ["Timestamp", "CAN ID", "DLC", "Data", "Status"]
        )

        traffic_table.setRowCount(3)

        data = [
            ["12:41:02", "0x123", "8", "01 02 03 04 05 06 07 08", "Normal"],
            ["12:41:03", "0x456", "8", "A1 B2 C3 D4 E5 F6 07 08", "Normal"],
            ["12:41:04", "0x789", "4", "10 20 30 40", "Normal"]
        ]

        for row, row_data in enumerate(data):
            for column, value in enumerate(row_data):
                traffic_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(value)
                )

        traffic_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        content_layout.addWidget(traffic_table)

        # Security alerts
        alert_title = QLabel("Security Alerts")
        alert_title.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        content_layout.addWidget(alert_title)

        alert_message = QLabel("No active threats")
        alert_message.setStyleSheet(
            "font-size: 16px;"
        )

        content_layout.addWidget(alert_message)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)


app = QApplication(sys.argv)

window = Dashboard()
window.show()

sys.exit(app.exec_())