from fastapi import APIRouter, BackgroundTasks, status
from api.schemas import MailSchema
from usecases import SendMailUseCase

router = APIRouter(tags=["SendMail"])


@router.post("/send_mail", status_code=status.HTTP_202_ACCEPTED)
async def send_mail(payload: MailSchema, background_tasks: BackgroundTasks):
    mail_service = SendMailUseCase()
    background_tasks.add_task(mail_service.execute, payload)
    return {
        "status": "accepted",
        "message": "Ваша заявка принята и обрабатывается в фоне."
    }

