from fastapi import APIRouter,HTTPException,Request
from schemas import CreateUserSchema,UserLoginSchema
from general import db_dependency
from models import User
from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime,timedelta
from pytz import timezone
from config import SECRET_KEY,ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=["auth"],prefix="/auth")



def generate_access_token(data: dict):
    data["exp"] = datetime.now(timezone('Asia/Tashkent')) + timedelta(minutes=30)
    token = jwt.encode(data,SECRET_KEY,ALGORITHM)
    return token

def decode_access_token(token: str):
    try:
        pyload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return pyload
    # except jwt.ExpiredSignatureError:
    #     raise HTTPException(status_code=403, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
    
def get_current_user(pyload,db):
    user_id = pyload.get("id")
    if not user_id:
        raise HTTPException(status_code=403, detail="Invalid token")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=403, detail="User not found")
    
    return user
    

@router.post("/signup",status_code=201,response_model=CreateUserSchema)
async def signup(user_schema: CreateUserSchema,db: db_dependency):
    
    if db.query(User).filter(User.username == user_schema.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(User).filter(User.email == user_schema.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
        
    user = User(
        username=user_schema.username,
        email=user_schema.email,
        password=pwd_context.hash(user_schema.password),
        first_name=user_schema.first_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
async def login(user_schema: UserLoginSchema, db: db_dependency,request: Request):
    print("REQ", request.headers)
    user = db.query(User).filter(User.username == user_schema.username).first()
    
    if not user or not pwd_context.verify(user_schema.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    data = {"id": user.id, "username": user.username}
    token = generate_access_token(data)
    
    return {"access_token": token, "type":"Bearer"}