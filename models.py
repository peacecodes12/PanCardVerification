from pydantic import BaseModel

## model defination for the pan card image
class PanCardVerificationResponse(BaseModel):
    valid: bool
    pan_number: str
    name: str
    fifth_letter: str
    message: str
