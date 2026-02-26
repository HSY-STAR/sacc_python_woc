from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy import Sequence
from app.database.database import Base

class User(Base):
    __tablename__ = "users"
    
    # 用户ID，主键，自增
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, index=True)
    
    # 用户名，唯一且必须
    username = Column(String(50), unique=True, index=True, nullable=False)
    
    # 邮箱，唯一且必须
    email = Column(String(100), unique=True, index=True, nullable=False)
    
    # 密码，必须
    password = Column(String(255), nullable=False)
    
    # 全名，可选
    full_name = Column(String(100))
    
    # 是否激活，默认为True
    is_active = Column(Boolean, default=True)
    
    # 创建时间，自动设置为当前时间
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 更新时间，更新时自动设置为当前时间
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())