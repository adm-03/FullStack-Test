from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import asyncio

import aiosmtplib
from api.schemas import MailSchema
from api.config import settings

logger = logging.getLogger(__name__)


class SendMailUseCase:

    async def _send_email(self, to_email: str, subject: str, body_text: str) -> None:
        message = MIMEMultipart()
        message["From"] = settings.SMTP_USER
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body_text, "plain", "utf-8"))

        # use_tls True is appropriate for SMTPS on port 465
        async with aiosmtplib.SMTP(
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            use_tls=True,
        ) as smtp:
            await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            await smtp.send_message(message)

    async def execute(self, payload: MailSchema) -> None:
        try:
            logger.info(f"Началась фоновая отправка писем для {payload.email}")

            owner_text = (
                f"Новая заявка с формы обратной связи!\n\n"
                f"Имя: {payload.name}\n"
                f"Телефон: {payload.phone}\n"
                f"Email: {payload.email}\n"
                f"Комментарий:\n{payload.comment}"
            )

            user_text = (
                f"Здравствуйте, {payload.name}!\n\n"
                f"Мы получили ваше обращение и уже взяли его в работу.\n"
                f"Копия вашего сообщения:\n\"{payload.comment}\"\n\n"
                f"С уважением, команда нашего сайта."
            )

            smtp_timeout = getattr(settings, "SMTP_TIMEOUT", 10)
            max_attempts = 2

            recipients = [
                (settings.SMTP_USER, "[Новая заявка] Форма", owner_text),
                (payload.email, "Ваше обращение принято", user_text),
            ]

            for to_email, subject, body in recipients:
                attempt = 0
                while attempt < max_attempts:
                    try:
                        attempt += 1
                        await asyncio.wait_for(self._send_email(to_email, subject, body), timeout=smtp_timeout)
                        logger.info(f"Письмо успешно отправлено на {to_email}")
                        break
                    except asyncio.TimeoutError:
                        logger.warning(f"Timeout при отправке на {to_email}, попытка {attempt}/{max_attempts}")
                        if attempt >= max_attempts:
                            raise
                        await asyncio.sleep(1 * attempt)
                    except Exception as e:
                        logger.error(f"Ошибка при отправке письма на {to_email}: {e}", exc_info=True)
                        if attempt >= max_attempts:
                            raise
                        await asyncio.sleep(1 * attempt)

            logger.info(f"Фоновая отправка для {payload.email} успешно завершена")

        except Exception as e:
            logger.error(f"Критическая ошибка при фоновой отправке почты: {e}", exc_info=True)
