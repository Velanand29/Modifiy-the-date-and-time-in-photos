# from PIL import Image
# import piexif
# from datetime import datetime

# # Load the image
# image_path = 'IMG_20230706_090902.jpg'
# img = Image.open(image_path)

# # Try to load EXIF data, or initialize an empty one if not available
# exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

# if "exif" in img.info:
#     exif_dict = piexif.load(img.info["exif"])

# # Get the original date if it exists
# original_date = None
# if piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
#     original_date = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
# elif piexif.ImageIFD.DateTime in exif_dict["0th"]:
#     original_date = exif_dict["0th"][piexif.ImageIFD.DateTime].decode('utf-8')

# if original_date:
#     print(f"Original Date and Time: {original_date}")
# else:
#     print("No original date found in EXIF data.")

# # Get the current year and month, and set the day to 13
# new_date = datetime.now().replace(day=13).strftime("%Y:%m:%d %H:%M:%S")

# # Update or add the DateTimeOriginal and DateTime fields in EXIF
# exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = new_date.encode('utf-8')
# exif_dict["0th"][piexif.ImageIFD.DateTime] = new_date.encode('utf-8')

# # Convert the exif_dict back to binary format
# exif_bytes = piexif.dump(exif_dict)

# # Save the image with the updated EXIF data
# img.save('updated_image.jpg', "jpeg", exif=exif_bytes)

# print(f"Date updated to: {new_date}")



from PIL import Image
import piexif
from datetime import datetime

# Function to get the original date from EXIF metadata
def get_original_datetime(exif_dict):
    original_date = None
    if piexif.ExifIFD.DateTimeOriginal in exif_dict['Exif']:
        original_date = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
        print(f"Original Date of the Photo (Taken): {original_date}")
    else:
        print("No original date found in EXIF data.")
    return original_date

# Function to clean up EXIF data (remove problematic tags)
def clean_exif_data(exif_dict):
    for ifd in exif_dict:
        if isinstance(exif_dict[ifd], dict):
            for tag in list(exif_dict[ifd].keys()):
                value = exif_dict[ifd][tag]
                if isinstance(value, int):
                    print(f"Removing tag {tag} in IFD {ifd} due to invalid type {type(value)}.")
                    del exif_dict[ifd][tag]
    return exif_dict

# Function to print the updated EXIF data
def print_updated_exif(image_path):
    img = Image.open(image_path)
    if "exif" in img.info:
        updated_exif_dict = piexif.load(img.info['exif'])
        updated_date_taken = updated_exif_dict['Exif'].get(piexif.ExifIFD.DateTimeOriginal)
        updated_date_modified = updated_exif_dict['Exif'].get(piexif.ExifIFD.DateTimeDigitized)
        updated_general_date = updated_exif_dict['0th'].get(piexif.ImageIFD.DateTime)
        
        if updated_date_taken:
            print(f"Updated Date Taken: {updated_date_taken.decode('utf-8')}")
        else:
            print("Failed to retrieve updated Date Taken.")
            
        if updated_date_modified:
            print(f"Updated Date Modified: {updated_date_modified.decode('utf-8')}")
        else:
            print("Failed to retrieve updated Date Modified.")
        
        if updated_general_date:
            print(f"Updated General Date: {updated_general_date.decode('utf-8')}")
        else:
            print("Failed to retrieve updated General Date.")
    else:
        print("No EXIF data found in the updated image.")

# Load the image
image_path = 'IMG_20230706_090902.jpg'  # Replace with your image file path
img = Image.open(image_path)

# Try to load EXIF data, or initialize an empty one if not available
exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
if "exif" in img.info:
    exif_dict = piexif.load(img.info["exif"])

# Print the original date of the photo
original_date = get_original_datetime(exif_dict)

# Prompt the user for the new date and time
new_date_str = input("Enter the new desired date and time (YYYY-MM-DD HH:MM:SS): ")
try:
    new_datetime = datetime.strptime(new_date_str, "%Y-%m-%d %H:%M:%S")
except ValueError:
    print("Invalid date format. Please use YYYY-MM-DD HH:MM:SS.")
    exit()

# Format the new date and time in the proper EXIF format: "YYYY:MM:DD HH:MM:SS"
formatted_datetime = new_datetime.strftime("%Y:%m:%d %H:%M:%S")

# Update or add the DateTimeOriginal (Date Taken), DateTimeDigitized (Date Modified), and DateTime (General Date)
exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = formatted_datetime.encode('utf-8')  # Date Taken
exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = formatted_datetime.encode('utf-8')  # Date Modified
exif_dict["0th"][piexif.ImageIFD.DateTime] = formatted_datetime.encode('utf-8')  # General Date

# Clean the EXIF data to remove problematic tags
exif_dict = clean_exif_data(exif_dict)

# Convert the exif_dict back to binary format
try:
    exif_bytes = piexif.dump(exif_dict)
    # Save the image only if EXIF data could be dumped successfully
    img.save('updated_image.jpg', "jpeg", exif=exif_bytes)
    print(f"EXIF data successfully updated to {formatted_datetime}.")
except ValueError as e:
    print(f"Error dumping EXIF data: {e}")
    exif_bytes = None

# Print updated EXIF date from the saved image
if exif_bytes:
    print_updated_exif('updated_image.jpg')