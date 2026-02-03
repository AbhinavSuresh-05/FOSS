"""
Chemical Equipment Parameter Visualizer - Desktop Application
A modern PyQt5 desktop client with professional UI styling.
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
    QProgressDialog, QGraphicsDropShadowEffect, QScrollArea, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QPixmap

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


# Configuration
API_BASE_URL = "http://localhost:8000/api"


# =============================================================================
# GLOBAL QSS STYLESHEET
# =============================================================================
GLOBAL_STYLESHEET = """
/* ============================================
   GLOBAL STYLES
   ============================================ */

* {
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
}

QMainWindow, QDialog, QWidget {
    background-color: #0f172a;
    color: #e2e8f0;
}

QLabel {
    color: #e2e8f0;
    background: transparent;
}

/* ============================================
   BUTTONS - Primary Style
   ============================================ */

QPushButton {
    background-color: #6366f1;
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 14px 28px;
    font-size: 14px;
    font-weight: 600;
    min-height: 20px;
}

QPushButton:hover {
    background-color: #818cf8;
}

QPushButton:pressed {
    background-color: #4f46e5;
}

QPushButton:disabled {
    background-color: #374151;
    color: #6b7280;
}

QPushButton#uploadBtn {
    background-color: #6366f1;
}

QPushButton#uploadBtn:hover {
    background-color: #818cf8;
}

QPushButton#pdfBtn {
    background-color: rgba(16, 185, 129, 0.15);
    color: #6ee7b7;
    border: 1px solid rgba(16, 185, 129, 0.4);
}

QPushButton#pdfBtn:hover {
    background-color: rgba(16, 185, 129, 0.25);
}

QPushButton#refreshBtn {
    background-color: rgba(59, 130, 246, 0.15);
    color: #60a5fa;
    border: 1px solid rgba(59, 130, 246, 0.4);
}

QPushButton#refreshBtn:hover {
    background-color: rgba(59, 130, 246, 0.25);
}

/* ============================================
   INPUT FIELDS
   ============================================ */

QLineEdit {
    background-color: rgba(255, 255, 255, 0.06);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 15px;
    color: #ffffff;
    selection-background-color: #6366f1;
}

QLineEdit:focus {
    border-color: #6366f1;
    background-color: rgba(99, 102, 241, 0.1);
}

QLineEdit::placeholder {
    color: rgba(255, 255, 255, 0.4);
}

/* ============================================
   TAB WIDGET
   ============================================ */

QTabWidget::pane {
    background-color: #1e1b4b;
    border: 1px solid rgba(139, 92, 246, 0.2);
    border-radius: 16px;
    padding: 8px;
    margin-top: -1px;
}

QTabBar {
    background: transparent;
}

QTabBar::tab {
    background-color: transparent;
    color: #94a3b8;
    padding: 16px 32px;
    margin-right: 8px;
    font-size: 14px;
    font-weight: 600;
    border: none;
    border-bottom: 3px solid transparent;
    min-width: 120px;
}

QTabBar::tab:selected {
    color: #ffffff;
    border-bottom: 3px solid #6366f1;
    background-color: rgba(99, 102, 241, 0.1);
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
}

QTabBar::tab:hover:!selected {
    color: #cbd5e1;
    background-color: rgba(255, 255, 255, 0.03);
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
}

/* ============================================
   TABLE WIDGET - Fixed Alignment
   ============================================ */

QTableWidget {
    background-color: transparent;
    border: none;
    gridline-color: rgba(255, 255, 255, 0.06);
    selection-background-color: rgba(99, 102, 241, 0.3);
    selection-color: #ffffff;
    font-size: 14px;
}

QTableWidget::item {
    padding: 12px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

QTableWidget::item:selected {
    background-color: rgba(99, 102, 241, 0.25);
}

QTableWidget::item:alternate {
    background-color: rgba(255, 255, 255, 0.02);
}

QHeaderView {
    background-color: transparent;
}

QHeaderView::section {
    background-color: #0f172a;
    color: #94a3b8;
    padding: 14px 16px;
    border: none;
    border-bottom: 2px solid #6366f1;
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Scrollbar Styling */
QScrollBar:vertical {
    background-color: rgba(255, 255, 255, 0.03);
    width: 10px;
    margin: 0;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: rgba(139, 92, 246, 0.4);
    min-height: 30px;
    border-radius: 5px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background-color: rgba(139, 92, 246, 0.6);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: rgba(255, 255, 255, 0.03);
    height: 10px;
    margin: 0;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background-color: rgba(139, 92, 246, 0.4);
    min-width: 30px;
    border-radius: 5px;
    margin: 2px;
}

/* ============================================
   FRAMES & CARDS
   ============================================ */

QFrame#statCard {
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
}

QFrame#statCard:hover {
    background-color: rgba(255, 255, 255, 0.05);
    border-color: rgba(139, 92, 246, 0.3);
}

/* ============================================
   MESSAGE BOX
   ============================================ */

QMessageBox {
    background-color: #1e1b4b;
}

QMessageBox QLabel {
    color: #e2e8f0;
    font-size: 14px;
}

QMessageBox QPushButton {
    min-width: 100px;
    padding: 10px 20px;
}
"""


# =============================================================================
# API CLIENT
# =============================================================================

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
    
    def register(self, username, password, password_confirm):
        try:
            response = requests.post(
                f"{API_BASE_URL}/auth/register/",
                json={
                    'username': username,
                    'password': password,
                    'password_confirm': password_confirm
                }
            )
            if response.status_code == 201:
                return True, response.json()
            else:
                # Parse validation errors
                errors = response.json()
                error_messages = []
                for field, msgs in errors.items():
                    if isinstance(msgs, list):
                        error_messages.extend(msgs)
                    else:
                        error_messages.append(str(msgs))
                return False, ' '.join(error_messages) if error_messages else 'Registration failed'
        except requests.exceptions.RequestException as e:
            return False, str(e)


# =============================================================================
# LOGIN DIALOG - Responsive with Max Width
# =============================================================================

class LoginDialog(QDialog):
    """Modern authentication dialog with responsive centered form."""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setMinimumSize(480, 520)
        self.resize(600, 600)
        
        # Main layout that fills the dialog
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create a scrollable container for responsiveness
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        # Container widget
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        
        # Spacer at top
        container_layout.addStretch(1)
        
        # Create a centered form wrapper with MAX WIDTH
        form_wrapper = QWidget()
        form_wrapper.setMaximumWidth(420)  # Constrain form width
        form_wrapper.setMinimumWidth(320)
        form_layout = QVBoxLayout(form_wrapper)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(0)
        
        # Logo/Icon - Flask Image
        logo_container = QLabel()
        logo_pixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'app-icon.png'))
        if not logo_pixmap.isNull():
            scaled_pixmap = logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_container.setPixmap(scaled_pixmap)
        logo_container.setFixedSize(100, 100)
        logo_container.setAlignment(Qt.AlignCenter)
        logo_container.setStyleSheet("background: transparent;")
        
        logo_h_layout = QHBoxLayout()
        logo_h_layout.addStretch()
        logo_h_layout.addWidget(logo_container)
        logo_h_layout.addStretch()
        form_layout.addLayout(logo_h_layout)
        
        form_layout.addSpacing(30)
        
        # Title
        title = QLabel("Chemical Equipment")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.5px;
        """)
        title.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Parameter Visualizer")
        subtitle.setStyleSheet("""
            font-size: 16px;
            color: #94a3b8;
            margin-top: 4px;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(subtitle)
        
        form_layout.addSpacing(40)
        
        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("👤  Username")
        self.username_input.setMinimumHeight(56)
        form_layout.addWidget(self.username_input)
        
        form_layout.addSpacing(16)
        
        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("🔒  Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(56)
        form_layout.addWidget(self.password_input)
        
        form_layout.addSpacing(28)
        
        # Login button
        self.login_button = QPushButton("Sign In  →")
        self.login_button.setMinimumHeight(56)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6);
                font-size: 16px;
                font-weight: 700;
                border-radius: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #818cf8, stop:1 #a78bfa);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4f46e5, stop:1 #7c3aed);
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        form_layout.addWidget(self.login_button)
        
        form_layout.addSpacing(24)
        
        # Hint
        hint = QLabel("Default credentials:  admin / admin123")
        hint.setStyleSheet("""
            font-size: 13px;
            color: #64748b;
        """)
        hint.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(hint)
        
        form_layout.addSpacing(16)
        
        # Sign up link
        signup_label = QLabel("Don't have an account?")
        signup_label.setStyleSheet("font-size: 13px; color: #64748b;")
        signup_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(signup_label)
        
        self.signup_button = QPushButton("Create Account")
        self.signup_button.setCursor(Qt.PointingHandCursor)
        self.signup_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #10b981;
                font-size: 14px;
                font-weight: 600;
                border: none;
                padding: 8px;
            }
            QPushButton:hover {
                color: #34d399;
                text-decoration: underline;
            }
        """)
        self.signup_button.clicked.connect(self.open_register)
        form_layout.addWidget(self.signup_button)
        
        # Center the form wrapper horizontally
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(form_wrapper)
        center_layout.addStretch()
        container_layout.addLayout(center_layout)
        
        # Spacer at bottom
        container_layout.addStretch(2)
        
        scroll.setWidget(container)
        outer_layout.addWidget(scroll)
        
        # Enter key triggers login
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
    
    def open_register(self):
        """Open registration dialog and auto-login on success."""
        self.hide()
        register_dialog = RegisterDialog(self.api_client, self)
        if register_dialog.exec_() == QDialog.Accepted:
            # Auto-login with the newly created credentials
            username = register_dialog.registered_username
            password = register_dialog.registered_password
            success, result = self.api_client.login(username, password)
            if success:
                self.accept()  # Close login dialog and proceed to main app
                return
            else:
                QMessageBox.warning(self, "Auto-Login Failed", 
                    "Account created but auto-login failed. Please login manually.")
        self.show()
    
    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Validation Error", "Please enter both username and password")
            return
        
        self.login_button.setEnabled(False)
        self.login_button.setText("Signing in...")
        QApplication.processEvents()
        
        success, result = self.api_client.login(username, password)
        
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Authentication Failed", 
                f"Could not sign in.\n\nPlease check your credentials and ensure the backend server is running.")
            self.login_button.setEnabled(True)
            self.login_button.setText("Sign In  →")


# =============================================================================
# REGISTER DIALOG
# =============================================================================

class RegisterDialog(QDialog):
    """Registration dialog with password validation."""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Create Account")
        self.setMinimumSize(480, 600)
        self.resize(600, 700)
        
        # Main layout
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        
        container_layout.addStretch(1)
        
        # Form wrapper
        form_wrapper = QWidget()
        form_wrapper.setMaximumWidth(420)
        form_wrapper.setMinimumWidth(320)
        form_layout = QVBoxLayout(form_wrapper)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(0)
        
        # Logo with flask icon (no background box)
        logo_container = QLabel()
        logo_container.setFixedSize(100, 100)
        logo_container.setAlignment(Qt.AlignCenter)
        
        # Load flask icon
        icon_path = os.path.join(os.path.dirname(__file__), 'app-icon.png')
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_container.setPixmap(scaled_pixmap)
        
        logo_h_layout = QHBoxLayout()
        logo_h_layout.addStretch()
        logo_h_layout.addWidget(logo_container)
        logo_h_layout.addStretch()
        form_layout.addLayout(logo_h_layout)
        
        form_layout.addSpacing(24)
        
        # Title
        title = QLabel("Create Account")
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: 700;
            color: #ffffff;
        """)
        title.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(title)
        
        subtitle = QLabel("Join Chemical Equipment Visualizer")
        subtitle.setStyleSheet("font-size: 14px; color: #94a3b8; margin-top: 4px;")
        subtitle.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(subtitle)
        
        form_layout.addSpacing(32)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("👤  Username (min 3 chars)")
        self.username_input.setMinimumHeight(52)
        form_layout.addWidget(self.username_input)
        
        form_layout.addSpacing(14)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("🔒  Password (8+ chars, letters, numbers, special)")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(52)
        form_layout.addWidget(self.password_input)
        
        form_layout.addSpacing(14)
        
        # Confirm Password
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("🔐  Confirm Password")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setMinimumHeight(52)
        form_layout.addWidget(self.confirm_input)
        
        form_layout.addSpacing(24)
        
        # Register button (green theme)
        self.register_button = QPushButton("Create Account  →")
        self.register_button.setMinimumHeight(52)
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10b981, stop:1 #059669);
                font-size: 15px;
                font-weight: 700;
                border-radius: 12px;
                color: #ffffff;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #34d399, stop:1 #10b981);
            }
        """)
        self.register_button.clicked.connect(self.handle_register)
        form_layout.addWidget(self.register_button)
        
        form_layout.addSpacing(20)
        
        # Back to login
        back_label = QLabel("Already have an account?")
        back_label.setStyleSheet("font-size: 13px; color: #64748b;")
        back_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(back_label)
        
        back_button = QPushButton("Back to Login")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #6366f1;
                font-size: 14px;
                font-weight: 600;
                border: none;
                padding: 8px;
            }
            QPushButton:hover {
                color: #818cf8;
            }
        """)
        back_button.clicked.connect(self.reject)
        form_layout.addWidget(back_button)
        
        # Center form
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(form_wrapper)
        center_layout.addStretch()
        container_layout.addLayout(center_layout)
        
        container_layout.addStretch(2)
        
        scroll.setWidget(container)
        outer_layout.addWidget(scroll)
    
    def handle_register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()
        
        if not username or not password or not confirm:
            QMessageBox.warning(self, "Validation Error", "Please fill in all fields")
            return
        
        if len(username) < 3:
            QMessageBox.warning(self, "Validation Error", "Username must be at least 3 characters")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Validation Error", "Passwords do not match")
            return
        
        self.register_button.setEnabled(False)
        self.register_button.setText("Creating account...")
        QApplication.processEvents()
        
        success, result = self.api_client.register(username, password, confirm)
        
        if success:
            # Store credentials for auto-login
            self.registered_username = username
            self.registered_password = password
            self.accept()
        else:
            QMessageBox.critical(self, "Registration Failed", f"{result}")
            self.register_button.setEnabled(True)
            self.register_button.setText("Create Account  →")


# =============================================================================
# MATPLOTLIB CHARTS - Bar + Scatter
# =============================================================================

class BarChartCanvas(FigureCanvas):
    """Bar chart canvas for type distribution."""
    
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(8, 5), dpi=100, facecolor='#1e1b4b')
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setup_style()
    
    def setup_style(self):
        self.axes.set_facecolor('#0f172a')
        self.axes.tick_params(colors='#94a3b8', labelsize=10)
        self.axes.spines['bottom'].set_color('#334155')
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['left'].set_color('#334155')
        self.axes.spines['right'].set_visible(False)
        self.axes.xaxis.label.set_color('#e2e8f0')
        self.axes.yaxis.label.set_color('#e2e8f0')
        self.axes.title.set_color('#ffffff')
    
    def plot(self, type_distribution):
        self.axes.clear()
        self.setup_style()
        
        if not type_distribution:
            self.axes.text(0.5, 0.5, 'No data available', 
                          ha='center', va='center', color='#64748b', fontsize=14,
                          transform=self.axes.transAxes)
            self.axes.set_xticks([])
            self.axes.set_yticks([])
            self.draw()
            return
        
        types = list(type_distribution.keys())
        counts = list(type_distribution.values())
        colors = ['#8b5cf6', '#3b82f6', '#10b981', '#f97316', '#ec4899', '#eab308', '#06b6d4', '#f43f5e']
        
        x_pos = range(len(types))
        bars = self.axes.bar(x_pos, counts, color=colors[:len(types)], 
                            edgecolor='none', width=0.6)
        
        self.axes.set_xticks(x_pos)
        self.axes.set_xticklabels(types, fontsize=9, rotation=15, ha='right')
        self.axes.set_ylabel('Count', fontsize=11, fontweight='500')
        self.axes.set_title('Equipment Type Distribution', fontsize=15, fontweight='700', 
                           pad=15, color='#ffffff')
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            self.axes.annotate(f'{count}',
                              xy=(bar.get_x() + bar.get_width() / 2, height),
                              xytext=(0, 5),
                              textcoords="offset points",
                              ha='center', va='bottom', 
                              color='#ffffff', fontsize=12, fontweight='600')
        
        self.axes.yaxis.grid(True, linestyle='--', alpha=0.15, color='#475569')
        self.axes.set_axisbelow(True)
        
        self.fig.tight_layout(pad=1.5)
        self.draw()


class ScatterChartCanvas(FigureCanvas):
    """Scatter chart canvas for Temperature vs Pressure."""
    
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(8, 5), dpi=100, facecolor='#1e1b4b')
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setup_style()
    
    def setup_style(self):
        self.axes.set_facecolor('#0f172a')
        self.axes.tick_params(colors='#94a3b8', labelsize=10)
        self.axes.spines['bottom'].set_color('#334155')
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['left'].set_color('#334155')
        self.axes.spines['right'].set_visible(False)
        self.axes.xaxis.label.set_color('#e2e8f0')
        self.axes.yaxis.label.set_color('#e2e8f0')
        self.axes.title.set_color('#ffffff')
    
    def plot(self, equipment_data):
        self.axes.clear()
        self.setup_style()
        
        if not equipment_data:
            self.axes.text(0.5, 0.5, 'No data available', 
                          ha='center', va='center', color='#64748b', fontsize=14,
                          transform=self.axes.transAxes)
            self.axes.set_xticks([])
            self.axes.set_yticks([])
            self.draw()
            return
        
        temps = [item['temperature'] for item in equipment_data]
        pressures = [item['pressure'] for item in equipment_data]
        
        scatter = self.axes.scatter(temps, pressures, 
                                   c='#6366f1', s=120, alpha=0.8,
                                   edgecolors='#a5b4fc', linewidths=2)
        
        self.axes.set_xlabel('Temperature (°C)', fontsize=11, fontweight='500')
        self.axes.set_ylabel('Pressure (bar)', fontsize=11, fontweight='500')
        self.axes.set_title('Temperature vs Pressure', fontsize=15, fontweight='700', 
                           pad=15, color='#ffffff')
        
        self.axes.xaxis.grid(True, linestyle='--', alpha=0.15, color='#475569')
        self.axes.yaxis.grid(True, linestyle='--', alpha=0.15, color='#475569')
        self.axes.set_axisbelow(True)
        
        self.fig.tight_layout(pad=1.5)
        self.draw()


# =============================================================================
# STAT CARD WIDGET - Clean without dark box behind emoji
# =============================================================================

class StatCard(QFrame):
    """A clean stat card widget without background on emoji."""
    
    def __init__(self, title, value, color, icon_emoji="📊", parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.color = color
        self.setup_ui(title, value, icon_emoji)
    
    def setup_ui(self, title, value, icon_emoji):
        self.setMinimumHeight(110)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(6)
        
        # Icon (without background box - just the emoji)
        icon_label = QLabel(icon_emoji)
        icon_label.setStyleSheet(f"""
            font-size: 28px;
            background: transparent;
        """)
        layout.addWidget(icon_label)
        
        layout.addStretch()
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 12px;
            color: #94a3b8;
            font-weight: 500;
            background: transparent;
        """)
        layout.addWidget(title_label)
        
        # Value
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet(f"""
            font-size: 28px;
            font-weight: 700;
            color: {self.color};
            letter-spacing: -1px;
            background: transparent;
        """)
        layout.addWidget(self.value_label)
    
    def update_value(self, value):
        self.value_label.setText(str(value))


# =============================================================================
# MAIN WINDOW
# =============================================================================

class MainWindow(QMainWindow):
    """Main application window with modern UI."""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.equipment_data = []
        self.type_distribution = {}
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(32, 28, 32, 28)
        main_layout.setSpacing(24)
        
        # Header
        header = self.create_header()
        main_layout.addLayout(header)
        
        # Stats cards
        stats_layout = self.create_stats_cards()
        main_layout.addLayout(stats_layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs, 1)
        
        # Data tab
        data_tab = QWidget()
        data_layout = QVBoxLayout(data_tab)
        data_layout.setContentsMargins(16, 20, 16, 16)
        self.table = self.create_data_table()
        data_layout.addWidget(self.table)
        self.tabs.addTab(data_tab, "📊  Data Table")
        
        # Visuals tab - Now with TWO charts
        visuals_tab = QWidget()
        visuals_layout = QHBoxLayout(visuals_tab)
        visuals_layout.setContentsMargins(16, 20, 16, 16)
        visuals_layout.setSpacing(20)
        
        # Bar chart on left
        bar_container = QFrame()
        bar_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 12px;
            }
        """)
        bar_layout = QVBoxLayout(bar_container)
        bar_layout.setContentsMargins(12, 12, 12, 12)
        self.bar_chart = BarChartCanvas(bar_container)
        bar_layout.addWidget(self.bar_chart)
        visuals_layout.addWidget(bar_container)
        
        # Scatter chart on right
        scatter_container = QFrame()
        scatter_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 12px;
            }
        """)
        scatter_layout = QVBoxLayout(scatter_container)
        scatter_layout.setContentsMargins(12, 12, 12, 12)
        self.scatter_chart = ScatterChartCanvas(scatter_container)
        scatter_layout.addWidget(self.scatter_chart)
        visuals_layout.addWidget(scatter_container)
        
        self.tabs.addTab(visuals_tab, "📈  Visualizations")
    
    def create_header(self):
        header = QHBoxLayout()
        header.setSpacing(16)
        
        # Title section
        title_section = QVBoxLayout()
        title_section.setSpacing(4)
        
        title = QLabel("Chemical Equipment Visualizer")
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.5px;
            background: transparent;
        """)
        title_section.addWidget(title)
        
        subtitle = QLabel("Manage and analyze your equipment data")
        subtitle.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            background: transparent;
        """)
        title_section.addWidget(subtitle)
        
        header.addLayout(title_section)
        header.addStretch()
        
        # Buttons
        self.upload_btn = QPushButton("📤  Upload CSV")
        self.upload_btn.setObjectName("uploadBtn")
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.setMinimumWidth(160)
        self.upload_btn.clicked.connect(self.upload_csv)
        header.addWidget(self.upload_btn)
        
        self.pdf_btn = QPushButton("📄  Download PDF")
        self.pdf_btn.setObjectName("pdfBtn")
        self.pdf_btn.setCursor(Qt.PointingHandCursor)
        self.pdf_btn.setMinimumWidth(160)
        self.pdf_btn.clicked.connect(self.download_pdf)
        header.addWidget(self.pdf_btn)
        
        self.refresh_btn = QPushButton("🔄  Refresh")
        self.refresh_btn.setObjectName("refreshBtn")
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.setMinimumWidth(120)
        self.refresh_btn.clicked.connect(self.refresh_data)
        header.addWidget(self.refresh_btn)
        
        return header
    
    def create_stats_cards(self):
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        self.total_card = StatCard("Total Equipment", "0", "#a78bfa", "📦")
        self.flowrate_card = StatCard("Avg Flowrate", "0", "#60a5fa", "💧")
        self.pressure_card = StatCard("Avg Pressure", "0", "#6ee7b7", "⚡")
        self.temp_card = StatCard("Avg Temperature", "0", "#fb923c", "🌡️")
        
        stats_layout.addWidget(self.total_card)
        stats_layout.addWidget(self.flowrate_card)
        stats_layout.addWidget(self.pressure_card)
        stats_layout.addWidget(self.temp_card)
        
        return stats_layout
    
    def create_data_table(self):
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([
            "Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"
        ])
        
        # Fixed: Uniform column sizing
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        table.setAlternatingRowColors(True)
        table.setShowGrid(False)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSelectionMode(QTableWidget.SingleSelection)
        table.verticalHeader().setVisible(False)
        table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        
        # Set consistent row height
        table.verticalHeader().setDefaultSectionSize(52)
        
        return table
    
    def refresh_data(self):
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setText("Loading...")
        QApplication.processEvents()
        
        success, data = self.api_client.get_dashboard_stats()
        
        self.refresh_btn.setEnabled(True)
        self.refresh_btn.setText("🔄  Refresh")
        
        if not success:
            QMessageBox.critical(self, "Connection Error", 
                f"Failed to fetch data from server.\n\nPlease ensure the backend is running.")
            return
        
        # Update stats
        self.total_card.update_value(data.get('total_count', 0))
        avg_values = data.get('average_values', {})
        self.flowrate_card.update_value(round(avg_values.get('flowrate', 0), 1))
        self.pressure_card.update_value(round(avg_values.get('pressure', 0), 2))
        self.temp_card.update_value(round(avg_values.get('temperature', 0), 1))
        
        # Update table
        self.equipment_data = data.get('equipment_data', [])
        self.update_table()
        
        # Update charts (both bar and scatter)
        self.type_distribution = data.get('type_distribution', {})
        self.bar_chart.plot(self.type_distribution)
        self.scatter_chart.plot(self.equipment_data)
    
    def update_table(self):
        self.table.setRowCount(len(self.equipment_data))
        
        # Type colors for badges
        type_colors = {
            'reactor': '#a78bfa',
            'pump': '#60a5fa', 
            'heat exchanger': '#fb923c',
            'valve': '#6ee7b7',
            'tank': '#f472b6',
            'storage tank': '#818cf8',
            'compressor': '#fbbf24',
            'distillation column': '#fb7185',
            'mixer': '#34d399',
        }
        
        for row, item in enumerate(self.equipment_data):
            # Equipment Name
            name_item = QTableWidgetItem(item['equipment_name'])
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 0, name_item)
            
            # Type (with color)
            type_text = item['type']
            type_item = QTableWidgetItem(type_text)
            type_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            color = type_colors.get(type_text.lower(), '#94a3b8')
            type_item.setForeground(QColor(color))
            self.table.setItem(row, 1, type_item)
            
            # Numeric values
            for col, key in [(2, 'flowrate'), (3, 'pressure'), (4, 'temperature')]:
                value_item = QTableWidgetItem(f"{item[key]:.2f}")
                value_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.table.setItem(row, col, value_item)
    
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:
            return
        
        self.upload_btn.setEnabled(False)
        self.upload_btn.setText("Uploading...")
        QApplication.processEvents()
        
        success, result = self.api_client.upload_csv(file_path)
        
        self.upload_btn.setEnabled(True)
        self.upload_btn.setText("📤  Upload CSV")
        
        if success:
            QMessageBox.information(
                self, 
                "Upload Successful", 
                f"✅ Successfully uploaded {result.get('records_created', 0)} equipment records!"
            )
            self.refresh_data()
        else:
            QMessageBox.critical(self, "Upload Failed", f"Error uploading file:\n\n{result}")
    
    def download_pdf(self):
        if not self.equipment_data:
            QMessageBox.warning(self, "No Data", 
                "No equipment data available.\n\nPlease upload a CSV file first.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            "equipment_report.pdf",
            "PDF Files (*.pdf)"
        )
        
        if not file_path:
            return
        
        self.pdf_btn.setEnabled(False)
        self.pdf_btn.setText("Generating...")
        QApplication.processEvents()
        
        success, result = self.api_client.download_pdf()
        
        self.pdf_btn.setEnabled(True)
        self.pdf_btn.setText("📄  Download PDF")
        
        if success:
            with open(file_path, 'wb') as f:
                f.write(result)
            QMessageBox.information(self, "Report Generated", 
                f"✅ PDF report saved successfully!\n\n{file_path}")
        else:
            QMessageBox.critical(self, "Generation Failed", f"Failed to generate PDF:\n\n{result}")


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

def main():
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Prevent app from closing when switching windows
    
    # Set global font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    app.setStyle('Fusion')
    
    # Apply global stylesheet
    app.setStyleSheet(GLOBAL_STYLESHEET)
    
    # Set dark palette as fallback
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(15, 23, 42))
    palette.setColor(QPalette.WindowText, QColor(226, 232, 240))
    palette.setColor(QPalette.Base, QColor(30, 27, 75))
    palette.setColor(QPalette.AlternateBase, QColor(20, 18, 60))
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
