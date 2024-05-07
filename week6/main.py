from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# from typing import Annotated

import mysql.connector
from mysql.connector import Error

app = FastAPI() # FastAPI 物件

app.add_middleware(SessionMiddleware, secret_key="123456")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/signup")
async def signup(request: Request, name: str = Form(default=None), username: str = Form(default=None), password: str = Form(default=None)):
    con, cursor = connectMySQLserver()
    if cursor is not None:
         # 取得一筆資料
        cursor.execute("select username from member where username = %s",(username,))
        data=cursor.fetchone()
        if data:
             # 帳號已註冊
            error_message = "此帳號已註冊，請重新註冊"
            con.close()
            return RedirectResponse(url=f'/error?message={error_message}', status_code=301)
        else:
            cursor.execute("insert into member(name, username, password)values(%s, %s, %s)",(name, username, password))
            con.commit()
            # 關閉資料庫連線
            con.close()
            return RedirectResponse(url='/', status_code=303)
    else:
        error_message = "資料庫連線異常，請通知系統管理員"
        return RedirectResponse(url=f'/error?message={error_message}', status_code=301)

@app.post("/signin")
async def signin(request: Request, username: str = Form(default=None), password: str = Form(default=None)):
    con, cursor = connectMySQLserver()
    if cursor is not None:
         # 取得一筆資料
        cursor.execute("select id, name, username from member where username = %s and password = %s",(username, password))
        data=cursor.fetchone()
        # 關閉資料庫連線
        con.close()
         # if username == "test" and password == "test":
        if data:
            # print(data[0], data[1], data[2])
            request.session['id'] = data[0]
            request.session['name'] = data[1]
            request.session['username'] = data[2]
            return RedirectResponse(url='/member', status_code=303)
        else:
            # 帳號密碼錯誤
            error_message = "帳號或密碼輸入錯誤"
            return RedirectResponse(url=f'/error?message={error_message}', status_code=301)
    else:
        error_message = "資料庫連線異常，請通知系統管理員"
        return RedirectResponse(url=f'/error?message={error_message}', status_code=301)

@app.get("/member")
async def read_member(request: Request):
    user = request.session.get('username')
    if not user:
       return RedirectResponse(url="/")   
    
    con, cursor = connectMySQLserver()
    if cursor is not None:
        cursor.execute("select member.name, content, member_id, message.id from message join member on member.id = message.member_id order by message.time desc")
        data=cursor.fetchall()
        msg_from_db = list(data)
        # print(msg_from_db)
        # 關閉資料庫連線
        con.close()
        # 將msg_from_db放入字典中
        context = {"request": request, "msg_from_db": msg_from_db}
        return templates.TemplateResponse("member.html", context)
    else:
        error_message = "資料庫連線異常，請通知系統管理員"
        return RedirectResponse(url=f'/error?message={error_message}', status_code=301)

@app.get("/error")
async def error_page(request: Request, message: str = ""):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

@app.get("/signout")
async def logout(request: Request):
    request.session.pop('username', None)
    return RedirectResponse(url="/")

@app.post("/createMessage")
async def createmsg(request: Request, message: str = Form(...)):
    con, cursor = connectMySQLserver()
    if cursor is not None:
         # 將資料塞入message table
        cursor.execute("insert into message(member_id, content)values(%s, %s)",(request.session['id'], message))
        con.commit()
        # 關閉資料庫連線
        con.close()
        return RedirectResponse(url='/member', status_code=303)
    else:
        error_message = "資料庫連線異常，請通知系統管理員"
        return RedirectResponse(url=f'/error?message={error_message}', status_code=301)

@app.post("/deleteMessage")
async def delmsg(request: Request, message_id: int = Form(...)):
    # 刪除前要先確認是不是使用者的帳號訊息
    con, cursor = connectMySQLserver()
    if cursor is not None:
         # 取得一筆資料
        cursor.execute("select member_id from message where id = %s",(message_id,))
        data=cursor.fetchone()
        if data:
           member_id=data[0]
           # print(member_id) 
           # 透過查詢message table中的member_id來比對確認身分
           user_id = request.session.get('id')
           if member_id!=user_id:
              error_message = "無效的資料刪除操作"
              return RedirectResponse(url=f'/error?message={error_message}', status_code=301)
           con.close()
        else:
           error_message = "沒有此筆留言資料，無效的資料刪除操作"
           con.close()
           return RedirectResponse(url=f'/error?message={error_message}', status_code=301)
    else:
        error_message = "資料庫連線異常，請通知系統管理員"
        return RedirectResponse(url=f'/error?message={error_message}', status_code=301)


    con, cursor = connectMySQLserver()
    if cursor is not None:
         # 刪除留言訊息
        cursor.execute("delete from message WHERE id = %s AND member_id = %s", (message_id, member_id))
        con.commit()
        # 關閉資料庫連線
        con.close()
        return RedirectResponse(url='/member', status_code=303)
    else:
        error_message = "資料庫連線異常，請通知系統管理員"
        return RedirectResponse(url=f'/error?message={error_message}', status_code=301)

def connectMySQLserver():
    try:
        # 連線到資料庫
        con = mysql.connector.connect(
            user="root",
            password="12345678",
            host="localhost",
            database="website"
        )
        if con.is_connected():
            #print("資料庫連線成功")
            cursor = con.cursor()  
            return con, cursor
        else:
            print("資料庫連線未成功")
            return None, None 
    except Error as e:
        print("資料庫連線失敗:", e)
        return None, None

