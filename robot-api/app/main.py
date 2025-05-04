from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import MockRobotController
from app.routers import RobotRouter
from app.services import RobotService
from app.settings import settings


@asynccontextmanager
async def lifespan(_app: FastAPI):
    robot_controller = MockRobotController(refresh_rate=settings.refresh_rate)
    robot_service = RobotService(robot_controller)
    _app.include_router(RobotRouter.register(robot_service))
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
