from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()

users = [
    {"id": str(uuid.uuid4()), "username": "Jo", "email": "jo@example.com"},
    {"id": str(uuid.uuid4()), "username": "Ed", "email": "ed@example.com"},
]

#Pydantic model
class User(BaseModel):
    username: str
    email: str

@app.get("/")
def read_root():
    return {"message": "Checking if the server is running!"}

@app.get("/users")
def get_users():
    return users

@app.get("/users/{user_id}")
def get_user(user_id: str):
    for user in users:
        if user["id"] == user_id:
            return user
    return {"message": "User is not found due to the id unmatch"}

@app.post("/users")
def create_user(user: User):
    new_user = {
        "id": str(uuid.uuid4()),
        "username": user.username,
        "email": user.email
    }
    users.append(new_user)
    return new_user

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="localhost", port=8001)