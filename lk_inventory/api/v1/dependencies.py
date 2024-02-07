import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from lk_inventory.api.v1.db_queries import get_user_query
from lk_inventory.app.db import get_session

security = HTTPBasic()


async def auth(credentials: HTTPBasicCredentials = Depends(security), session: AsyncSession = Depends(get_session)):
    async with session.begin():
        user = await get_user_query(credentials.username, session)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Login is not found')
        if not bcrypt.hashpw(credentials.password.encode('utf-8'), user.password) == user.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Basic"},
            )
