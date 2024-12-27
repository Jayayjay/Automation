import argparse
from PIL import Image, ImageDraw, ImageFont

def create_id_card(name, id_number, department, photo_path, output_path):
    # Create a blank ID card (size: 600x300 pixels)
    card = Image.new("RGB", (600, 300), "white")
    draw = ImageDraw.Draw(card)

    # Add text details
    font = ImageFont.truetype("arial.ttf", 20)  # Change to your font file if needed
    draw.text((20, 30), f"Name: {name}", fill="black", font=font)
    draw.text((20, 70), f"ID: {id_number}", fill="black", font=font)
    draw.text((20, 110), f"Department: {department}", fill="black", font=font)

    # Insert photo (resize it to fit)
    photo = Image.open(photo_path)
    photo = photo.resize((100, 100))
    card.paste(photo, (450, 50))

    # Save the ID card
    card.save(output_path)
    print(f"ID card saved at {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an ID card")
    parser.add_argument("--name", required=True, help="Name of the person")
    parser.add_argument("--id", required=True, help="ID number")
    parser.add_argument("--department", required=True, help="Department")
    parser.add_argument("--photo", required=True, help="Path to the photo")
    parser.add_argument("--output", required=True, help="Output path for the ID card")

    args = parser.parse_args()
    create_id_card(args.name, args.id, args.department, args.photo, args.output)
