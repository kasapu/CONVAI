from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Conversation schemas
class ConversationBase(BaseModel):
    title: str
    ai_model: Optional[str] = "gpt-3.5-turbo"
    system_prompt: Optional[str] = None

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    ai_model: Optional[str] = None
    system_prompt: Optional[str] = None
    is_active: Optional[bool] = None

class Conversation(ConversationBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Message schemas
class MessageBase(BaseModel):
    content: str
    role: str  # 'user', 'assistant', 'system'
    message_metadata: Optional[str] = None

class MessageCreate(MessageBase):
    conversation_id: int

class Message(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Chat schemas
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    ai_model: Optional[str] = "gpt-3.5-turbo"
    system_prompt: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    conversation_id: int
    message_id: int

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None