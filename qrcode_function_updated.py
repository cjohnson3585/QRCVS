import qrcode
import argparse

parser = argparse.ArgumentParser(description="A simple command-line tool")

# Add an argument
parser.add_argument('url', type=str, help='The url to embed in the QR Code')

# Parse the arguments
args = parser.parse_args()


# URL to be encoded in the QR code
url = {args.url}


# Create a QR code object
qr = qrcode.QRCode(
    version=4,  # controls the size of the QR Code
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # controls the error correction used for the QR Code
    box_size=15,  # controls how many pixels each “box” of the QR code is
    border=1,  # controls how many boxes thick the border should be
)

# Add data to the QR code
qr.add_data(url)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill='black', back_color='white')

# Save the image to a file
img.save("github_qr_code.png")

print("QR code generated and saved as github_qr_code.png")