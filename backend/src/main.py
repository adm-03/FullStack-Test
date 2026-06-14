from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groq import AsyncGroq

from api.config import settings
from api.routers import ai_response_router, send_mail_router

@asynccontextmanager
async def lifespan(app: FastAPI):
  
    
    ai_client = AsyncGroq(api_key=settings.GROQ_API_KEY)
    app.state.ai_client = ai_client
    
    print("🚀 Официальный клиент Groq ИИ успешно запущен в lifespan")
    yield
    
    await ai_client.close()


app = FastAPI( title="Portfolio Presentation API", description="Backend для формы обратной связи и ИИ-ассистента", lifespan=lifespan)

origins = [
    "https://adm-03.github.io",  # 👈 Замени на точный URL твоего GitHub Pages
    "http://localhost:5500",         # Для тестов дома через VS Code Live Server
    "http://127.0.0.1:5500",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_response_router, prefix="/api")
app.include_router(send_mail_router, prefix="/api")

