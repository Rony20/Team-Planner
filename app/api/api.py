from .endpoints.projects import router as project_router
from .endpoints.employees import router as employees_router
from .endpoints.plugins import router as plugins_router
from .endpoints.requests import router as requests_router
from fastapi import APIRouter, WebSocket

router = APIRouter()

router.include_router(project_router)
router.include_router(employees_router)
router.include_router(plugins_router)
router.include_router(requests_router)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    clients = []
    await websocket.accept()
    clients.append(websocket.client)
    print(websocket.client)
    while True:
        data = await websocket.receive_json()
        print(data)
        await websocket.send_text("hello")
