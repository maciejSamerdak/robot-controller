import logging
from enum import Enum
from typing import Optional

from app.controllers.base import RobotController, RobotState


class FanModes(Enum):
    PROPORTIONAL = "proportional"
    STATIC = "static"


class RobotServiceException(Exception):
    def __innit__(self, detail):
        self.detail = detail


class RobotService:
    controller: RobotController

    def __init__(self, controller: RobotController) -> None:
        self.controller = controller
        self._logger = logging.getLogger("RobotService")

    async def switch(self) -> None:
        self._logger.info("Switching robot mode")
        is_switch_successful = self.controller.switch()
        if not is_switch_successful:
            raise RobotServiceException("Robot cannot be switched on/off from current state")

    async def reset(self) -> None:
        self._logger.info("Resetting robot")
        is_reset_successful = self.controller.reset()
        if not is_reset_successful:
            raise RobotServiceException("Robot cannot be reset from current state")

    async def switch_fan(self, mode: str, value: Optional[int]) -> None:
        self._logger.info("Setting fan configuration")
        match mode:
            case FanModes.PROPORTIONAL.value:
                self.controller.automate_fan_speed()
                self._logger.info("Fan operation is set to auto")
            case FanModes.STATIC.value:
                if value >= 0 and value <= 100:
                    self.controller.set_fan_speed(value)
                    self._logger.info(f"Fan operation is set to static speed at {value}%")
                else:
                    message = "Fan speed out of range (0-100)"
                    self._logger.error(message)
                    raise RobotServiceException(message)
            case _:
                message = f"Incorrect fan operation mode: '{mode}'"
                self._logger.error(message)
                raise RobotServiceException(message)

    async def get_state(self) -> RobotState:
        self._logger.info("Obtaining robot state")
        return self.controller.get_state()
