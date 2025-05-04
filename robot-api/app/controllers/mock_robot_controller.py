import asyncio
import logging
import math
import random
from datetime import datetime, timedelta
from threading import RLock

import numpy as np

from app.controllers import RobotController, RobotState, RobotStatus
from app.settings import settings


class MockRobotController(RobotController):
    MAX_FAN_COOLING = settings.mock_max_fan_cooling
    TEMPERATURE_RANGE = settings.mock_temperature_range
    TEMPERATURE_THRESHOLD = settings.mock_temperature_threshold
    OFFLINE_CHANCE_THRESHOLD = settings.mock_offline_chance_threshold

    MAX_POWER = 20
    POWER_CONSUPTION_RANGES = {
        RobotStatus.IDLE.value: (7, 10),
        RobotStatus.RUNNING.value: (15, 20),
        RobotStatus.OFFLINE.value: (0, 0),
        RobotStatus.ERROR.value: (7, 10),
    }

    state: RobotState
    is_fan_speed_proportional: bool = True
    previous_status: str = RobotStatus.IDLE.value

    def __init__(self, refresh_rate: int):
        super().__init__(refresh_rate)
        self._logger = logging.getLogger("RobotController")
        self._lock = RLock()
        self.state = RobotState(
            current_temperature=np.float16(0),
            current_power_consumption=np.float16(0),
            status=RobotStatus.IDLE.value,
            fan_speed=np.int8(0),
            uptime=timedelta(),
            logs=[],
        )
        self._task = asyncio.create_task(self.__update_loop(self.refresh_rate))

    def get_state(self) -> RobotState:
        return self.state

    def set_fan_speed(self, speed: int) -> None:
        with self._lock:
            self.is_fan_speed_proportional = False
            self.state.fan_speed = np.int8(speed)
            self._warn("Static fan speed has been set, the robot may overheat if set too low")
        
    def automate_fan_speed(self) -> None:
        with self._lock:
            self.is_fan_speed_proportional = True

    def switch(self) -> bool:
        with self._lock:
            if self.state.status == RobotStatus.IDLE.value:
                self.state.status = RobotStatus.RUNNING.value
                return True
            if self.state.status == RobotStatus.RUNNING.value:
                self.state.status = RobotStatus.IDLE.value
                return True
            message = f"Unable to switch with current state: '{self.state.status}'"
            self._warn(message)
            return False

    def reset(self) -> bool:
        with self._lock:
            if self.state.status not in [RobotStatus.IDLE.value, RobotStatus.ERROR.value]:
                message = f"Unable to reset whith current state: '{self.state.status}'"
                self._warn(message)
                return False
            self.state.status = RobotStatus.IDLE.value
            self.state.uptime = timedelta()
            self.state.logs = []
            self.started_at = datetime.now()
            return True

    def _warn(self, message: str) -> None:
        self._logger.warning(message)
        self.state.logs.append(f"WARN: {message}")

    def _update_state(self, delta_us: int) -> None:
        logs = []

        with self._lock:
            status = self.state.status
            
            # Uptime update
            if status != RobotStatus.OFFLINE.value:
                if self.state.uptime == timedelta(0):
                    time_delta = datetime.now() - self.started_at
                else:
                    time_delta = timedelta(microseconds=delta_us)
            else:
                time_delta = timedelta()

            # Status update
            if self.state.status == RobotStatus.OFFLINE.value:
                if random.random() > 0.7:
                    status = self.previous_status
            elif random.random() < self.OFFLINE_CHANCE_THRESHOLD:
                self.previous_status = status
                status = RobotStatus.OFFLINE.value
                message = "Robot is offline"
                self._logger.error(message)
                logs.append(f"ERROR: {message}")
            elif self.state.current_temperature == self.TEMPERATURE_RANGE[1]:
                status = RobotStatus.ERROR.value
                message = "Robot overheated"
                self._logger.error(message)
                logs.append(f"ERROR: {message}")

            # Temperature and other updates
            power_consumption = random.randint(*self.POWER_CONSUPTION_RANGES[status])
            fan_speed = power_consumption/self.MAX_POWER * 100 if self.is_fan_speed_proportional else self.state.fan_speed
            if status != RobotStatus.OFFLINE.value:
                temperature_range = (
                    min(
                        self.TEMPERATURE_RANGE[0],
                        math.floor(self.POWER_CONSUPTION_RANGES[status][0] / self.MAX_POWER * power_consumption + self.TEMPERATURE_RANGE[0])
                    ),
                    math.ceil(self.TEMPERATURE_RANGE[1] * self.POWER_CONSUPTION_RANGES[status][1] / self.MAX_POWER)
                )
                temperature = random.randint(*temperature_range) - self.MAX_FAN_COOLING * fan_speed / 100
                if temperature >= self.TEMPERATURE_THRESHOLD:
                    message = "Temperature reaching critical level! Increase fan speed to avoid overheating"
                    self._logger.warning(message)
                    logs.append(f"WARN: {message}")
            else:
                temperature = 0
            
            self.state.current_temperature = np.float16(temperature)
            self.state.current_power_consumption = np.float16(power_consumption)
            self.state.status = status
            self.state.fan_speed = np.int8(fan_speed)
            self.state.uptime += time_delta
            self.state.logs += logs

    async def __update_loop(self, refresh_rate: int):
        delta_us = 10**6 / refresh_rate
        while True:
            self._update_state(delta_us)
            await asyncio.sleep(1/refresh_rate)

    def __del__(self):
        self._task.cancel()
