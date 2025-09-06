from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import get_db
from app.models.user import User
from app.services.auth import verify_password, create_access_token
from app.config import SECRET_KEY
from jose import jwt, JWTError
import os


router = APIRouter(prefix="/auth",tags=["auth"])
oauth2_scheme= OAuth2PasswordBearer(tokendUrl="token")

API_BASE_URL = os.getenv("API_BASE-URL","http://localgost:8000")


@router.post("/token")
async def login(
    form_data:QAuth2PasswordRequestForm = Depends(),
    db : AsyncSession = Depends(get_db)
):
    stmt : select(User).where(User.username == form_data.username)
    result = await db.execute(stmt)
    user=result.scalars.first()

    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="Incorrect username")
    
    access_token = create_access_token(data={"sub" : user.document_id})

    return {"acces_token" : access_token, "token_type":"bearer"}