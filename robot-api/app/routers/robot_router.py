from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.robot_service import RobotService, RobotServiceException


class SwitchFanRequestBody(BaseModel):
    mode: str = Field(title="Fan operation mode", description="Can either be 'proportional' or 'static'")
    value: Optional[int] = Field(desccription="Fan power in %, must be provided if mode is 'static", default=None)


class GetStateResponseBody(BaseModel):
    current_temperature: float = Field(description="Current temperature in Celsius")
    current_power_consumption: float = Field(description="Current power consumption in Watts")
    status: str = Field(description="Any one of 'idle', 'running', 'error', 'offline'")
    fan_speed: int = Field(description="Fan speed in %")
    uptime: str = Field(description="Total running time")
    logs: List[str] = Field(description="Error and warning logs")


class RobotRouter:
    def register(robot_service: RobotService) -> APIRouter:
        robot_router = APIRouter(prefix="/robot", tags=["robot"])

        @robot_router.post("/switch")
        async def switch_robot_on_off() -> None:
            try:
                await robot_service.switch()
            except RobotServiceException as error:
                raise HTTPException(403, detail=error.detail)

        @robot_router.post("/reset")
        async def reset_robot() -> None:
            try:
                await robot_service.reset()
            except RobotServiceException as error:
                raise HTTPException(403, detail=error.detail)
        
        @robot_router.post("/fan")
        async def switch_fan(fan_config: SwitchFanRequestBody) -> None:
            try:
                await robot_service.switch_fan(mode=fan_config.mode, value=fan_config.value)
            except RobotServiceException as error:
                raise HTTPException(400, detail=error.detail)

        @robot_router.get("", response_model=GetStateResponseBody)
        async def get_robot_state():
            state = await robot_service.get_state()
            return GetStateResponseBody(
                current_power_consumption=state.current_power_consumption,
                current_temperature=state.current_temperature,
                status=state.status,
                fan_speed=state.fan_speed,
                uptime=str(state.uptime),
                logs=state.logs,
            )

        return robot_router
