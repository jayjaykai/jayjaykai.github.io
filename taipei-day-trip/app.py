from typing import Optional, Union
from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from jose import ExpiredSignatureError, JWTError
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from mysql.connector.pooling import MySQLConnectionPool
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone

secret_key="dfjewkjfejwfjiewfjoewjfioewjf"

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/static", StaticFiles(directory="/home/ubuntu/tdt/static"), name="static")
load_dotenv()
# load_dotenv('/home/ubuntu/tdt/.env')
# 設定可存取資源的來源端點
origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有HTTP方法
    allow_headers=["*"],  # 允許所有HTTP headers
)


print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_USER:", os.getenv("DB_USER"))
print("DB_PASSWORD:", os.getenv("DB_PASSWORD"))
print("DB_NAME:", os.getenv("DB_NAME"))

pool_size_str = os.getenv("POOL_SIZE")
if pool_size_str is None:
    pool_size = 5  
else:
    pool_size = int(pool_size_str)

pool = MySQLConnectionPool(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    pool_size=pool_size)

# JWT setting
SECRET_KEY = "sfegrehrtwerwet54h5jtyfgdfgergerg"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/auth")

# 自定義User資料 model
class User(BaseModel):
    email: str
    password: str
    
class SignOnInfo(BaseModel):
    name: str
    email: str
    password: str

class TokenData(BaseModel):
    userID: str
    name: str
    email: str    

class BookingData(BaseModel):
    attraction_id: int
    date: Optional[str] = None
    travel_time: str
    tour_price: int

def hash_password(text):
    mode = hashlib.sha256()
    mode.update((text+secret_key).encode())
    return mode.hexdigest()

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str = Depends(oauth2_scheme))-> Union[TokenData, JSONResponse]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("userID")
        username: str = payload.get("username")
        email: str = payload.get("email")
        if user_id is None or username is None or email is None:
            return JSONResponse(
                status_code=403,
                content={"error": True, "message": "未登入系統，拒絕存取"}
            )
        return TokenData(userID=user_id, name=username, email=email)
    except (ExpiredSignatureError, JWTError):
        return JSONResponse(
            status_code=403,
            content={"error": True, "message": "未登入系統，拒絕存取"}
        )
    
@app.put("/api/user/auth")
async def login(user: User):
    con, cursor = connectMySQLserver()
    if cursor is not None:
        try:
            # print(user.email)
            # print(user.password)
            # print(hash_password(user.password))
            cursor.execute("select id,name,email from User where email = %s and password = %s", (user.email, hash_password(user.password)))
            data = cursor.fetchone()

            if data:
                print(f"User: {data[0]}")
                print(f"User email: {user.email}")
                access_token = create_access_token(
                    data={"userID": str(data[0]), "username": data[1], "email": data[2]}, expires_delta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
                )
                return {"token": access_token}
            else:
                return JSONResponse(status_code=400, content={"error": True, "message": "登入失敗，帳號或密碼錯誤或其他原因"})
        except Exception as err:
            return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
        finally:
            con.close()
    else:
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@app.post("/api/user")
async def signOn(user: SignOnInfo):
    con, cursor = connectMySQLserver()
    if cursor is not None:
        try:
            print(user.name)
            print(user.email)
            print(user.password)
            cursor.execute("select name from User where email = %s", (user.email,))
            data = cursor.fetchone()
            if data:
                return JSONResponse(status_code=400, content={"error": True, "message": "註冊失敗，重複的 Email 或其他原因"})
            else:
                hashed_pwd = hash_password(user.password)
                cursor.execute("insert into User(name, email, password) values(%s, %s, %s)", (user.name, user.email, hashed_pwd))
                con.commit()
                return JSONResponse(status_code=200, content={"ok": True})
        except Exception as err:
            return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
        finally:
            con.close()
    else:
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

@app.get("/api/user/auth")
async def checkUser(token_data: TokenData = Depends(verify_jwt_token)) :
    # if isinstance(token_data, FileResponse):
    #     return token_data 
    # print(token_data)
    result = {
                "id": token_data.userID,
                "name": token_data.name,
                "email": token_data.email
             }

    return {"data": result}

@app.post("/api/booking")
async def bookEvent(booking_data: BookingData, token_data: TokenData = Depends(verify_jwt_token)):
    con, cursor = connectMySQLserver()
    if cursor is not None:
        try: 
            cursor.execute("insert into Booking(attractionId, date, timeSlot, price) values(%s, %s, %s, %s)", 
                           (booking_data.attraction_id, 
                            booking_data.date if booking_data.date else None, 
                            booking_data.travel_time, 
                            booking_data.tour_price))
            con.commit()
            return JSONResponse(status_code=200, content={"ok": True})
        except Exception as err:
            return JSONResponse(status_code=500, content={"error": True, "message": "建立失敗，輸入不正確或其他原因"})
        finally:
            con.close()
    else:
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})

#*** Static Pages (Never Modify Code in this Block) ***
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")
#*** Static Pages (Never Modify Code in this Block) ***

@app.get("/api/attractions")
def get_attractions(page: int = 0, keyword: Optional[str] = Query(None)):
    con, cursor = connectMySQLserver()
    if cursor is not None:
       try:
            offset = page * 12
            query = "SELECT * FROM Attraction"
            params = []
            
            if keyword:
                query += " WHERE name LIKE %s OR mrt = %s"
                params.extend([f"%{keyword}%", keyword])
                
            query += " LIMIT %s OFFSET %s"
            params.extend([12, offset])
            
            print(query)
            cursor.execute(query, tuple(params))
            attractions = cursor.fetchall()
            
            if not attractions:
                return {"nextPage": None, "data": []}
            
            if len(attractions) == 12:
                next_page = page + 1
            else:
                next_page = None
            
            result = []
            for attraction in attractions:
                images = []
                id, name, category, description, address, direction, mrt, latitude, longitude, image_urls, rate, avBegin, avEnd = attraction
                if image_urls:
                    urls = image_urls.split(',')
                    for url in urls:
                        if url.lower().endswith(('jpg', 'png')):
                            images.append(url)
                else:
                    images = []

                result.append({
                    "id": id,
                    "name": name,
                    "category": category,
                    "description": description,
                    "address": address,
                    "transport": direction,
                    "mrt": mrt,
                    "lat": latitude,
                    "lng": longitude,
                    "images": images
                })
            
            return {"nextPage": next_page, "data": result}
       except Exception as err:
            return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
       finally:
            con.close()
    else:
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
    
@app.get("/api/attraction/{attractionId}")
def get_attraction(attractionId: int):
    con, cursor = connectMySQLserver()
    if cursor is not None:
        try:
            cursor.execute("SELECT * FROM Attraction WHERE id = %s", (attractionId,))
            attraction = cursor.fetchone()
            
            if not attraction:
                return JSONResponse(status_code=400, content={"error": True, "message": "景點編號不正確"})
                #return {"error": True,"message": "景點編號不正確"}

            id, name, category, description, address, direction, mrt, latitude, longitude, image_urls, rate, avBegin, avEnd = attraction
            result = []
            if image_urls:
                images = []
                urls = image_urls.split(',')
                for url in urls:
                    if url.lower().endswith(('jpg', 'png')):
                        images.append(url)
            else:
                images = []

            result = {
                "id": id,
                "name": name,
                "category": category,
                "description": description,
                "address": address,
                "transport": direction,
                "mrt": mrt,
                "lat": latitude,
                "lng": longitude,
                "images": images
            }

            return {"data": result}
        except Exception as err:
            return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
        finally:
            con.close()
    else:
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
        #return {"error": True, "message": "無法連接到資料庫"}

@app.get("/api/mrts")
def get_mrts():
    con, cursor = connectMySQLserver()
    if cursor is not None:
        try:
            cursor.execute("SELECT mrt, count(mrt) FROM Attraction GROUP BY mrt ORDER BY count(mrt) DESC")
            rows = cursor.fetchall()
            mrts = []
            for row in rows:
                if row[0] is not None:
                    mrts.append(row[0])
            return mrts
        except Exception as err:
            return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
        finally:
            con.close()
    else:
        return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤"})
    
#程式關閉或登出後將Connection Pool關閉
def close_connection_pool():
    pool.close()

def connectMySQLserver():
    try:
        con = pool.get_connection()
        if con.is_connected():
            cursor = con.cursor()
            # print("資料庫連線成功")
            return con, cursor
        else:
            print("資料庫連線未成功")
            return None, None 
    
    except Error as e:
        print("資料庫連線失敗:", e)
        return None, None