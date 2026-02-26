from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# 基础用户模式 - 包含所有用户共有的字段
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="用户名，3-50个字符")
    email: EmailStr = Field(..., description="有效的邮箱地址")
    full_name: Optional[str] = Field(None, max_length=100, description="全名，可选，最多100字符")

# 创建用户的模式 - 包含密码字段
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="密码，至少6个字符")

# 更新用户的模式 - 所有字段都是可选的
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=6)
    is_active: Optional[bool] = None

# 响应中的用户模式 - 不包含密码，包含所有数据库字段
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # 允许从ORM对象创建

# 用户登录模式
class UserLogin(BaseModel):
    username: str
    password: str