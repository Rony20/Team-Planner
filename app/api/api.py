from .endpoints.projects import router as project_router
from .endpoints.employees import router as employees_router
from .endpoints.plugins import router as plugins_router
from .endpoints.requests import router as requests_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(project_router)
router.include_router(employees_router)
router.include_router(plugins_router)
router.include_router(requests_router)

