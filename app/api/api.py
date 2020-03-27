from fastapi import APIRouter

from .endpoints.employees import router as employees_router

router = APIRouter()

router.include_router(employees_router)
