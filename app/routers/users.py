from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.middleware.rate_limit import limiter, RateLimitConfig

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "未找到"}}
)


@router.get("/", response_model=List[UserResponse])
@limiter.limit(RateLimitConfig.ENDPOINT_LIMITS["/users/"]["GET"])
async def get_users(
    request: Request,  # 必须添加request参数
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """获取用户列表（限流：每分钟30次）"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
@limiter.limit(RateLimitConfig.ENDPOINT_LIMITS["/users/{user_id}"]["GET"])
async def get_user(
    request: Request,  # 必须添加request参数
    user_id: int, 
    db: Session = Depends(get_db)
):
    """获取单个用户（限流：每分钟30次）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户ID {user_id} 不存在"
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(RateLimitConfig.ENDPOINT_LIMITS["/users/"]["POST"])
async def create_user(
    request: Request,  # 必须添加request参数
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    """创建新用户（限流：每分钟10次）"""
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已被注册"
        )
    
    # 检查邮箱是否已存在
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 创建新用户
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
@limiter.limit(RateLimitConfig.ENDPOINT_LIMITS["/users/{user_id}"]["PUT"])
async def update_user(
    request: Request,  # 必须添加request参数
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db)
):
    """更新用户信息（限流：每分钟10次）"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户ID {user_id} 不存在"
        )
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(RateLimitConfig.ENDPOINT_LIMITS["/users/{user_id}"]["DELETE"])
async def delete_user(
    request: Request,  # 必须添加request参数
    user_id: int, 
    db: Session = Depends(get_db)
):
    """删除用户（限流：每分钟5次，最严格）"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户ID {user_id} 不存在"
        )
    
    db.delete(db_user)
    db.commit()
    return None


@router.get("/search/", response_model=List[UserResponse])
@limiter.limit(RateLimitConfig.ENDPOINT_LIMITS["/users/search/"]["GET"])
async def search_users(
    request: Request,  # 必须添加request参数
    username: Optional[str] = None,
    email: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """搜索用户（限流：每分钟20次）"""
    query = db.query(User)
    
    if username:
        query = query.filter(User.username.contains(username))
    if email:
        query = query.filter(User.email.contains(email))
    
    users = query.offset(skip).limit(limit).all()
    return users