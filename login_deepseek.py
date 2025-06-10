import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk, ImageOps

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Purvaj.com Login")
        self.root.state('zoomed')  # Set to full window (maximized)

        # Create a canvas for the background
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill="both", expand=True)

        # Load and set background image
        self.original_bg = Image.open("background.jpg")  # Replace with your background image
        self.bg_photo = ImageTk.PhotoImage(self.original_bg)
        self.bg_canvas = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Bind resize event
        self.root.bind("<Configure>", self.resize_background)

        # Create a rounded rectangle frame for login (right side)
        self.login_frame = tk.Canvas(self.canvas, bg="#333333", bd=0, highlightthickness=0, width=300, height=350)
        self.login_frame.place(relx=0.75, rely=0.5, anchor="center")

        # Draw rounded rectangle with semi-transparent background
        self.login_frame.create_round_rect(0, 0, 300, 350, radius=20, fill="#333333", alpha=0.8)

        # Login label
        login_label = tk.Label(self.login_frame, text="Login", font=("Helvetica", 18, "bold"), 
                             fg="#A9A9A9", bg="#333333")
        login_label.place(relx=0.5, rely=0.15, anchor="center")

        # Username field
        username_label = tk.Label(self.login_frame, text="Username", font=("Helvetica", 11), 
                                fg="#A9A9A9", bg="#333333")
        username_label.place(relx=0.5, rely=0.3, anchor="center")
        self.username_entry = tk.Entry(self.login_frame, font=("Helvetica", 12), width=22, 
                              bg="#444444", fg="white", insertbackground="white", relief="flat")
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")

        # Password field
        password_label = tk.Label(self.login_frame, text="Password", font=("Helvetica", 11), 
                                fg="#A9A9A9", bg="#333333")
        password_label.place(relx=0.5, rely=0.55, anchor="center")
        self.password_entry = tk.Entry(self.login_frame, font=("Helvetica", 12), show="*", width=22, 
                              bg="#444444", fg="white", insertbackground="white", relief="flat")
        self.password_entry.place(relx=0.5, rely=0.65, anchor="center")

        # Login button
        login_button = tk.Button(self.login_frame, text="Login", font=("Helvetica", 12, "bold"), 
                               bg="#4CAF50", fg="white", relief="flat", command=self.validate_login)
        login_button.place(relx=0.5, rely=0.8, anchor="center", width=100)

        # Bottom text
        bottom_text = tk.Label(self.login_frame, text='"Login for a Streamlined QC Process"', 
                             font=("Helvetica", 9, "italic"), fg="#A9A9A9", bg="#333333")
        bottom_text.place(relx=0.5, rely=0.9, anchor="center")

        # Center logo with transparent background
        self.logo_frame = tk.Canvas(self.canvas, bg='', bd=0, highlightthickness=0)
        self.logo_frame.place(relx=0.25, rely=0.5, anchor="center")

        try:
            # Load and process logo image
            logo_image = Image.open("logo.png")
            logo_image = logo_image.convert('RGBA')
            
            # Make white background transparent
            data = logo_image.getdata()
            new_data = []
            for item in data:
                # Change all white (also shades of whites) pixels to transparent
                if item[0] > 200 and item[1] > 200 and item[2] > 200:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            logo_image.putdata(new_data)
            
            # Resize logo
            logo_image = logo_image.resize((200, 100), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            
            # Display logo
            self.logo_canvas = tk.Label(self.logo_frame, image=self.logo_photo, bg='')
            self.logo_canvas.pack()

            # Slogan text
            slogan_text = tk.Label(self.logo_frame, text="Connecting the dots", 
                                 font=("Helvetica", 12), fg="white", bg='')
            slogan_text.pack()

            # Main text
            main_text = tk.Label(self.logo_frame, text="Streamlined QC Process", 
                               font=("Helvetica", 16, "bold"), fg="white", bg='')
            main_text.pack(pady=10)

        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback if logo not found
            logo_label = tk.Label(self.logo_frame, text="PURVAJ.com", 
                                font=("Helvetica", 24, "bold"), fg="white", bg='')
            logo_label.pack()

    def create_round_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        """Create rounded rectangle canvas object"""
        points = [x1+radius, y1,
                 x1+radius, y1,
                 x2-radius, y1,
                 x2-radius, y1,
                 x2, y1,
                 x2, y1+radius,
                 x2, y1+radius,
                 x2, y2-radius,
                 x2, y2-radius,
                 x2, y2,
                 x2-radius, y2,
                 x2-radius, y2,
                 x1+radius, y2,
                 x1+radius, y2,
                 x1, y2,
                 x1, y2-radius,
                 x1, y2-radius,
                 x1, y1+radius,
                 x1, y1+radius,
                 x1, y1]
        return self.login_frame.create_polygon(points, **kwargs, smooth=True)

    def resize_background(self, event):
        """Resize background image when window is resized"""
        new_width = event.width
        new_height = event.height
        resized_image = self.original_bg.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.bg_canvas, image=self.bg_photo)

    def validate_login(self):
        """Validate user login credentials"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            # Connect to MySQL (replace with your credentials)
            connection = mysql.connector.connect(
                host="localhost",
                user="your_username",
                password="your_password",
                database="purvaj_db"
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
    # Add rounded rectangle method to Canvas class
    tk.Canvas.create_round_rect = LoginApp.create_round_rect
    app = LoginApp(root)
    root.mainloop()