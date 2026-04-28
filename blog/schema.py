# blog/schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True



class PostCreate(BaseModel):
    title: str
    content: str
    category_id: Optional[int] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    is_published: Optional[bool] = None


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    is_published: bool
    created_at: datetime
    updated_at: datetime
    author_id: int
    category_id: Optional[int] = None

    class Config:
        from_attributes = True


class PostDetailResponse(BaseModel):
    id: int
    title: str
    content: str
    is_published: bool
    created_at: datetime
    updated_at: datetime
    author: "UserShort"
    category: Optional[CategoryResponse] = None
    comments: list["CommentResponse"] = []

    class Config:
        from_attributes = True




class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    author_id: int
    post_id: int

    class Config:
        from_attributes = True



class UserShort(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


PostDetailResponse.model_rebuild()