from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from .service import (
    get_facebook_login_url, exchange_code_for_token, get_facebook_user_info
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


from fastapi import Request

@router.get("/login")
def login(request: Request):
    facebook_login_url = get_facebook_login_url()
    return templates.TemplateResponse("page.html", {
        "request": request,
        "facebook_login_url": facebook_login_url
    })



@router.get("/callback")
def callback(request: Request, code: str):
    access_token = exchange_code_for_token(code)
    user_info = get_facebook_user_info(access_token)
    return user_info
