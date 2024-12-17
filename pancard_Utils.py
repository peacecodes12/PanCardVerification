import pytesseract
import cv2
import numpy as np
from PIL import Image
import re

# Function where the details of pan card are extracted
def extract_pan_details(image: Image.Image):
    open_cv_image = np.array(image)
    gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(gray_image)
    return extracted_text

# Function to check if the extraced pan card format is correct 
#### ABCDE1234F   10 charactes, starting with 5 letter then 4 digits and then 1 character
def is_valid_pan(pan_number: str):
    return bool(re.match(r'^[A-Z]{5}\d{4}[A-Z]$', pan_number))

## Function to verify the 5th letter
## 5th letter should be same as the initial of the last name
def check_fifth_letter(name: str):
    if len(name) >= 5:
        return name[4]  
    return None


def parse_pan_card_details(ocr_text: str):
    pan_details = {}
    
   ## regrex function
    pan_match = re.search(r'Permanent Account Number\s*[:\-]?\s*([A-Z]{5}\d{4}[A-Z])', ocr_text)
    if pan_match:
        pan_details['pan_number'] = pan_match.group(1)

    
    name_match = re.search(r'Name\s*[:\-]?\s*([A-Za-z\s]+)', ocr_text)
    if name_match:
        pan_details['name'] = name_match.group(1).strip()

    return pan_details
