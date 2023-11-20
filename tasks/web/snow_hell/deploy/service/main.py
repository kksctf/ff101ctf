import os

from typing import Optional
from datetime import datetime, timedelta

from fastapi import FastAPI, Form, HTTPException, status, Request, Depends
from fastapi.templating import Jinja2Templates
from starlette.responses import Response, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt


JWT_SECRET_KEY = "902addb3f1a15d5a45652794bb36a630ddb2cdb8097419fb81fd4047f686956b"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
super_db_users = {
    "admin": {
        "username": "admin",
        "pass": "ee6b4deb587078e5423813736fdbc6c2aeca47fde86bc95877cb780be91d5bc3",
        "admin": True,
    }
}
super_db_congrs = {}


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    global JWT_SECRET_KEY
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_user_token(username: str):
    access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"username": username}, expires_delta=access_token_expires)
    return access_token


async def get_current_user(token: str = Depends(oauth2_scheme)):
    global super_db_users, JWT_SECRET_KEY
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    username: str = None
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])  # no "alg:none"
        username = payload.get("username")
        if username is None:
            print("username is nont")
            raise credentials_exception
    except JWTError as ex:
        print("jwt gg", token, ex)
        raise credentials_exception
    user = super_db_users.get(username, None)
    if user is None:
        print("user is none")
        raise credentials_exception
    return user


async def get_user_safe(request: Request):
    user = None
    try:
        user = await get_current_user(await oauth2_scheme(request))
    except HTTPException:
        user = None
        print("oops")
    return user


app = FastAPI(
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_base_path = os.path.dirname(os.path.abspath(__file__))
t = Jinja2Templates(directory=os.path.join(_base_path, "front", "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(_base_path, "front", "static")), name="static")


@app.middleware("http")
async def CSP_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers[
        "Content-Security-Policy"
    ] = "default-src * 'unsafe-inline' 'unsafe-eval'; script-src * 'unsafe-inline' 'unsafe-eval'; connect-src * 'unsafe-inline'; img-src * data: blob: 'unsafe-inline'; frame-src *; style-src * 'unsafe-inline';"
    return response


@app.get("/")
@app.get("/index")
async def index(request: Request, response: Response):
    return t.TemplateResponse(
        "index.jhtml",
        {
            "request": request,
            "curr_user": await get_user_safe(request),
        },
    )


@app.get("/login")
async def login(request: Request, response: Response):
    return t.TemplateResponse(
        "login.jhtml",
        {
            "request": request,
            "curr_user": await get_user_safe(request),
        },
    )


@app.post("/login")
async def login_post(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    global super_db_users
    message = ""
    curr_user = None
    cookie = None
    if username in super_db_users:
        user = super_db_users[username]
        if user["pass"] != password:
            message = "Неверный пароль"
        else:
            message = "Успешный вход"
            curr_user = user
            cookie = create_user_token(username)
    else:
        super_db_users[username] = {
            "username": username,
            "pass": password,
            "admin": False,
        }
        message = "Успешная регистрация"
        curr_user = super_db_users[username]
        cookie = create_user_token(username)

    resp = t.TemplateResponse(
        "login.jhtml",
        {
            "request": request,
            "curr_user": curr_user,
            "message": message,
            "username": username,
            "password": password,
        },
    )
    resp.set_cookie("access_token", value=f"Bearer {cookie}")
    return resp


@app.get("/users_list")
async def users_list(request: Request, response: Response, curr_user=Depends(get_current_user)):
    global super_db_users
    usernames = super_db_users.keys()
    return t.TemplateResponse(
        "users_list.jhtml",
        {
            "request": request,
            "usernames": usernames,
            "curr_user": curr_user,
        },
    )


@app.get("/congr")
async def congr(request: Request, response: Response, curr_user=Depends(get_current_user)):
    return t.TemplateResponse(
        "congr.jhtml",
        {
            "request": request,
            "curr_user": curr_user,
        },
    )


@app.post("/congr")
async def congr_post(
    request: Request,
    response: Response,
    curr_user=Depends(get_current_user),
    username: str = Form(...),
    congr: str = Form(...),
):
    global super_db_users, super_db_congrs
    message = ""
    if username not in super_db_users:
        message = "Пользователь не существует"
    else:
        if username not in super_db_congrs:
            super_db_congrs[username] = []
        super_db_congrs[username].append(
            {
                "from": curr_user["username"],
                "to": username,
                "congr": congr,
            }
        )
        message = "Ваше поздравление было отправлено"
    return t.TemplateResponse(
        "congr.jhtml",
        {"request": request, "curr_user": curr_user, "message": message, "username": username, "congr": congr},
    )


@app.get("/my_congr")
async def congr_list(request: Request, response: Response, curr_user=Depends(get_current_user)):
    global super_db_users, super_db_congrs
    congs = []
    for congr in super_db_congrs.values():
        congs.extend(congr)
    congrs_about_me = filter(lambda x: x["to"] == curr_user["username"] or x["from"] == curr_user["username"], congs)
    return t.TemplateResponse(
        "congr_list.jhtml",
        {
            "request": request,
            "congrs_about_me": congrs_about_me,
            "curr_user": curr_user,
            "do_kek": False,
        },
    )


@app.get("/admin_congr")
async def admin_congr_list(request: Request, response: Response, curr_user=Depends(get_current_user)):
    global super_db_users, super_db_congrs
    congs = []
    for congr in super_db_congrs.values():
        congs.extend(congr)
    return t.TemplateResponse(
        "congr_list.jhtml",
        {
            "request": request,
            "congrs_about_me": congs,
            "curr_user": curr_user,
            "do_kek": True,
        },
    )
