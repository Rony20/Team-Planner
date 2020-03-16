from .endpoints.projects import router as project_router
from fastapi import APIRouter

router = APIRouter()

# include all project routes to api.py file
router.include_router(project_router)
