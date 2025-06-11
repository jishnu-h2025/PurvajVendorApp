from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                            QFrame, QSpacerItem, QSizePolicy)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt

class Sidebar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(250)
        self.setStyleSheet("""
            background-color: #2c3e50;
            padding: 20px;
        """)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo
        logo = QLabel("PURVAJ_Lean")
        logo.setStyleSheet("""
            color: #3498db;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 5px;
        """)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)
        
        # System Name
        system_name = QLabel("Purvaj QC System")
        system_name.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 3px;
        """)
        system_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(system_name)
        
        # System Description
        system_desc = QLabel("Streamlined QC Process")
        system_desc.setStyleSheet("""
            color: #bdc3c7;
            font-size: 12px;
            margin-bottom: 30px;
        """)
        system_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(system_desc)
        
        # User Info Container
        user_container = QFrame()
        user_container.setStyleSheet("""
            background-color: #34495e;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 30px;
        """)
        
        user_layout = QVBoxLayout()
        user_layout.setSpacing(5)
        
        # User Name
        user_name = QLabel("VINAY SINGH")
        user_name.setStyleSheet("""
            color: white;
            font-size: 14px;
            font-weight: bold;
        """)
        user_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_layout.addWidget(user_name)
        
        # User Role
        user_role = QLabel("Upload User")
        user_role.setStyleSheet("""
            color: #bdc3c7;
            font-size: 12px;
        """)
        user_role.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_layout.addWidget(user_role)
        
        user_container.setLayout(user_layout)
        layout.addWidget(user_container)
        
        # Navigation Buttons
        buttons = [
            ("Logout", "#e74c3c"),
            ("New Upload", "#3498db"),
            ("My Uploads", "#3498db"), 
            ("Re-upload", "#3498db")
        ]
        
        for text, color in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    padding: 10px 15px;
                    text-align: left;
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 4px;
                    margin-bottom: 10px;
                }}
                QPushButton:hover {{
                    background-color: #2980b9;
                }}
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            layout.addWidget(btn)
        
        # Spacer to push version info to bottom
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Version Info
        version = QLabel("v2.0")
        version.setStyleSheet("""
            color: #7f8c8d;
            font-size: 10px;
            margin-bottom: 5px;
        """)
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)
        
        # Copyright
        copyright = QLabel("© 2025 Purvaj QC System. All Rights Reserved")
        copyright.setStyleSheet("""
            color: #7f8c8d;
            font-size: 10px;
        """)
        copyright.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright)
        
        self.setLayout(layout)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = Sidebar()
    window.show()
    sys.exit(app.exec())