from dataclasses import dataclass
import logging
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

@dataclass
class AIResponseUseCase:
    _client: AsyncOpenAI

    async def execute(self) -> str:
        try:
            logger.info("Запрос к ИИ через официальный SDK Groq")

            completion = await self._client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Ты — поддерживающий ИИ-ассистент на сайте разработчика. "
                            "Твой ответ должен быть строго на русском языке, максимум 1 короткое предложение. "
                            "Сгенерируй случайную, яркую, вдохновляющую мысль или совет дня для программиста. "
                            "Пиши сразу текст фразы, без кавычек и лишних слов."
                        )
                    },
                    {
                        "role": "user",
                        "content": "Выдай случайную фразу дня."
                    }
                ],
                max_tokens=80,
                temperature=0.85,
            )

            first_choice = completion.choices[0]
            phrase = getattr(first_choice.message, "content", None) or first_choice.message["content"]
            return (phrase or "").strip().replace('"', '')

        except Exception as e:
            logger.error(f"Сбой Groq API, сработал защитный Fallback: {e}", exc_info=True)
            import random
            return random.choice([
                "Чистый код — это поэзия, которую понимает машина.",
                "Маленькие шаги каждый день ведут к большим результатам.",
                "Архитектура — это выбор того, какими вещами можно пожертвовать."
            ])
