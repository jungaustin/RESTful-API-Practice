from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# create a user
@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email = user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# get all users
@app.get("/users/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# get a user by ID
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user

# delete a user
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    db.delete(user)
    db.commit()
    return {"message" : f"User {user_id} deleted successfully"}




# app = FastAPI()

# items = []
# #If I want an Item required, I could remove "= None" so it fails to run if I don't have it. Otherwise i can leave it if its optional
# class Item(BaseModel):
#     text: str = None
#     is_done: bool = False


# @app.get("/")
# def root():
#     return {"Hello": "World"}

# @app.post("/items")
# def create_item(item: Item):
#     items.append(item)
#     return items

# @app.get("/items", response_model=list[Item])
# def list_items(limit: int = 10):
#     return items[0:limit]

# @app.get("/items/{item_id}", response_model=Item)
# def get_item(item_id:int) -> Item:
#     if item_id < len(items):
#         item = items[item_id]
#         return item
#     else:
#         raise HTTPException(status_code=404, detail=f"Item {item_id} not found")