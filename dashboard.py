import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtGui import QPixmap, QIcon, QColor
from PyQt6.QtCore import Qt, QSize
from login import LoginApp  # Import the login page for logout functionality

class DashboardApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Purvaj Dashboard")
        self.setWindowIcon(QIcon("logo.png"))
        self.setFixedSize(730, 450)  # Default size to match login page
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMaximizeButtonHint)

        # Set the main window background color to --bg-color: #f8f9fa
        self.setStyleSheet("background-color: #f8f9fa;")

        # Reference sizes for scaling
        self.reference_width = 730  # Default window width for scaling
        self.reference_sidebar_width = 150  # Sidebar width at default size
        self.reference_icon_size = 16  # Default icon size (16x16)

        # Main layout (horizontal: sidebar + main content)
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Sidebar (left side)
        self.sidebar = QWidget(self)
        self.sidebar.setStyleSheet("background-color: #273027;")  # --sidebar-bg
        self.sidebar.setFixedWidth(self.reference_sidebar_width)
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)

        # Sidebar items (clickable buttons with icons)
        self.dashboard_label = QPushButton("Dashboard")
        self.dashboard_label.setIcon(QIcon("icons/speedometer2.svg"))  # Bootstrap Icon: bi-speedometer2
        self.dashboard_label.setIconSize(QSize(self.reference_icon_size, self.reference_icon_size))
        self.dashboard_label.setStyleSheet("font: 14px Helvetica; color: white; padding: 10px; border: none; background: rgba(255, 255, 255, 0.2); text-align: left;")  # --sidebar-text, --sidebar-active
        self.dashboard_label.clicked.connect(lambda: self.update_content("Dashboard"))
        self.sidebar_layout.addWidget(self.dashboard_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.qc_process_label = QPushButton("QC Process")
        self.qc_process_label.setIcon(QIcon("icons/gear.svg"))  # Bootstrap Icon: bi-gear
        self.qc_process_label.setIconSize(QSize(self.reference_icon_size, self.reference_icon_size))
        self.qc_process_label.setStyleSheet("font: 14px Helvetica; color: white; padding: 10px; border: none; background: transparent; text-align: left;")  # --sidebar-text
        self.qc_process_label.clicked.connect(lambda: self.update_content("QC Process"))
        self.sidebar_layout.addWidget(self.qc_process_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.reports_label = QPushButton("Reports")
        self.reports_label.setIcon(QIcon("icons/file-earmark-text.svg"))  # Bootstrap Icon: bi-file-earmark-text
        self.reports_label.setIconSize(QSize(self.reference_icon_size, self.reference_icon_size))
        self.reports_label.setStyleSheet("font: 14px Helvetica; color: white; padding: 10px; border: none; background: transparent; text-align: left;")  # --sidebar-text
        self.reports_label.clicked.connect(lambda: self.update_content("Reports"))
        self.sidebar_layout.addWidget(self.reports_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.settings_label = QPushButton("Settings")
        self.settings_label.setIcon(QIcon("icons/sliders.svg"))  # Bootstrap Icon: bi-sliders
        self.settings_label.setIconSize(QSize(self.reference_icon_size, self.reference_icon_size))
        self.settings_label.setStyleSheet("font: 14px Helvetica; color: white; padding: 10px; border: none; background: transparent; text-align: left;")  # --sidebar-text
        self.settings_label.clicked.connect(lambda: self.update_content("Settings"))
        self.sidebar_layout.addWidget(self.settings_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Spacer to push logout to the bottom
        self.sidebar_layout.addStretch()

        # Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.setIcon(QIcon("icons/logout.svg"))  # Bootstrap Icon: bi-box-arrow-right
        self.logout_button.setIconSize(QSize(self.reference_icon_size, self.reference_icon_size))
        self.logout_button.setStyleSheet("background-color: #4A704A; color: white; font: bold 12px Helvetica; border: none; padding: 5px; text-align: left;")  # --primary-color
        self.logout_button.clicked.connect(self.logout)
        self.sidebar_layout.addWidget(self.logout_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.sidebar)

        # Main content area (right side)
        self.content_area = QWidget(self)
        self.content_area.setStyleSheet("background-color: white;")  # --content-bg
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)

        # Add shadow to content area
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, int(0.05 * 255)))  # --content-shadow: rgba(0, 0, 0, 0.05)
        self.content_area.setGraphicsEffect(shadow)

        # Header in main content
        self.header_label = QLabel("Welcome to Purvaj Dashboard")
        self.header_label.setStyleSheet("font: bold 18px Helvetica; color: #4A704A; padding: 20px;")  # --page-title-color
        self.content_layout.addWidget(self.header_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Content area (updated dynamically)
        self.content_label = QLabel("This is the dashboard. Select an option from the sidebar to proceed.")
        self.content_label.setStyleSheet("font: 14px Helvetica; color: #333; padding: 20px;")  # --text-color
        self.content_layout.addWidget(self.content_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.content_layout.addStretch()  # Push content to the top

        self.main_layout.addWidget(self.content_area)

    def update_content(self, section):
        # Update the main content area based on the selected sidebar option
        self.header_label.setText(f"{section}")
        if section == "Dashboard":
            self.content_label.setText("This is the dashboard. Select an option from the sidebar to proceed.")
        elif section == "QC Process":
            self.content_label.setText("QC Process: Manage your quality control workflows here.")
        elif section == "Reports":
            self.content_label.setText("Reports: View and generate reports for your QC processes.")
        elif section == "Settings":
            self.content_label.setText("Settings: Adjust your preferences and account settings.")

        # Update sidebar styling to highlight the active section
        sections = {
            "Dashboard": self.dashboard_label,
            "QC Process": self.qc_process_label,
            "Reports": self.reports_label,
            "Settings": self.settings_label
        }
        for name, button in sections.items():
            if name == section:
                button.setStyleSheet(f"font: 14px Helvetica; color: white; padding: 10px; border: none; background: rgba(255, 255, 255, 0.2); text-align: left;")
            else:
                button.setStyleSheet(f"font: 14px Helvetica; color: white; padding: 10px; border: none; background: transparent; text-align: left;")

    def update_sizes(self, window_width):
        # Scale sidebar width based on window width
        scale_factor = window_width / self.reference_width
        new_sidebar_width = int(self.reference_sidebar_width * scale_factor)
        self.sidebar.setFixedWidth(new_sidebar_width)

        # Scale font sizes and icon sizes
        new_sidebar_font_size = max(10, int(14 * scale_factor))
        new_header_font_size = max(12, int(18 * scale_factor))
        new_content_font_size = max(10, int(14 * scale_factor))
        new_icon_size = max(12, int(self.reference_icon_size * scale_factor))

        # Update sidebar items
        sections = {
            "Dashboard": self.dashboard_label,
            "QC Process": self.qc_process_label,
            "Reports": self.reports_label,
            "Settings": self.settings_label
        }
        for name, button in sections.items():
            current_style = "rgba(255, 255, 255, 0.2)" if button.styleSheet().find("rgba(255, 255, 255, 0.2)") != -1 else "transparent"
            button.setStyleSheet(f"font: {new_sidebar_font_size}px Helvetica; color: white; padding: 10px; border: none; background: {current_style}; text-align: left;")
            button.setIconSize(QSize(new_icon_size, new_icon_size))

        self.logout_button.setStyleSheet(f"background-color: #4A704A; color: white; font: bold {new_sidebar_font_size}px Helvetica; border: none; padding: 5px; text-align: left;")
        self.logout_button.setIconSize(QSize(new_icon_size, new_icon_size))

        self.header_label.setStyleSheet(f"font: bold {new_header_font_size}px Helvetica; color: #4A704A; padding: 20px;")
        self.content_label.setStyleSheet(f"font: {new_content_font_size}px Helvetica; color: #333; padding: 20px;")

    def resizeEvent(self, event):
        window_width = event.size().width()
        window_height = event.size().height()

        # Update sizes of sidebar and content
        self.update_sizes(window_width)

        super().resizeEvent(event)

    def logout(self):
        # Close the dashboard and reopen the login page
        self.close()
        self.login_window = LoginApp()
        self.login_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())
