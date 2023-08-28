from pydantic import BaseModel, conint, constr, condecimal, NaiveDatetime, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):

    email: EmailStr
    password: constr(min_length=8, max_length=25)

class UserResponse(BaseModel):

    id: int
    email: EmailStr
    created_at: NaiveDatetime

class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=25)

class ItemBase(BaseModel):
    item_description: constr(min_length=1, max_length=60)
    item_format: int
    item_genre: int
    item_country: int
    item_region: int
    item_subtitles: int
    item_packaging: int
    item_slipcover: int = 0
    item_condition: int
    item_condition_comment: constr(max_length=255) = None
    item_images: constr(max_length=255) = None
    item_price: condecimal(max_digits=5, decimal_places=2)
    item_shipping: int
    item_huuto_id: int = None
    item_huuto_text: constr(max_length=1024) = None
    item_huuto_endtime: NaiveDatetime = None
    item_modified: int = 0

class ItemCreate(ItemBase):
    pass

class ItemResponse(BaseModel):

    item_id: int
    item_description: constr(min_length=1, max_length=60) 
    item_format: int
    item_genre: int
    item_country: Optional[int]
    item_region: int
    item_subtitles: Optional[int]
    item_packaging: int
    item_slipcover: int
    item_condition: int
    item_condition_comment: Optional[constr(max_length=255)]
    item_images: Optional[constr(max_length=255)]
    item_price: condecimal(max_digits=5, decimal_places=2)
    item_shipping: int
    item_huuto_id: Optional[int]
    item_huuto_text: Optional[constr(max_length=1024)]
    item_huuto_endtime: Optional[NaiveDatetime]
    item_modified: int
    #owner_id: Optional[int]
    #owner: UserResponse

class ItemCount(BaseModel):
    item_count: int 

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    id: int

class Vote(BaseModel):
    item_id: int
    dir: conint(le=1)

class Format(BaseModel):
    format_name: constr(max_length=10)
    format_id: int

class Genre(BaseModel):
    genre_name: constr(max_length=20)
    genre_id: int

class Country(BaseModel):
    country_name: constr(max_length=15)
    country_id: int
    
class Condition(BaseModel):
    condition_description: constr(max_length=15)
    condition_id: int

class Region(BaseModel):
    region_name: constr(max_length=15)
    region_id: int

class Subtitles(BaseModel):
    subtitle_name: constr(max_length=15)
    subtitle_id: int

class Packaging(BaseModel):
    packaging_name: constr(max_length=15)
    packaging_id: int

class Shipping(BaseModel):
    shipping_price: condecimal(max_digits=4, decimal_places=2)
    shipping_description: constr(max_length=20)
    shipping_costs_id: int

class FilterResponse(BaseModel):
    Format: List[Format]
    Genre: List[Genre]
    Country: List[Country]
    Condition: List[Condition]
    Region: List[Region]
    Subtitles: List[Subtitles]
    Packaging: List[Packaging]
    Shipping: List[Shipping]