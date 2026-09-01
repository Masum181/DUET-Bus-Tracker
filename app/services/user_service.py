from app.repositories import user_repositories


from app.schemas.base import BaseResponse

from fastapi import status, HTTPException
from datetime import datetime, timezone

from app.core.hashing import Hash

from app.schemas.user import (
    User as UserSchema,
    ShowUser,
    ResponseUser
)

from app.schemas.base import BaseResponse, Meta
from app.core.context import get_request_id

from app.enums.user_enums import DriverStatus

async def create_new_user(db, payload):
    user = await user_repositories.get_user(db, email=payload.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    data = {
        "username":payload.name,
        "email":payload.email,
        "password":Hash.hash(payload.password),
        "dob":payload.dob,
        'mobile':payload.mobile,
        "gender":payload.gender,
        "role":payload.role
    }
    new_user = await user_repositories.create_user(db, data)

    return ResponseUser(
        status=status.HTTP_201_CREATED,
        success=True,
        message="User created successfully",
        lang="en",
        data=ShowUser(
            name=new_user.username,
            email=new_user.email,
            mobile=new_user.mobile,
            dob=new_user.dob,
            gender=new_user.gender,
            role=new_user.role
        ),
        meta=Meta(
            request_id=get_request_id(),
            timestamp = datetime.now(tz=timezone.utc)
        )
    )

async def create_new_student(db, payload):
    user = await user_repositories.get_user(db, email=payload.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    data = {
        "username":payload.name,
        "email":payload.email,
        "password":Hash.hash(payload.password),
        "dob":payload.dob,
        'mobile':payload.mobile,
        "gender":payload.gender,
        "role":payload.role,
    }
    new_user = await user_repositories.create_user(db, data)
    user_info = {
        "user_id":new_user.id,
        "full_name":payload.name,
        "status":DriverStatus.ACTIVE,
        "address":payload.address,
        "student_id":payload.student_id,
        "current_semester":payload.current_semester
    }
    await user_repositories.create_student_info(db, user_info)
    return ResponseUser(
        status=status.HTTP_201_CREATED,
        success=True,
        message="User created successfully",
        lang="en",
        data=ShowUser(
            name=new_user.username,
            email=new_user.email,
            mobile=new_user.mobile,
            dob=new_user.dob,
            gender=new_user.gender,
            role=new_user.role
        ),
        meta=Meta(
            request_id=get_request_id(),
            timestamp = datetime.now(tz=timezone.utc)
        )
    )

async def create_new_driver(db, payload):    
    user = await user_repositories.get_user(db, email=payload.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    data = {
        "username":payload.name,
        "email":payload.email,
        "password":Hash.hash(payload.password),
        "dob":payload.dob,
        'mobile':payload.mobile,
        "gender":payload.gender,
        "role":payload.role,
    }
    new_user = await user_repositories.create_user(db, data)
    user_info = {
        "user_id":new_user.id,
        "full_name":payload.name,
        "status":DriverStatus.INACTIVE,
        "address":payload.address,
        "license_plate":payload.license_plate,
        "license_plate_expiry":payload.license_plate_expiry,
        "emergency_contact_name":payload.emergency_contact_name,
        "emergency_contact_phone":payload.emergency_contact_phone
    }
    await user_repositories.create_driver_info(db, user_info)
    return ResponseUser(
        status=status.HTTP_201_CREATED,
        success=True,
        message="User created successfully",
        lang="en",
        data=ShowUser(
            name=new_user.username,
            email=new_user.email,
            mobile=new_user.mobile,
            dob=new_user.dob,
            gender=new_user.gender,
            role=new_user.role
        ),
        meta=Meta(
            request_id=get_request_id(),
            timestamp = datetime.now(tz=timezone.utc)
        )
    )

async def create_new_session(db,request, user_id, refresh_token, expire):
    # Extract device info
    ip_address = request.headers.get(
        "x-forwarded-for", request.client.host
    )
    user_agent = request.headers.get("user-agent")

    session = {
        "user_id":user_id,
        "refresh_token":refresh_token,
        "device_name":"unknown",
        "device_type":"unknown",
        "ip_address":ip_address,
        "user_agent":user_agent,
        "expires_at":expire,
        "is_revoked":False,
        "created_at":datetime.now(timezone.utc),
        "last_used_at":datetime.now(timezone.utc)
    }

    session = await user_repositories.create_session(db, session)
    return session


