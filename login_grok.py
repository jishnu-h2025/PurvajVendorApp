import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Purvaj.com Login")
        self.root.state('zoomed')  # Set to full window (maximized)

        # Load background image
        self.original_image = Image.open("background.jpg")  # Replace with the actual path to the image
        self.bg_photo = ImageTk.PhotoImage(self.original_image)
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Bind resize event
        self.root.bind("<Configure>", self.resize_background)

        # Frame for login section (right side)
        login_frame = tk.Frame(root, bg="black", bd=0, relief="flat")
        login_frame.place(relx=0.85, rely=0.5, anchor="center", width=280, height=220)

        # Add a canvas for rounded rectangle effect (simulating semi-transparency)
        canvas = tk.Canvas(login_frame, bg="black", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=10, pady=10)
        # Draw a rounded rectangle (simulating semi-transparent background)
        self.create_rounded_rectangle(canvas, 5, 5, 275, 215, radius=20, fill="#444444", outline="#555555", width=2)

        # Login label
        login_label = tk.Label(login_frame, text="Login", font=("Helvetica", 18, "bold"), fg="#A9A9A9", bg="#444444")
        login_label.place(relx=0.5, rely=0.1, anchor="center")

        # Username field
        username_label = tk.Label(login_frame, text="Username", font=("Helvetica", 11), fg="#A9A9A9", bg="#444444")
        username_label.place(relx=0.5, rely=0.25, anchor="center")
        self.username_entry = tk.Entry(login_frame, font=("Helvetica", 12), width=22, bg="white", fg="black", insertbackground="black", relief="flat")
        self.username_entry.place(relx=0.5, rely=0.35, anchor="center")

        # Password field
        password_label = tk.Label(login_frame, text="Password", font=("Helvetica", 11), fg="#A9A9A9", bg="#444444")
        password_label.place(relx=0.5, rely=0.5, anchor="center")
        self.password_entry = tk.Entry(login_frame, font=("Helvetica", 12), show="*", width=22, bg="white", fg="black", insertbackground="black", relief="flat")
        self.password_entry.place(relx=0.5, rely=0.6, anchor="center")

        # Login button
        login_button = tk.Button(login_frame, text="Login", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", command=self.validate_login)
        login_button.place(relx=0.5, rely=0.75, anchor="center", width=100)

        # Bottom text
        bottom_text = tk.Label(login_frame, text='"Login for a Streamlined QC Process"', font=("Helvetica", 9, "italic"), fg="#A9A9A9", bg="#444444")
        bottom_text.place(relx=0.5, rely=0.9, anchor="center")

        # Center - Logo and Text
        logo_frame = tk.Frame(root, bg="black")
        logo_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Logo with transparent background
        try:
            logo_image = Image.open("logo.png")
            logo_image = logo_image.convert('RGBA')
            data = logo_image.getdata()
            new_data = [(R, G, B, 0) if (R, G, B) == (255, 255, 255) else (R, G, B, A) for (R, G, B, A) in data]
            logo_image.putdata(new_data)
            logo_image = logo_image.resize((150, 50), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(logo_frame, image=self.logo_photo, bg="black")
            logo_label.pack()
        except:
            logo_label = tk.Label(logo_frame, text="PURVAJ.com", font=("Helvetica", 20, "bold"), fg="#FF4500", bg="black")
            logo_label.pack()

        # Slogan text
        slogan_text = tk.Label(logo_frame, text="Connecting the dots", font=("Helvetica", 10), fg="#A9A9A9", bg="black")
        slogan_text.pack()

        # Main text
        main_text = tk.Label(logo_frame, text="Streamlined QC Process", font=("Helvetica", 14, "bold"), fg="white", bg="black")
        main_text.pack(pady=10)

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        """Draw a rounded rectangle on the canvas."""
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1
        ]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def resize_background(self, event):
        new_width = event.width
        new_height = event.height
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized_image)
        self.bg_label.configure(image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="your_username",
                password="your_password",
                database="purvaj_db"
            )
            cursor = connection.cursor()
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