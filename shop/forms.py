from pydantic import BaseModel, EmailStr


class MenuItem(BaseModel):
    food_name: str
    food_quantity: str
    food_price: float
    food_img_url: str

    class Config:
        from_attributes = True


class OrderItem(BaseModel):
    food_name: str
    quantity_ordered: str

    class Config:
        from_attributes = True


class UpdateMenu(BaseModel):
    food_name: str | None
    food_quantity: str | None
    food_price: float | None
    food_img_url: str | None

    class Config:
        from_attributes = True


class UpdateOrder(BaseModel):
    food_name: str | None
    quantity_ordered: str | None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    email: EmailStr
    name: str

    class Config:
        from_attributes = True
