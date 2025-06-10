import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Purvaj.com Login")
        self.root.geometry("800x450")
        
        # Load background image (replace 'background.jpg' with the actual image path)
        try:
            bg_image = Image.open("background.jpg")
            bg_image = bg_image.resize((800, 450), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            # Fallback if image not found
            bg_label = tk.Label(root, bg="#2E2E2E")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame for login section (right side)
        login_frame = tk.Frame(root, bg="#333333", bd=0)
        login_frame.place(relx=0.65, rely=0.5, anchor="center", width=250, height=200)

        # Login label
        login_label = tk.Label(login_frame, text="Login", font=("Helvetica", 16, "bold"), fg="#A9A9A9", bg="#333333")
        login_label.pack(pady=10)

        # Username field
        username_label = tk.Label(login_frame, text="Username", font=("Helvetica", 10), fg="#A9A9A9", bg="#333333")
        username_label.pack()
        self.username_entry = tk.Entry(login_frame, font=("Helvetica", 12), width=20)
        self.username_entry.pack(pady=5)

        # Password field
        password_label = tk.Label(login_frame, text="Password", font=("Helvetica", 10), fg="#A9A9A9", bg="#333333")
        password_label.pack()
        self.password_entry = tk.Entry(login_frame, font=("Helvetica", 12), show="*", width=20)
        self.password_entry.pack(pady=5)

        # Login button
        login_button = tk.Button(login_frame, text="Login", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=self.validate_login)
        login_button.pack(pady=10)

        # Bottom text
        bottom_text = tk.Label(login_frame, text='"Login for a Streamlined QC Process"', font=("Helvetica", 8, "italic"), fg="#A9A9A9", bg="#333333")
        bottom_text.pack()

        # Left side - Logo and Text
        logo_frame = tk.Frame(root)
        logo_frame.place(relx=0.35, rely=0.5, anchor="center")

        # Placeholder for logo (replace with actual logo image)
        try:
            logo_image = Image.open("logo.png")
            logo_image = logo_image.resize((150, 50), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(logo_frame, image=self.logo_photo)
            logo_label.pack()
        except:
            # Fallback if logo not found
            logo_label = tk.Label(logo_frame, text="PURVAJ.com", font=("Helvetica", 20, "bold"), fg="#FF4500")
            logo_label.pack()

        # Slogan text
        slogan_text = tk.Label(logo_frame, text="Connecting the dots", font=("Helvetica", 10), fg="#A9A9A9")
        slogan_text.pack()

        # Main text
        main_text = tk.Label(logo_frame, text="Streamlined QC Process", font=("Helvetica", 14, "bold"), fg="white")
        main_text.pack(pady=10)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            # Connect to MySQL
            connection = mysql.connector.connect(
                host="localhost",
                user="your_username",  # Replace with your MySQL username
                password="your_password",  # Replace with your MySQL password
                database="purvaj_db"  # Replace with your database name
            )
            cursor = connection.cursor()

            # Query to check credentials
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                messagebox.showinfo("Success", "Login Successful!")
            else:
                messagebox.showerror("Error", "Invalid Username or Password")

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()