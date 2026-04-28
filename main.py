from fastapi import FastAPI
from users.router import router as users_router
from blog.router import router as blog_router
from ai.router import router as ai_router


app = FastAPI(
    title="Blog API",
    description="Blog sayt API",
    version="1.0.0"
)

app.include_router(users_router)
app.include_router(blog_router)
app.include_router(ai_router)


@app.get("/")
async def root():
    return {"message": "Blog API ishlamoqda!"}