import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtCore import Qt
import mysql.connector
from PIL import Image
import io
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Purvaj.com Login")
        self.setWindowIcon(QIcon("window_logo.png"))
        # self.setFixedSize(730, 450)  # Default size
        self.setFixedSize(977,596)  # Default size

        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMaximizeButtonHint)

        # Reference sizes for scaling
        self.reference_width = 1920  # Reference width for full-screen (when logo is 300x75)
        self.reference_logo_width = 300  # Logo width at full-screen
        self.reference_login_width = 280  # Login box width at default size (730px)
        self.reference_login_height = 220  # Login box height at default size

        # Background image
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap("background.jpg").scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding))
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.lower()

        # Right side - Login Frame
        self.login_frame = QWidget(self)
        self.login_frame.setStyleSheet("""
            background-color: rgba(0,0,0,0.3); 
            border-radius: 10px;
        """)
        self.login_frame.setFixedSize(self.reference_login_width, self.reference_login_height)
        self.login_frame.move(int(self.width() * 0.85 - self.reference_login_width // 2), self.height() // 2 - self.reference_login_height // 2)

        self.login_layout = QVBoxLayout()
        self.login_layout.setSpacing(10)  # Adjust spacing between elements to match screenshot
        self.login_frame.setLayout(self.login_layout)

        # Login label
        self.login_label = QLabel("Login")
        self.login_label.setStyleSheet("font: bold 18px Helvetica; color: #A9A9A9;")
        self.login_layout.addWidget(self.login_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Username field
        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("Username")  # Match screenshot
        self.username_entry.setFixedWidth(200)
        self.username_entry.setStyleSheet("background-color: #D3D3D3; color: black; border: none; padding: 5px;")
        self.login_layout.addWidget(self.username_entry, alignment=Qt.AlignmentFlag.AlignCenter)

        # Password field
        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("•••••")  # Indicate password field, match screenshot
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_entry.setFixedWidth(200)
        self.password_entry.setStyleSheet("background-color: #D3D3D3; color: black; border: none; padding: 5px;")
        self.login_layout.addWidget(self.password_entry, alignment=Qt.AlignmentFlag.AlignCenter)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setFixedWidth(100)
        self.login_button.setStyleSheet("background-color: #4CAF50; color: white; font: bold 12px Helvetica; border: none; padding: 5px;")
        self.login_button.clicked.connect(self.validate_login)
        self.login_layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Bottom text
        self.bottom_text = QLabel('"Login for a Streamlined QC Process"')
        self.bottom_text.setStyleSheet("font: italic 9px Helvetica; color: #A9A9A9;")
        self.login_layout.addWidget(self.bottom_text, alignment=Qt.AlignmentFlag.AlignCenter)

        # Center - Logo and Text
        self.logo_container = QWidget(self)
        self.logo_container.setStyleSheet("background-color: transparent;")
        self.logo_layout = QVBoxLayout()
        self.logo_container.setLayout(self.logo_layout)

        # Logo (initially set to scale based on default window size)
        self.logo_label = QLabel()
        self.update_logo_size(self.width())
        self.logo_layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Main text
        self.main_text = QLabel("Streamlined QC Process")
        self.main_text.setStyleSheet("font: bold 16px Helvetica; color: #ffffff;")
        self.logo_layout.addWidget(self.main_text, alignment=Qt.AlignmentFlag.AlignCenter)

        # Position the logo container in the center
        self.logo_container.adjustSize()
        self.logo_container.move(self.width() // 2 - self.logo_container.width() // 2, self.height() // 2 - self.logo_container.height() // 2)

    def update_logo_size(self, window_width):
        # Scale logo size based on window width
        scale_factor = window_width / self.reference_width
        new_logo_width = int(self.reference_logo_width * scale_factor)
        new_logo_height = int(new_logo_width * (75 / 300))  # Maintain 4:1 aspect ratio

        try:
            logo_image = Image.open("logo.png").convert('RGBA')
            data = logo_image.getdata()
            new_data = [(r, g, b, 0) if (r, g, b) == (255, 255, 255) else (r, g, b, a) for (r, g, b, a) in data]
            logo_image.putdata(new_data)

            # Resize logo to new dimensions
            logo_image = logo_image.resize((new_logo_width, new_logo_height), Image.Resampling.LANCZOS)

            buffer = io.BytesIO()
            logo_image.save(buffer, format="PNG")
            qimage = QImage.fromData(buffer.getvalue())
            logo_pixmap = QPixmap.fromImage(qimage)
            self.logo_label.setPixmap(logo_pixmap)
        except FileNotFoundError:
            self.logo_label.setText("PURVAJ.com")
            self.logo_label.setStyleSheet("font: bold 20px Helvetica; color: #FF4500;")

    def update_login_box_size(self, window_width, window_height):
        # Scale login box size based on window width
        scale_factor = window_width / 730  # Default window width
        new_login_width = int(self.reference_login_width * scale_factor)
        new_login_height = int(self.reference_login_height * scale_factor)

        # Update login frame size
        self.login_frame.setFixedSize(new_login_width, new_login_height)

        # Scale font sizes and widget sizes inside the login box
        new_font_size = max(10, int(18 * scale_factor))  # Login label font size (min 10px)
        new_input_width = int(200 * scale_factor)  # Input field width
        new_button_width = int(100 * scale_factor)  # Button width
        new_bottom_font_size = max(6, int(9 * scale_factor))  # Bottom text font size (min 6px)

        self.login_label.setStyleSheet(f"font: bold {new_font_size}px Helvetica; color: #A9A9A9;")
        self.username_entry.setFixedWidth(new_input_width)
        self.password_entry.setFixedWidth(new_input_width)
        self.login_button.setFixedWidth(new_button_width)
        self.bottom_text.setStyleSheet(f"font: italic {new_bottom_font_size}px Helvetica; color: #A9A9A9;")

        # Reposition login frame
        self.login_frame.move(int(window_width * 0.85 - new_login_width // 2), window_height // 2 - new_login_height // 2)

    def resizeEvent(self, event):
        window_width = event.size().width()
        window_height = event.size().height()

        # Resize background image to cover the entire window
        self.bg_label.setPixmap(QPixmap("background.jpg").scaled(event.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding))
        self.bg_label.setGeometry(0, 0, window_width, window_height)

        # Update logo size
        self.update_logo_size(window_width)

        # Update login box size
        self.update_login_box_size(window_width, window_height)

        # Reposition logo container
        self.logo_container.adjustSize()
        self.logo_container.move(window_width // 2 - self.logo_container.width() // 2, window_height // 2 - self.logo_container.height() // 2)

        super().resizeEvent(event)

    def validate_login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        
        print(os.getenv("user"))
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user=os.getenv("user"),
                password=os.getenv("password"),
                database=os.getenv("database")
            )
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            Uploader_Name = None
            if result:
                # Assuming the columns are (id, username, password, name, ...)
                Uploader_Name = result[2]  # Adjust index if 'name' is at a different position
            if result:
                # On successful login, close the login window and open the dashboard
                from dashboard import DashboardApp  # Import here to avoid circular import
                self.close()
                self.dashboard = DashboardApp(Uploader_Name)
                self.dashboard.show()
            else:
                QMessageBox.critical(self, "Error", "Invalid Username or Password")

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec())