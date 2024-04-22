from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# from typing import Annotated

app = FastAPI() # FastAPI 物件

app.add_middleware(SessionMiddleware, secret_key="123456")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/signin")
# async def signin(username: Annotated[str, Form()], password: Annotated[str, Form()]):
async def signin(request: Request, username: str = Form(default=None), password: str = Form(default=None)):
    if username == "test" and password == "test":
        request.session['user'] = username
        return RedirectResponse(url='/member', status_code=302)
    else:
        # 帳號密碼錯誤
        error_message = "帳號、或密碼輸入錯誤"
        return RedirectResponse(url=f'/error?message={error_message}', status_code=302)

@app.get("/member", response_class=HTMLResponse)
async def read_member(request: Request):
    user = request.session.get('user')
    if not user:
       return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("member.html", {"request": request})

@app.get("/error")
async def error_page(request: Request, message: str = ""):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

@app.get("/signout")
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url="/", status_code=302)

@app.get("/square/{number}")
async def square(request: Request, number: int):
    value = number * number
    return templates.TemplateResponse("square.html", {"request": request, "square": value})