import base64
import os
import random
import shutil
from stat import S_IREAD

from databases import Database
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

# i experienced a lot of hacks, so let's open database in r/o mode
os.chmod('test.db', S_IREAD)
DATABASE_URL = "sqlite:///./test.db"

SECRET_KEY = open("jwt.txt").read()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

BANNED = ["jwt_is_unbreakable"]
database = Database(DATABASE_URL)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


def create_access_token(data: dict):
    to_encode = data.copy()
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token


security = HTTPBearer()


def get_current_username(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


@app.get("/login")
async def login(username: str, password: str):
    if username in BANNED:
        return {"status": "failed", "reason": "User banned"}

    try:
        user = await database.fetch_one(
            f"SELECT * FROM users WHERE username='" + username + "' and password='" + password + "'")
        if not user:
            return {"status": "failed", "reason": "Invalid user or password"}
    except Exception as e:
        return {"status": "failed", "reason": str(e)}

    access_token = create_access_token(data={"sub": username})
    return {"status": "ok", "access_token": access_token, "token_type": "bearer"}


@app.get("/get_content")
async def get_content(token_username: str = Depends(get_current_username)):
    listdir = os.listdir(os.path.join("image_storage", token_username))
    images = {item: base64.b64encode(open(os.path.join("image_storage", token_username, item), "rb").read()) for item in
              listdir}
    return {"status": "ok", "images": images}


@app.post("/set_content")
async def set_content(token_username: str = Depends(get_current_username), file: UploadFile = File(...)):
    if random.random() < 2:  # no hope
        return {"status": "failed", "reason": "currently disabled, out of disk space"}
    file_location = f"image_storage/{token_username}/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "Image uploaded successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
