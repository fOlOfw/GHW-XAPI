from fastapi import FastAPI, HTTPException, HTTPException, Security, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import uuid

app = FastAPI()

users = [
    {"id": str(uuid.uuid4()), "username": "Jo", "email": "jo@example.com", "password": "pass", "role": "admin"},
    {"id": str(uuid.uuid4()), "username": "Ed", "email": "ed@example.com", "password": "pass", "role": "user"},
]

#Pydantic model
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str

class UserUpdate(BaseModel):
    username: str
    email: str

security = HTTPBasic() 

# check if user is authenticated
def authenticate(credentials: HTTPBasicCredentials = Security(security)):
    user = None
    for u in users:
        if u["username"] == credentials.username and u["password"] == credentials.password:
            user = u
            return user
    raise HTTPException(status_code=401, detail="invalid credentials!")

# authorize user
def authorize(user: dict = Depends(authenticate)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="permission denied!")
    return None

#Get all users if the user is authenticated 
@app.get("/users", response_model=list[UserResponse])
def get_users(user: dict = Depends(authorize)):
    return users

def read_root():
    return {"message": "Checking if the server is running!"}

@app.get("/")
def read_root():
    return {"message": "Checking if the server is running!"}

#Get all users if the user is authenticated and have admin role
@app.get("/users/{user_id}", response_model=list[UserResponse])
def get_user(user_id: str, user: dict = Depends(authorize)):
    for user in users:
        if user["id"] == user_id:
            return user
    return {"message": "User is not found due to the id unmatch"}

@app.post("/users")
def create_user(user: UserResponse):
    new_user = {
        "id": str(uuid.uuid4()),
        "username": user.username,
        "email": user.email
    }
    users.append(new_user)
    return new_user

@app.put("/users/{user_id}")
def update_user(user_id: str, user: UserResponse):
   for u in users:
    if u["id"] == user_id:
        u["username"] = user.username
        u["email"] = user.email
        return u
    return {"message": "Current user cannot be updated because user is not found!"}

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    for i, user in enumerate(users):
        if user["id"] == user_id:
            users.pop(i)
            return{"message": "User deleted successfully!"}
    return {"mesage": "User is not found!"}


if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="localhost", port=8001)