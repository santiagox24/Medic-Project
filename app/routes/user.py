from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.services.auth import get_password_hash

router = APIRouter(prefix="/user",tags=("users"))

@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate,
    db: AsyncSession = Depends (get_db)
):
    stmt = select(User).where(User.document_id == user.document_id)
    result = await db.execute (stmt)
    existing_user = result.scalars().first()


    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Theres a user that alredy exists with this document id."
        )

    hashed_password = get_password_hash(user.password)

    db_user = User(**user.dict(exclude={"password"}),hashed_password=hashed_password)
    db.add(db_user)

    try:
        await db.commit()
        await db.refresh(db_user)

        return {
            "Message" : "Usuario registrado correctamente."
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar al usuario : {str(e)}"
            )