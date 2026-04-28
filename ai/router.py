# ai/router.py
import os
from groq import Groq
from fastapi import APIRouter, Depends, HTTPException
from dotenv import load_dotenv
from ai.schema import ChatRequest, ChatResponse
from users.models import User
from dependencies import get_current_user

load_dotenv()

router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"]
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
Sen "Blog API" loyihasi uchun yordamchi assistantsan.

Bu loyiha haqida:
- FastAPI asosida qurilgan blog platformasi
- Foydalanuvchilar ro'yxatdan o'tib, login qila oladi
- Blog postlar yozish, tahrirlash, o'chirish mumkin
- Postlarga comment qoldirish mumkin
- Kategoriyalar mavjud

Mavjud endpointlar:
- POST /users/register — ro'yxatdan o'tish
- POST /users/login — login qilish
- GET /blog/posts — barcha postlarni ko'rish
- POST /blog/posts — yangi post yaratish
- GET /blog/posts/{id} — bitta postni ko'rish
- PATCH /blog/posts/{id} — postni tahrirlash
- DELETE /blog/posts/{id} — postni o'chirish
- POST /blog/posts/{id}/comments — comment qoldirish
- POST /blog/categories — kategoriya yaratish
- GET /blog/categories — kategoriyalarni ko'rish

QOIDALAR:
1. FAQAT shu blog loyihasi haqidagi savollarga javob ber
2. Agar savol loyihaga aloqador bo'lmasa:
   "Kechirasiz, men faqat Blog loyihasi haqida javob bera olaman" de
3. Texnik savollar, kod, API ishlatish haqida batafsil tushuntir
4. O'zbek tilida javob ber
"""

@router.post("/chat", response_model=ChatResponse)
async def chat(
    data: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": data.message}
            ],
            max_tokens=1000
        )

        return ChatResponse(reply=response.choices[0].message.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI xatosi: {str(e)}")