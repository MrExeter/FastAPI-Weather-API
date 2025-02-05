from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
    responses={404: {"description": "Not Found"}},
)
