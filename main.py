
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from models import PanCardVerificationResponse
from pan_card_utils import extract_pan_details, parse_pan_card_details, is_valid_pan, check_fifth_letter


app = FastAPI()


## Image reading and extracting the text from images using OCR (Optical Character Recognition)
@app.post("/verify_pan_card/", response_model=PanCardVerificationResponse)
async def verify_pan_card(file: UploadFile = File(...)):
    # Read the image file and process it
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    

    ocr_text = extract_pan_details(image)
    pan_details = parse_pan_card_details(ocr_text)
    
    if not pan_details.get("pan_number") or not pan_details.get("name"):
        return JSONResponse(status_code=400, content={"message": "Could not extract PAN number or Name"})
    
    pan_number = pan_details["pan_number"]
    name = pan_details["name"]
    
    valid_pan = is_valid_pan(pan_number)
    fifth_letter = check_fifth_letter(name)
    
    if valid_pan and fifth_letter:
        return PanCardVerificationResponse(
            valid=True,
            pan_number=pan_number,
            name=name,
            fifth_letter=fifth_letter,
            message="PAN Card is valid and the 5th letter of the name is correct."
        )
    
    return PanCardVerificationResponse(
        valid=False,
        pan_number=pan_number,
        name=name,
        fifth_letter=fifth_letter if fifth_letter else "Not applicable",
        message="Invalid PAN Card or the name does not have a valid 5th letter."
    )

#Using uvicorn to run api locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
