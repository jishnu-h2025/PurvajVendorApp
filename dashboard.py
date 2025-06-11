import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, 
    QGraphicsDropShadowEffect, QFrame, QFileDialog, QComboBox, QMessageBox
)
from PyQt6.QtGui import QPixmap, QIcon, QColor
from PyQt6.QtCore import Qt, QSize
from login import LoginApp
import os

class DashboardApp(QWidget):
    def __init__(self, username="User"):
        super().__init__()
        self.username = username
        self.setWindowTitle("Purvaj Dashboard")
        self.setWindowIcon(QIcon("window_logo.png"))
        self.setFixedSize(977, 596)

        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMaximizeButtonHint)

        # Set the background to an urban rooftop at night
        self.setStyleSheet("background-image: url('urban_rooftop_night.png'); background-repeat: no-repeat; background-position: center; background-size: cover;")

        self.reference_width = 730
        self.reference_sidebar_width = 150
        self.reference_icon_size = 16
        self.reference_logo_width = 120
        self.reference_footer_width = 120

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.sidebar = QWidget(self)
        self.sidebar.setStyleSheet("background-color: #273027;")
        self.sidebar.setFixedWidth(self.reference_sidebar_width)
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)

        self.logo_label = QLabel(self)
        self.update_logo_size(self.reference_width)
        self.sidebar_layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.user_label = QLabel(f"Logged as: \n\n {self.username}")
        self.user_label.setStyleSheet("font: 11px Helvetica; color: rgba(255, 255, 255, 0.7); padding: 4px;")
        self.sidebar_layout.addWidget(self.user_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.divider0 = QFrame()
        self.divider0.setFrameShape(QFrame.Shape.HLine)
        self.divider0.setStyleSheet("background-color: #dee2e6; margin: 5px 10px;")
        self.divider0.setFixedHeight(1)
        self.sidebar_layout.addWidget(self.divider0)

        self.divider_style = "background-color: rgba(255, 255, 255, 0.1); margin: 5px 10px;"

        self.new_upload_label = QPushButton("New Upload")
        self.new_upload_label.setIcon(QIcon("icons/speedometer2.svg"))
        self.new_upload_label.setIconSize(QSize(self.reference_icon_size, self.reference_icon_size))
        self.new_upload_label.setStyleSheet("font: 12px Helvetica; color: white; padding: 8px; border: none; background: rgba(255, 255, 255, 0.2); text-align: left;")
        self.new_upload_label.clicked.connect(lambda: self.update_content("New Upload"))
        self.sidebar_layout.addWidget(self.new_upload_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.divider1 = QFrame()
        self.divider1.setFrameShape(QFrame.Shape.HLine)
        self.divider1.setStyleSheet(self.divider_style)
        self.divider1.setFixedHeight(1)
        self.sidebar_layout.addWidget(self.divider1)

        self.my_uploads_label = QPushButton("My Uploads")
        self.my_uploads_label.setIcon(QIcon("icons/gear.svg"))
        self.my_uploads_label.setIconSize(QSize(self.reference_icon_size, self.reference_icon_size))
        self.my_uploads_label.setStyleSheet("font: 12px Helvetica; color: white; padding: 8px; border: none; background: transparent; text-align: left;")
        self.my_uploads_label.clicked.connect(lambda: self.update_content("My Uploads"))
        self.sidebar_layout.addWidget(self.my_uploads_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.divider2 = QFrame()
        self.divider2.setFrameShape(QFrame.Shape.HLine)
        self.divider2.setStyleSheet(self.divider_style)
        self.divider2.setFixedHeight(1)
        self.sidebar_layout.addWidget(self.divider2)

        self.reuploads_label = QPushButton("Re-Uploads")
        self.reuploads_label.setIcon(QIcon("icons/file-earmark-text.svg"))
        self.reuploads_label.setIconSize(QSize(self.reference_icon_size, self.reference_icon_size))
        self.reuploads_label.setStyleSheet("font: 12px Helvetica; color: white; padding: 8px; border: none; background: transparent; text-align: left;")
        self.reuploads_label.clicked.connect(lambda: self.update_content("Re-Uploads"))
        self.sidebar_layout.addWidget(self.reuploads_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.divider3 = QFrame()
        self.divider3.setFrameShape(QFrame.Shape.HLine)
        self.divider3.setStyleSheet(self.divider_style)
        self.divider3.setFixedHeight(1)
        self.sidebar_layout.addWidget(self.divider3)

        self.settings_label = QPushButton("Settings")
        self.settings_label.setIcon(QIcon("icons/sliders.svg"))
        self.settings_label.setIconSize(QSize(self.reference_icon_size, self.reference_icon_size))
        self.settings_label.setStyleSheet("font: 12px Helvetica; color: white; padding: 8px; border: none; background: transparent; text-align: left;")
        self.settings_label.clicked.connect(lambda: self.update_content("Settings"))
        self.sidebar_layout.addWidget(self.settings_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.divider4 = QFrame()
        self.divider4.setFrameShape(QFrame.Shape.HLine)
        self.divider4.setStyleSheet(self.divider_style)
        self.divider4.setFixedHeight(1)
        self.sidebar_layout.addWidget(self.divider4)

        self.sidebar_layout.addStretch()

        self.logout_button = QPushButton("Logout")
        self.logout_button.setIcon(QIcon("icons/logout.svg"))
        self.logout_button.setIconSize(QSize(self.reference_icon_size, self.reference_icon_size))
        self.logout_button.setStyleSheet("background-color: #4A704A; color: white; font: bold 11px Helvetica; border: none; padding: 4px; text-align: left;")
        self.logout_button.clicked.connect(self.logout)
        self.sidebar_layout.addWidget(self.logout_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.footer_label = QLabel(self)
        self.update_footer_size(self.reference_width)
        self.sidebar_layout.addWidget(self.footer_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.sidebar)

        self.content_area = QWidget(self)
        self.content_area.setStyleSheet("background-color: rgba(255, 255, 255, 0.95);")
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, int(0.1 * 255)))
        self.content_area.setGraphicsEffect(shadow)

        self.header_label = QLabel("Welcome to Purvaj Dashboard")
        self.header_label.setStyleSheet("font: bold 18px Helvetica; color: #4A704A; padding: 20px;")
        self.content_layout.addWidget(self.header_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.content_widget = QWidget()
        self.content_widget_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_widget_layout)
        self.content_layout.addWidget(self.content_widget)

        self.content_layout.addStretch()

        self.main_layout.addWidget(self.content_area)

        self.update_content("New Upload")

    def update_logo_size(self, window_width):
        scale_factor = window_width / self.reference_width
        new_logo_width = int(self.reference_logo_width * scale_factor)
        new_logo_height = int(new_logo_width * (75 / 300))
        logo_pixmap = QPixmap("logo.png").scaled(new_logo_width, new_logo_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo_label.setPixmap(logo_pixmap)

    def update_footer_size(self, window_width):
        scale_factor = window_width / self.reference_width
        new_footer_width = int(self.reference_footer_width * scale_factor)
        new_footer_height = int(new_footer_width * (50 / 120))
        footer_pixmap = QPixmap("footer.png").scaled(new_footer_width, new_footer_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.footer_label.setPixmap(footer_pixmap)

    def create_new_upload_content(self):
        while self.content_widget_layout.count():
            item = self.content_widget_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Form container
        form_container = QWidget()
        form_container.setStyleSheet("background-color: #F5F7FA; border-radius: 10px; padding: 20px;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, int(0.05 * 255)))
        form_container.setGraphicsEffect(shadow)
        form_layout = QVBoxLayout()
        form_container.setLayout(form_layout)

        # Upload Option Drop-down
        upload_option_layout = QHBoxLayout()
        upload_option_label = QLabel("Upload Option:")
        upload_option_label.setStyleSheet("font: 12px Helvetica; color: #333;")
        upload_option_layout.addWidget(upload_option_label)

        self.upload_option_combo = QComboBox()
        self.upload_option_combo.addItems(["Complete", "Partial"])
        self.upload_option_combo.setStyleSheet("background-color: #FFFFFF; border: 1px solid #CED4DA; border-radius: 5px; padding: 5px; font: 12px Helvetica; color: #333;")
        self.upload_option_combo.setFixedWidth(200)
        upload_option_layout.addWidget(self.upload_option_combo)
        upload_option_layout.addStretch()
        form_layout.addLayout(upload_option_layout)

        # Priority Drop-down
        priority_layout = QHBoxLayout()
        priority_label = QLabel("Priority:")
        priority_label.setStyleSheet("font: 12px Helvetica; color: #333;")
        priority_layout.addWidget(priority_label)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Normal", "High"])
        self.priority_combo.setStyleSheet("background-color: #FFFFFF; border: 1px solid #CED4DA; border-radius: 5px; padding: 5px; font: 12px Helvetica; color: #333;")
        self.priority_combo.setFixedWidth(200)
        priority_layout.addWidget(self.priority_combo)
        priority_layout.addStretch()
        form_layout.addLayout(priority_layout)

        # Browse Folder
        browse_layout = QHBoxLayout()
        browse_label = QLabel("Select Folder:")
        browse_label.setStyleSheet("font: 12px Helvetica; color: #333;")
        browse_layout.addWidget(browse_label)

        self.folder_path_label = QLabel("No folder selected")
        self.folder_path_label.setStyleSheet("font: 12px Helvetica; color: #666;")
        browse_layout.addWidget(self.folder_path_label)

        browse_button = QPushButton("Browse Folder")
        browse_button.setStyleSheet("""
            background-color: #4A704A; 
            color: white; 
            font: 12px Helvetica; 
            border: none; 
            padding: 5px 10px; 
            border-radius: 5px;
            """
        )
        browse_button.clicked.connect(self.browse_folder)
        browse_layout.addWidget(browse_button)
        browse_layout.addStretch()
        form_layout.addLayout(browse_layout)

        # Buttons (Reset and Submit)
        button_layout = QHBoxLayout()
        reset_button = QPushButton("Reset Form")
        reset_button.setStyleSheet("""
            background-color: #6C757D; 
            color: white; 
            font: 12px Helvetica; 
            border: none; 
            padding: 5px 10px; 
            border-radius: 5px;
            """
        )
        reset_button.clicked.connect(self.reset_form)
        button_layout.addWidget(reset_button)

        submit_button = QPushButton("Submit")
        submit_button.setStyleSheet("""
            background-color: #007BFF; 
            color: white; 
            font: bold 12px Helvetica; 
            border: none; 
            padding: 5px 10px; 
            border-radius: 5px;
            """
        )
        submit_button.clicked.connect(self.submit_form)
        button_layout.addWidget(submit_button)
        button_layout.addStretch()
        form_layout.addLayout(button_layout)

        self.content_widget_layout.addWidget(form_container)
        self.content_widget_layout.addStretch()

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_path_label.setText(folder_path)

    def reset_form(self):
        self.upload_option_combo.setCurrentIndex(0)
        self.priority_combo.setCurrentIndex(0)
        self.folder_path_label.setText("No folder selected")

    def submit_form(self):
        folder_path = self.folder_path_label.text()
        upload_option = self.upload_option_combo.currentText()
        priority = self.priority_combo.currentText()

        if folder_path == "No folder selected":
            QMessageBox.critical(self, "Error", "Please select a folder to upload.")
            return

        # Validate folder contents (only .jpg and .png files)
        try:
            files = os.listdir(folder_path)
            if not files:
                QMessageBox.critical(self, "Error", "The selected folder is empty.")
                return
            for file_name in files:
                if not (file_name.lower().endswith('.jpg') or file_name.lower().endswith('.png')):
                    QMessageBox.critical(self, "Error", "The folder contains unsupported files. Only .jpg and .png files are allowed.")
                    return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to access the folder: {str(e)}")
            return

        QMessageBox.information(self, "Success", f"Folder uploaded successfully!\n\nFolder: {folder_path}\nUpload Option: {upload_option}\nPriority: {priority}")
        self.reset_form()

    def update_content(self, section):
        self.header_label.setText(f"{section}")
        if section == "New Upload":
            self.create_new_upload_content()
        else:
            while self.content_widget_layout.count():
                item = self.content_widget_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            content_label = QLabel(self.get_content_text(section))
            content_label.setStyleSheet("font: 14px Helvetica; color: #333; padding: 20px;")
            self.content_widget_layout.addWidget(content_label)
            self.content_widget_layout.addStretch()

        sections = {
            "New Upload": self.new_upload_label,
            "My Uploads": self.my_uploads_label,
            "Re-Uploads": self.reuploads_label,
            "Settings": self.settings_label
        }
        for name, button in sections.items():
            if name == section:
                button.setStyleSheet(f"font: 14px Helvetica; color: white; padding: 10px; border: none; background: rgba(255, 255, 255, 0.2); text-align: left;")
            else:
                button.setStyleSheet(f"font: 14px Helvetica; color: white; padding: 10px; border: none; background: transparent; text-align: left;")

    def get_content_text(self, section):
        if section == "My Uploads":
            return "My Uploads: Manage your quality control workflows here."
        elif section == "Re-Uploads":
            return "Re-Uploads: View and generate reports for your QC processes."
        elif section == "Settings":
            return "Settings: Adjust your preferences and account settings."
        return "Select an option from the sidebar to proceed."

    def update_sizes(self, window_width):
        scale_factor = window_width / self.reference_width
        new_sidebar_width = int(self.reference_sidebar_width * scale_factor)
        self.sidebar.setFixedWidth(new_sidebar_width)

        new_sidebar_font_size = max(9, int(12 * scale_factor))
        new_header_font_size = max(12, int(18 * scale_factor))
        new_content_font_size = max(10, int(14 * scale_factor))
        new_icon_size = max(12, int(self.reference_icon_size * scale_factor))

        self.update_logo_size(window_width)
        self.update_footer_size(window_width)

        self.user_label.setStyleSheet(f"font: {new_sidebar_font_size}px Helvetica; color: rgba(255, 255, 255, 0.7); padding: 4px;")

        sections = {
            "New Upload": self.new_upload_label,
            "My Uploads": self.my_uploads_label,
            "Re-Uploads": self.reuploads_label,
            "Settings": self.settings_label
        }
        for name, button in sections.items():
            current_style = "rgba(255, 255, 255, 0.2)" if button.styleSheet().find("rgba(255, 255, 255, 0.2)") != -1 else "transparent"
            button.setStyleSheet(f"font: {new_sidebar_font_size}px Helvetica; color: white; padding: 8px; border: none; background: {current_style}; text-align: left;")
            button.setIconSize(QSize(new_icon_size, new_icon_size))

        self.logout_button.setStyleSheet(f"background-color: #4A704A; color: white; font: bold {new_sidebar_font_size}px Helvetica; border: none; padding: 4px; text-align: left;")
        self.logout_button.setIconSize(QSize(new_icon_size, new_icon_size))

        new_margin = int(5 * scale_factor)
        new_side_margin = int(10 * scale_factor)
        divider_style = f"background-color: rgba(255, 255, 255, 0.1); margin: {new_margin}px {new_side_margin}px;"
        self.divider0.setStyleSheet(f"background-color: #dee2e6; margin: {new_margin}px {new_side_margin}px;")
        self.divider1.setStyleSheet(divider_style)
        self.divider2.setStyleSheet(divider_style)
        self.divider3.setStyleSheet(divider_style)
        self.divider4.setStyleSheet(divider_style)

        self.header_label.setStyleSheet(f"font: bold {new_header_font_size}px Helvetica; color: #4A704A; padding: 20px;")

    def resizeEvent(self, event):
        window_width = event.size().width()
        window_height = event.size().height()
        self.update_sizes(window_width)
        super().resizeEvent(event)

    def logout(self):
        self.close()
        self.login_window = LoginApp()
        self.login_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())