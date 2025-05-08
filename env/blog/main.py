from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError
from .schemas import Blog
from .config import CLIET_ID, CLINET_SECRET

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="rajabadidurgaparsai")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=CLIET_ID,
    client_secret=CLINET_SECRET,
    client_kwargs={
        "scope": "openid email profile"
    }
)

@app.get("/")
async def get_all(request: Request):
    return templates.TemplateResponse("page.html", {"request": request})

@app.post("/")
async def create_new(request_body: Blog):
    return {"data": {"message": request_body}}

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/google/callback")
async def google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return {"error": str(e)}

    user = token.get("userinfo")
    if user:
        request.session["user"] = dict(user)
    return {"message": "Logged in as Google user", "user": user}
