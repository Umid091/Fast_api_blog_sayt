# blog/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db import get_db
from blog.models import Post, Category, Comment
from blog.schema import (
    PostCreate, PostUpdate, PostResponse, PostDetailResponse,
    CategoryCreate, CategoryResponse,
    CommentCreate, CommentResponse
)
from users.models import User
from dependencies import get_current_user

router = APIRouter(prefix="/blog",tags=["Blog"])



@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Category).where(Category.name == data.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Bu kategoriya allaqachon mavjud")

    category = Category(name=data.name, description=data.description)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


@router.get("/categories", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    return result.scalars().all()



@router.post("/posts", response_model=PostResponse, status_code=201)
async def create_post(
    data: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = Post(
        title=data.title,
        content=data.content,
        category_id=data.category_id,
        author_id=current_user.id
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


@router.get("/posts", response_model=list[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post).where(Post.is_published == True)
    )
    return result.scalars().all()


@router.get("/posts/{post_id}", response_model=PostDetailResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post)
        .where(Post.id == post_id)
        .options(
            selectinload(Post.author),
            selectinload(Post.category),
            selectinload(Post.comments)
        )
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post topilmadi")
    return post


@router.patch("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    data: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post topilmadi")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu post sizniki emas")

    if data.title is not None:
        post.title = data.title
    if data.content is not None:
        post.content = data.content
    if data.category_id is not None:
        post.category_id = data.category_id
    if data.is_published is not None:
        post.is_published = data.is_published

    await db.commit()
    await db.refresh(post)
    return post


@router.delete("/posts/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post topilmadi")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu post sizniki emas")

    await db.delete(post)
    await db.commit()



@router.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=201)
async def create_comment(
    post_id: int,
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post topilmadi")

    comment = Comment(
        content=data.content,
        post_id=post_id,
        author_id=current_user.id
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


@router.delete("/posts/{post_id}/comments/{comment_id}", status_code=204)
async def delete_comment(
    post_id: int,
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Comment).where(Comment.id == comment_id, Comment.post_id == post_id)
    )
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment topilmadi")

    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu comment sizniki emas")

    await db.delete(comment)
    await db.commit()