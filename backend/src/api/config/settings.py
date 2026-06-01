from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
   

    SMTP_HOST: str = "smtp.mail.ru"
    SMTP_PORT: int = 465
    SMTP_USER: str = "your_bot_mail@mail.ru"
    SMTP_PASSWORD: str = "your_app_password"

    GROQ_API_KEY: str = "mock_gsk_key"


    model_config = SettingsConfigDict(
        env_file=".env",            
        env_file_encoding="utf-8",  
        extra="ignore"              
    )

settings = Settings()
