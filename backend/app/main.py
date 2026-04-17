from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import current_user_id
from app.config import get_settings
from app.llm import summarise_consultation
from app.schemas import ConsultationRequest, ConsultationResponse

settings = get_settings()
app = FastAPI(title="Health App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "env": settings.app_env}


@app.post("/api/consultations", response_model=ConsultationResponse)
async def create_consultation(
    body: ConsultationRequest,
    user_id: str = Depends(current_user_id),
) -> ConsultationResponse:
    del user_id  # reserved for future per-user persistence / rate limiting
    return await summarise_consultation(body.notes)
