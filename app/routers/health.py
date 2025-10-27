from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/healthz")
def healthcheck():
    return {"status": "ok"}
