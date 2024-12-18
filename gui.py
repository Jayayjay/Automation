import pandas as pd
import requests
from PIL import Image, ImageDraw, ImageFont
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Button, Label, Frame


# Convert Google Drive URL to direct download link
def get_drive_direct_url(drive_url):
    if "id=" in drive_url:
        file_id = drive_url.split("id=")[-1]
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return drive_url


# Download image from URL
def download_image(image_url, output_path):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Check for HTTP errors
        with open(output_path, "wb") as file:
            file.write(response.content)
        return output_path
    except Exception as e:
        print(f"Failed to download image from {image_url}: {e}")
        return None


# Create ID card
def create_id_card(template_path, output_path, full_name, matric_number, department, passport_path, signature_path, gender, blood_group):
    card = Image.open(template_path)
    draw = ImageDraw.Draw(card)

    # Define font and positions
    font = ImageFont.truetype("arial.ttf", 24)
    text_positions = {
        "name": (100, 100),
        "matric_number": (100, 150),
        "department": (100, 200),
        "gender": (100, 250),
        "blood_group": (100, 300)
    }

    # Add text to the template
    draw.text(text_positions["name"], f"Name: {full_name}", fill="black", font=font)
    draw.text(text_positions["matric_number"], f"Matric No: {matric_number}", fill="black", font=font)
    draw.text(text_positions["department"], f"Department: {department}", fill="black", font=font)
    draw.text(text_positions["gender"], f"Gender: {gender}", fill="black", font=font)
    draw.text(text_positions["blood_group"], f"Blood Group: {blood_group}", fill="black", font=font)

    # Add Passport
    if passport_path and os.path.exists(passport_path):
        passport = Image.open(passport_path).resize((100, 100))
        card.paste(passport, (400, 100))

    # Add Signature
    if signature_path and os.path.exists(signature_path):
        signature = Image.open(signature_path).resize((150, 50))
        card.paste(signature, (400, 250))

    # Save the ID card
    card.save(output_path)


# GUI Application
class IDCardAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ID Card Automation")
        self.csv_data = None
        self.current_index = 0
        self.template_path = "/path/to/id_card_template.png"  # Update with your template path
        self.output_dir = "./id_cards/"
        self.image_dir = "./images/"

        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.image_dir, exist_ok=True)

        self.build_gui()

    def build_gui(self):
        # GUI Layout
        frame = Frame(self.root)
        frame.pack(pady=20)

        Label(frame, text="ID Card Automation Tool").grid(row=0, column=0, columnspan=3, pady=10)

        Button(frame, text="Load CSV", command=self.load_csv).grid(row=1, column=0, padx=10)
        Button(frame, text="Generate All ID Cards", command=self.generate_all).grid(row=1, column=1, padx=10)
        Button(frame, text="Exit", command=self.root.quit).grid(row=1, column=2, padx=10)

        self.preview_label = Label(self.root, text="", font=("Arial", 12))
        self.preview_label.pack(pady=20)

        self.nav_frame = Frame(self.root)
        self.nav_frame.pack(pady=10)

        Button(self.nav_frame, text="Previous", command=self.previous_entry).grid(row=0, column=0, padx=10)
        Button(self.nav_frame, text="Generate ID Card", command=self.generate_single).grid(row=0, column=1, padx=10)
        Button(self.nav_frame, text="Next", command=self.next_entry).grid(row=0, column=2, padx=10)

    def load_csv(self):
        # Load CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.csv_data = pd.read_csv(file_path)
            self.current_index = 0
            self.update_preview()
            messagebox.showinfo("Success", "CSV file loaded successfully!")

    def update_preview(self):
        if self.csv_data is not None and not self.csv_data.empty:
            row = self.csv_data.iloc[self.current_index]
            preview_text = (
                f"Name: {row['Full Name ( Format - Last, First, Other names) ']}\n"
                f"Matriculation Number: {row['Matriculation Number']}\n"
                f"Department: {row['Department']}\n"
                f"Gender: {row['Gender']}\n"
                f"Blood Group: {row['Blood Group']}\n"
            )
            self.preview_label.config(text=preview_text)

    def generate_single(self):
        if self.csv_data is not None:
            row = self.csv_data.iloc[self.current_index]

            # Extract details
            full_name = row["Full Name ( Format - Last, First, Other names) "]
            matric_number = row["Matriculation Number"]
            department = row["Department"]
            passport_url = get_drive_direct_url(row["Passport"])
            signature_url = get_drive_direct_url(row["Signature"])
            gender = row["Gender"]
            blood_group = row["Blood Group"]

            # Download images
            passport_path = download_image(passport_url, f"{self.image_dir}/{matric_number}_passport.png")
            signature_path = download_image(signature_url, f"{self.image_dir}/{matric_number}_signature.png")

            # Generate ID card
            output_path = f"{self.output_dir}/{matric_number}_id_card.png"
            create_id_card(self.template_path, output_path, full_name, matric_number, department, passport_path, signature_path, gender, blood_group)
            messagebox.showinfo("Success", f"ID Card for {full_name} generated!")

    def generate_all(self):
        if self.csv_data is not None:
            for _, row in self.csv_data.iterrows():
                full_name = row["Full Name ( Format - Last, First, Other names) "]
                matric_number = row["Matriculation Number"]
                department = row["Department"]
                passport_url = get_drive_direct_url(row["Passport"])
                signature_url = get_drive_direct_url(row["Signature"])
                gender = row["Gender"]
                blood_group = row["Blood Group"]

                # Download images
                passport_path = download_image(passport_url, f"{self.image_dir}/{matric_number}_passport.png")
                signature_path = download_image(signature_url, f"{self.image_dir}/{matric_number}_signature.png")

                # Generate ID card
                output_path = f"{self.output_dir}/{matric_number}_id_card.png"
                create_id_card(self.template_path, output_path, full_name, matric_number, department, passport_path, signature_path, gender, blood_group)
            messagebox.showinfo("Success", "All ID Cards generated successfully!")

    def previous_entry(self):
        if self.csv_data is not None and self.current_index > 0:
            self.current_index -= 1
            self.update_preview()

    def next_entry(self):
        if self.csv_data is not None and self.current_index < len(self.csv_data) - 1:
            self.current_index += 1
            self.update_preview()


if __name__ == "__main__":
    root = tk.Tk()
    app = IDCardAutomationApp(root)
    root.mainloop()
