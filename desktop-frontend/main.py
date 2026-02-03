"""
Chemical Equipment Parameter Visualizer - Desktop Application
A PyQt5 desktop client for the Chemical Equipment Visualizer API.
"""

import sys
import os
import requests
from io import BytesIO

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QTabWidget,
    QFileDialog, QMessageBox, QDialog, QLineEdit, QFormLayout,
    QDialogButtonBox, QFrame, QSpacerItem, QSizePolicy, QHeaderView,
    QProgressDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


# Configuration
API_BASE_URL = "http://localhost:8000/api"


class APIClient:
    """Handle all API communications."""
    
    def __init__(self):
        self.token = None
        self.session = requests.Session()
    
    def set_token(self, token):
        self.token = token
        self.session.headers.update({'Authorization': f'Token {token}'})
    
    def login(self, username, password):
        try:
            response = requests.post(
                f"{API_BASE_URL}/auth/token/",
                json={'username': username, 'password': password}
            )
            response.raise_for_status()
            data = response.json()
            self.set_token(data['token'])
            return True, data['token']
        except requests.exceptions.RequestException as e:
            return False, str(e)
    
    def get_dashboard_stats(self):
        try:
            response = self.session.get(f"{API_BASE_URL}/dashboard/")
            response.raise_for_status()
            return True, response.json()
        except requests.exceptions.RequestException as e:
            return False, str(e)
    
    def upload_csv(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, 'text/csv')}
                response = self.session.post(
                    f"{API_BASE_URL}/upload/",
                    files=files
                )
            response.raise_for_status()
            return True, response.json()
        except requests.exceptions.RequestException as e:
            return False, str(e)
    
    def download_pdf(self):
        try:
            response = self.session.get(f"{API_BASE_URL}/report/pdf/")
            response.raise_for_status()
            return True, response.content
        except requests.exceptions.RequestException as e:
            return False, str(e)


class LoginDialog(QDialog):
    """Authentication dialog."""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Login - Chemical Equipment Visualizer")
        self.setFixedSize(380, 320)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1b4b;
            }
            QLabel {
                color: #e2e8f0;
                font-size: 13px;
            }
            QLabel#title {
                font-size: 20px;
                font-weight: bold;
                color: #fff;
            }
            QLabel#subtitle {
                font-size: 12px;
                color: #94a3b8;
                margin-bottom: 20px;
            }
            QLineEdit {
                padding: 12px 16px;
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: #fff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #6366f1;
                background-color: rgba(99, 102, 241, 0.1);
            }
            QPushButton {
                padding: 14px;
                background-color: #6366f1;
                border: none;
                border-radius: 8px;
                color: #fff;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8b5cf6;
            }
            QPushButton:pressed {
                background-color: #5b21b6;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("Chemical Equipment")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Parameter Visualizer")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        layout.addSpacing(10)
        
        # Login button
        self.login_button = QPushButton("Sign In")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        
        # Hint
        hint = QLabel("Default: admin / admin123")
        hint.setStyleSheet("color: #64748b; font-size: 11px;")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)
        
        # Enter key triggers login
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
    
    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return
        
        self.login_button.setEnabled(False)
        self.login_button.setText("Signing in...")
        
        success, result = self.api_client.login(username, password)
        
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Login Failed", f"Could not authenticate: {result}")
            self.login_button.setEnabled(True)
            self.login_button.setText("Sign In")


class ChartCanvas(FigureCanvas):
    """Matplotlib canvas for embedding in PyQt5."""
    
    def __init__(self, parent=None, width=8, height=5):
        self.fig = Figure(figsize=(width, height), dpi=100, facecolor='#1e1b4b')
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setup_style()
    
    def setup_style(self):
        self.axes.set_facecolor('#0f172a')
        self.axes.tick_params(colors='#94a3b8')
        self.axes.spines['bottom'].set_color('#334155')
        self.axes.spines['top'].set_color('#334155')
        self.axes.spines['left'].set_color('#334155')
        self.axes.spines['right'].set_color('#334155')
        self.axes.xaxis.label.set_color('#e2e8f0')
        self.axes.yaxis.label.set_color('#e2e8f0')
        self.axes.title.set_color('#fff')
    
    def plot_bar_chart(self, type_distribution):
        self.axes.clear()
        self.setup_style()
        
        if not type_distribution:
            self.axes.text(0.5, 0.5, 'No data available', 
                          ha='center', va='center', color='#94a3b8', fontsize=14)
            self.draw()
            return
        
        types = list(type_distribution.keys())
        counts = list(type_distribution.values())
        colors = ['#8b5cf6', '#3b82f6', '#10b981', '#f97316', '#ec4899', '#eab308']
        
        bars = self.axes.bar(types, counts, color=colors[:len(types)], 
                            edgecolor='none', width=0.6)
        
        self.axes.set_xlabel('Equipment Type', fontsize=11)
        self.axes.set_ylabel('Count', fontsize=11)
        self.axes.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold', pad=15)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            self.axes.annotate(f'{count}',
                              xy=(bar.get_x() + bar.get_width() / 2, height),
                              xytext=(0, 3),
                              textcoords="offset points",
                              ha='center', va='bottom', color='#e2e8f0', fontsize=10)
        
        self.fig.tight_layout()
        self.draw()


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.equipment_data = []
        self.type_distribution = {}
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setMinimumSize(1100, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
            }
            QWidget {
                background-color: #0f172a;
                color: #e2e8f0;
            }
            QTabWidget::pane {
                border: 1px solid #334155;
                border-radius: 8px;
                background-color: #1e1b4b;
            }
            QTabBar::tab {
                background-color: #1e293b;
                color: #94a3b8;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: #1e1b4b;
                color: #fff;
            }
            QTableWidget {
                background-color: #1e1b4b;
                border: none;
                gridline-color: #334155;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #334155;
            }
            QTableWidget::item:selected {
                background-color: rgba(99, 102, 241, 0.3);
            }
            QHeaderView::section {
                background-color: #0f172a;
                color: #94a3b8;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #6366f1;
                font-weight: bold;
            }
            QPushButton {
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton#uploadBtn {
                background-color: #6366f1;
                color: #fff;
                border: none;
            }
            QPushButton#uploadBtn:hover {
                background-color: #8b5cf6;
            }
            QPushButton#pdfBtn {
                background-color: rgba(16, 185, 129, 0.2);
                color: #6ee7b7;
                border: 1px solid rgba(16, 185, 129, 0.3);
            }
            QPushButton#pdfBtn:hover {
                background-color: rgba(16, 185, 129, 0.3);
            }
            QPushButton#refreshBtn {
                background-color: rgba(59, 130, 246, 0.2);
                color: #60a5fa;
                border: 1px solid rgba(59, 130, 246, 0.3);
            }
            QPushButton#refreshBtn:hover {
                background-color: rgba(59, 130, 246, 0.3);
            }
            QLabel#statCard {
                background-color: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)
        
        # Header
        header = self.create_header()
        main_layout.addLayout(header)
        
        # Stats cards
        self.stats_layout = self.create_stats_cards()
        main_layout.addLayout(self.stats_layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs, 1)
        
        # Data tab
        data_tab = QWidget()
        data_layout = QVBoxLayout(data_tab)
        data_layout.setContentsMargins(16, 16, 16, 16)
        self.table = self.create_data_table()
        data_layout.addWidget(self.table)
        self.tabs.addTab(data_tab, "📊 Data Table")
        
        # Visuals tab
        visuals_tab = QWidget()
        visuals_layout = QVBoxLayout(visuals_tab)
        visuals_layout.setContentsMargins(16, 16, 16, 16)
        self.chart_canvas = ChartCanvas(visuals_tab)
        visuals_layout.addWidget(self.chart_canvas)
        self.tabs.addTab(visuals_tab, "📈 Visualizations")
    
    def create_header(self):
        header = QHBoxLayout()
        
        # Title
        title = QLabel("Chemical Equipment Visualizer")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #fff;")
        header.addWidget(title)
        
        header.addStretch()
        
        # Buttons
        self.upload_btn = QPushButton("📤 Upload CSV")
        self.upload_btn.setObjectName("uploadBtn")
        self.upload_btn.clicked.connect(self.upload_csv)
        header.addWidget(self.upload_btn)
        
        self.pdf_btn = QPushButton("📄 Download PDF")
        self.pdf_btn.setObjectName("pdfBtn")
        self.pdf_btn.clicked.connect(self.download_pdf)
        header.addWidget(self.pdf_btn)
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setObjectName("refreshBtn")
        self.refresh_btn.clicked.connect(self.refresh_data)
        header.addWidget(self.refresh_btn)
        
        return header
    
    def create_stats_cards(self):
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        # Create stat cards
        self.total_label = self.create_stat_card("Total Equipment", "0", "#8b5cf6")
        self.flowrate_label = self.create_stat_card("Avg Flowrate", "0", "#3b82f6")
        self.pressure_label = self.create_stat_card("Avg Pressure", "0", "#10b981")
        self.temp_label = self.create_stat_card("Avg Temperature", "0", "#f97316")
        
        stats_layout.addWidget(self.total_label)
        stats_layout.addWidget(self.flowrate_label)
        stats_layout.addWidget(self.pressure_label)
        stats_layout.addWidget(self.temp_label)
        
        return stats_layout
    
    def create_stat_card(self, title, value, color):
        card = QFrame()
        card.setObjectName("statCard")
        card.setStyleSheet(f"""
            QFrame#statCard {{
                background-color: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 12px;
                padding: 16px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #94a3b8; font-size: 12px;")
        layout.addWidget(title_lbl)
        
        value_lbl = QLabel(value)
        value_lbl.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")
        value_lbl.setProperty("value_label", True)
        layout.addWidget(value_lbl)
        
        return card
    
    def update_stat_card(self, card, value):
        for child in card.findChildren(QLabel):
            if child.property("value_label"):
                child.setText(str(value))
                break
    
    def create_data_table(self):
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([
            "Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"
        ])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setAlternatingRowColors(True)
        table.setAlternatingRowColors(False)
        table.setShowGrid(True)
        return table
    
    def refresh_data(self):
        success, data = self.api_client.get_dashboard_stats()
        
        if not success:
            QMessageBox.critical(self, "Error", f"Failed to fetch data: {data}")
            return
        
        # Update stats
        self.update_stat_card(self.total_label, data.get('total_count', 0))
        avg_values = data.get('average_values', {})
        self.update_stat_card(self.flowrate_label, round(avg_values.get('flowrate', 0), 2))
        self.update_stat_card(self.pressure_label, round(avg_values.get('pressure', 0), 2))
        self.update_stat_card(self.temp_label, round(avg_values.get('temperature', 0), 2))
        
        # Update table
        self.equipment_data = data.get('equipment_data', [])
        self.update_table()
        
        # Update chart
        self.type_distribution = data.get('type_distribution', {})
        self.chart_canvas.plot_bar_chart(self.type_distribution)
    
    def update_table(self):
        self.table.setRowCount(len(self.equipment_data))
        
        for row, item in enumerate(self.equipment_data):
            self.table.setItem(row, 0, QTableWidgetItem(item['equipment_name']))
            self.table.setItem(row, 1, QTableWidgetItem(item['type']))
            self.table.setItem(row, 2, QTableWidgetItem(f"{item['flowrate']:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{item['pressure']:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{item['temperature']:.2f}"))
    
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)"
        )
        
        if not file_path:
            return
        
        success, result = self.api_client.upload_csv(file_path)
        
        if success:
            QMessageBox.information(
                self, 
                "Success", 
                f"Successfully uploaded {result.get('records_created', 0)} records!"
            )
            self.refresh_data()
        else:
            QMessageBox.critical(self, "Upload Failed", f"Error: {result}")
    
    def download_pdf(self):
        if not self.equipment_data:
            QMessageBox.warning(self, "No Data", "No data available to generate report")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            "equipment_report.pdf",
            "PDF Files (*.pdf)"
        )
        
        if not file_path:
            return
        
        success, result = self.api_client.download_pdf()
        
        if success:
            with open(file_path, 'wb') as f:
                f.write(result)
            QMessageBox.information(self, "Success", f"Report saved to:\n{file_path}")
        else:
            QMessageBox.critical(self, "Error", f"Failed to generate PDF: {result}")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(15, 23, 42))
    palette.setColor(QPalette.WindowText, QColor(226, 232, 240))
    palette.setColor(QPalette.Base, QColor(30, 27, 75))
    palette.setColor(QPalette.AlternateBase, QColor(15, 23, 42))
    palette.setColor(QPalette.ToolTipBase, QColor(30, 27, 75))
    palette.setColor(QPalette.ToolTipText, QColor(226, 232, 240))
    palette.setColor(QPalette.Text, QColor(226, 232, 240))
    palette.setColor(QPalette.Button, QColor(30, 27, 75))
    palette.setColor(QPalette.ButtonText, QColor(226, 232, 240))
    palette.setColor(QPalette.Highlight, QColor(99, 102, 241))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    # Create API client
    api_client = APIClient()
    
    # Show login dialog
    login_dialog = LoginDialog(api_client)
    if login_dialog.exec_() != QDialog.Accepted:
        sys.exit(0)
    
    # Show main window
    main_window = MainWindow(api_client)
    main_window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
