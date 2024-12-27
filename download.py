import gdown

# Google Drive file ID
file_id = "1Vp_N-8eoM5tY0lUxhh_SR1LNekT-8Isk"
url = f"https://drive.google.com/uc?id={file_id}"

# Download the file
output = "downloaded_image.jpg"
gdown.download(url, output, quiet=False)

print("File downloaded successfully!")
