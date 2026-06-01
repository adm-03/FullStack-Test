from fastapi import APIRouter, Depends, status
from api.dependencies.ai_response import get_ai_response_use_case
from usecases.ai_response import AIResponseUseCase


router = APIRouter(tags=["AI Integration"])


@router.get("/ai-tip", status_code=status.HTTP_200_OK)
async def get_ai_response(use_case: AIResponseUseCase = Depends(get_ai_response_use_case)):
    phrase = await use_case.execute()
    return {"status": "success", "ai_phrase": phrase}
