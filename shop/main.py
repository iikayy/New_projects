from fastapi import FastAPI, Depends, HTTPException, Path, Form, status
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from forms import MenuItem, UpdateMenu, UpdateOrder, OrderItem, UserOut
from models import *
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from pydantic import EmailStr
import secrets

SECRET_KEY = secrets.token_hex(32)

Base.metadata.create_all(bind=engine)
app = FastAPI()


# Initialize password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT
SECRET = SECRET_KEY
manager = LoginManager(SECRET, token_url='/login', use_cookie=True)
manager.cookie_name = "auth"


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get user by email function for login manager
def get_user(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


@manager.user_loader
def load_user(email: str):
    db = next(get_db())
    return get_user(email, db)


# Route to get all menu items
@app.get("/menu", response_model=list[MenuItem])
def get_all_menu(db: Session = Depends(get_db)):
    all_menu = db.query(Menu).all()
    return all_menu


# Route to search for a particular menu item
@app.get("/search/{name}", response_model=MenuItem)
def search_menu(name: str = Path(description="The name of the food in the menu"), db: Session = Depends(get_db)):
    result = db.query(Menu).filter(Menu.food_name == name.title()).first()
    if not result:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return result


# Route to add a new menu item
@app.post("/add", response_model=MenuItem)
def add_new_menu_item(menu_item: MenuItem, db: Session = Depends(get_db)):
    db_menu_item = db.query(Menu).filter(Menu.food_name == menu_item.food_name.title()).first()
    if db_menu_item:
        raise HTTPException(status_code=400, detail="Menu item already exists")
    new_menu_item = Menu(**menu_item.dict())
    db.add(new_menu_item)
    db.commit()
    db.refresh(new_menu_item)
    return new_menu_item


# Route to make a new order
@app.post("/new-order", response_model=OrderItem)
async def create_order(order: OrderItem, db: Session = Depends(get_db)):
    new_order = Order(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


# Route to update the menu
@app.put("/update_menu/{food_name}", response_model=MenuItem)
def update_menu(
    menu_update: UpdateMenu,
    food_name: str = Path(description="The name of the food you want to update in the menu"),
    db: Session = Depends(get_db)
):
    menu = db.query(Menu).filter(Menu.food_name == food_name).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu item not found")
    for key, value in menu_update.dict(exclude_unset=True).items():
        setattr(menu, key, value)
    db.commit()
    db.refresh(menu)
    return menu


# Route to update an order
@app.put("/update_order/{order_name}", response_model=OrderItem)
def update_order(order_name: str, order_update: UpdateOrder, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.food_name == order_name.lower()).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order item not found")
    for key, value in order_update.dict(exclude_unset=True).items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order


# Route to delete a menu item
@app.delete("/delete_menu/{food_name}", response_model=dict)
def delete_menu_item(food_name: str = Path(description="The name of the food you want to delete from the menu"),
                     db: Session = Depends(get_db)):
    menu_item = db.query(Menu).filter(Menu.food_name == food_name.title()).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    db.delete(menu_item)
    db.commit()
    return {"success": "Successfully deleted the menu item"}


# Route to delete an order
@app.delete("/delete_order/{order_name}", response_model=dict)
def delete_order(order_name: str = Path(description="The name of the food you want to delete from your order"),
                 db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.food_name == order_name.lower()).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order item not found")
    db.delete(order)
    db.commit()
    return {"success": "Successfully deleted the order"}


# Route to register a new user
@app.post("/register", response_model=UserOut)
async def register_user(
        email: EmailStr = Form(...),
        name: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    # Check if user already exists
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = pwd_context.hash(password)

    # Create new user
    new_user = User(
        email=email,
        name=name,
        password=hashed_password,
    )

    # Add user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Route to log in a user
@app.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form_data.username
    password = form_data.password

    user = get_user(email, db)
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = manager.create_access_token(data={"sub": user.email})
    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    manager.set_cookie(response, access_token)
    return response


# Route to logout user
@app.post("/logout")
async def logout_user():
    response = JSONResponse(content={"message": "Successfully logged out"})
    manager.set_cookie(response, "")
    return response
