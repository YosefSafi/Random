from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Any
from ...application.commands.create_task import CreateTaskCommand, CreateTaskHandler
from ...application.queries.get_tasks import GetTasksQuery, GetTasksHandler
from ...infrastructure.di import get_create_task_handler, get_tasks_handler, init_db

from strawberry.fastapi import GraphQLRouter
from .graphql import schema

app = FastAPI(
    title="NexusTask Enterprise API",
    version="10.4.2",
    description="High-performance gRPC/REST gateway for NexusTask."
)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.on_event("startup")
async def startup_event():
    await init_db()

class CreateTaskRequest(BaseModel):
    title: str
    project_id: str

@app.post("/api/v1/tasks", status_code=201)
async def create_task(request: CreateTaskRequest, handler: CreateTaskHandler = Depends(get_create_task_handler)):
    """
    Create a new task via the CQRS command bus.
    """
    command = CreateTaskCommand(title=request.title, project_id=request.project_id)
    task_id = await handler.handle(command)
    return {"task_id": task_id, "status": "accepted"}

@app.get("/api/v1/tasks")
async def list_tasks(limit: int = 100, offset: int = 0, handler: GetTasksHandler = Depends(get_tasks_handler)):
    """
    List tasks from the persistent store.
    """
    query = GetTasksQuery(limit=limit, offset=offset)
    tasks = await handler.handle(query)
    return tasks

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "10.4.2"}
