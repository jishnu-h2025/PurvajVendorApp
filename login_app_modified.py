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

        # Frame for login section (right side) with styling from image.png
        login_frame = tk.Frame(root, bg="#333333", bd=0, relief="flat")
        login_frame.place(relx=0.675, rely=0.5, anchor="center", width=280, height=220)  # Moved right by ~2% of window width

        # Add a canvas for shadow effect
        canvas = tk.Canvas(login_frame, bg="#333333", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=10, pady=10)
        canvas.create_rectangle(5, 5, 275, 215, fill="#333333", outline="#444444", width=2)

        # Login label
        login_label = tk.Label(login_frame, text="Login", font=("Helvetica", 18, "bold"), fg="#A9A9A9", bg="#333333")
        login_label.place(relx=0.5, rely=0.1, anchor="center")

        # Username field
        username_label = tk.Label(login_frame, text="Username", font=("Helvetica", 11), fg="#A9A9A9", bg="#333333")
        username_label.place(relx=0.5, rely=0.25, anchor="center")
        self.username_entry = tk.Entry(login_frame, font=("Helvetica", 12), width=22, bg="white", fg="black", insertbackground="black", relief="flat")
        self.username_entry.place(relx=0.5, rely=0.35, anchor="center")

        # Password field
        password_label = tk.Label(login_frame, text="Password", font=("Helvetica", 11), fg="#A9A9A9", bg="#333333")
        password_label.place(relx=0.5, rely=0.5, anchor="center")
        self.password_entry = tk.Entry(login_frame, font=("Helvetica", 12), show="*", width=22, bg="white", fg="black", insertbackground="black", relief="flat")
        self.password_entry.place(relx=0.5, rely=0.6, anchor="center")

        # Login button
        login_button = tk.Button(login_frame, text="Login", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", command=self.validate_login)
        login_button.place(relx=0.5, rely=0.75, anchor="center", width=100)

        # Bottom text
        bottom_text = tk.Label(login_frame, text='"Login for a Streamlined QC Process"', font=("Helvetica", 9, "italic"), fg="#A9A9A9", bg="#333333")
        bottom_text.place(relx=0.5, rely=0.9, anchor="center")

        # Left side - Logo and Text
        logo_frame = tk.Frame(root)
        logo_frame.place(relx=0.375, rely=0.5, anchor="center")  # Moved right by ~2% of window width

        # Placeholder for logo (replace with actual logo image)
        try:
            logo_image = Image.open("logo.png")
            logo_image = logo_image.convert('RGBA')  # Convert to RGBA mode
            data = logo_image.getdata()
            new_data = [(R, G, B, 0) if (R, G, B) == (255, 255, 255) else (R, G, B, A) for (R, G, B, A) in data]  # Make white background transparent
            logo_image.putdata(new_data)
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

    def resize_background(self, event):
        # Resize the background image when the window is resized
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