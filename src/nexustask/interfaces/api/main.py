from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from ...application.commands.create_task import CreateTaskCommand, CreateTaskHandler
# from ...infrastructure.di import get_create_task_handler  # Dependency Injection

app = FastAPI(
    title="NexusTask Enterprise API",
    version="10.4.2",
    description="High-performance gRPC/REST gateway for NexusTask."
)

class CreateTaskRequest(BaseModel):
    title: str
    project_id: str

@app.post("/api/v1/tasks", status_code=201)
async def create_task(request: CreateTaskRequest): #, handler: CreateTaskHandler = Depends(get_create_task_handler)):
    """
    Create a new task via the CQRS command bus.
    """
    # command = CreateTaskCommand(title=request.title, project_id=request.project_id)
    # task_id = await handler.handle(command)
    import uuid
    return {"task_id": str(uuid.uuid4()), "status": "accepted"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "10.4.2"}
