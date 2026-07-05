from typing import ClassVar
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
import html
import re

class ContactForm(BaseModel):
    '''
    Contact Form Model
    This will reqpresent the messages for inquiries or questions that our visitors may have.
    '''
    
    # make sure we strip whitespace and do not allow exta space
    model_config: ClassVar[ConfigDict] = {
        "str_strip_whitespace": True, 
        "extra": "forbid"
    }

    # set the fields we are collecting and set constraints such as min and max length
    # Use build in EmailStr to validate email address patterns
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    subject: str = Field(..., min_length=1, max_length=150)
    message: str = Field(..., min_length=1, max_length=2000)


    # Function that will allow stripping empty space and removing special chars
    @field_validator('name', 'subject', mode='before')
    def strip_whitespace_and_remove_control_chars(cls, v: str) -> str:
        if not isinstance(v, str):
            return v
        # The config now handles stripping, but explicit is fine too.
        v = v.strip() 
        v = re.sub(r'[\x00-\x1f\x7f]+', '', v)
        return v


    # Function that will strip HTML and trim whitespace from the message field
    @field_validator('message', mode='before')
    def escape_html_and_trim(cls, v: str) -> str:
        if not isinstance(v, str):
            return v
        v = v.strip()
        return html.escape(v)