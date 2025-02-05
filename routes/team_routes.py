from fastapi import APIRouter

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
    responses={404: {"description": "Not Found"}},
)
