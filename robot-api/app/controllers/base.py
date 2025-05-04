import abc
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import List

import numpy as np


class RobotStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    OFFLINE = "offline"
    ERROR = "error"


@dataclass
class RobotState:
    current_temperature: np.float16
    current_power_consumption: np.float16
    status: str
    fan_speed: np.int8
    uptime: timedelta
    logs: List[str]


class RobotController(abc.ABC):
    started_at: datetime
    refresh_rate: int

    def __init__(self, refresh_rate: int) -> None:
        self.started_at = datetime.now()
        self.refresh_rate = refresh_rate

    def get_state(self) -> RobotState:
        raise NotImplementedError

    def set_fan_speed(self, speed: int) -> None:
        raise NotImplementedError
        
    def automate_fan_speed(self) -> None:
        raise NotImplementedError

    def switch(self) -> bool:
        raise NotImplementedError

    def reset(self) -> bool:
        raise NotImplementedError
