from fastapi import APIRouter, Depends, status, HTTPException, Form
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.base import get_db
from app.models.user import User
from app.schemas.user import (
    User as UserSchema,
    StudentSchema,
    DriverSchema
)
from app.core.hashing import Hash
from app.core.outh2 import get_current_user

from app.services import user_service

router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(payload:UserSchema, db:Annotated[AsyncSession, Depends(get_db)]):
    # Check if user with the same email already exists
    response = await user_service.create_new_user(db, payload)
    return response

@router.post("/register/student", status_code=status.HTTP_201_CREATED)
async def create_student(payload:StudentSchema, db:Annotated[AsyncSession, Depends(get_db)]):
    # Check if user with the same email already exists
    response = await user_service.create_new_student(db, payload)
    return response

@router.post("/register/driver", status_code=status.HTTP_201_CREATED)
async def create_driver(payload:DriverSchema, db:Annotated[AsyncSession, Depends(get_db)]):
    # Check if user with the same email already exists
    response = await user_service.create_new_driver(db, payload)
    return response

