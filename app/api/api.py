from .endpoints.projects import router as project_router
from .endpoints.employees import router as employees_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(project_router)
router.include_router(employees_router)

