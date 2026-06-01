from fastapi import Request
from usecases import AIResponseUseCase


def get_ai_response_use_case(
    request: Request
) -> AIResponseUseCase:
    return AIResponseUseCase(request.app.state.ai_client)

