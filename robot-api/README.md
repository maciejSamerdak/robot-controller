# Robot API
An API to interact with a virtual robot.
Built with [**FastAPI**](https://fastapi.tiangolo.com/).

## Overview
This application simulates behavior of a robot and exposes several endpoints to interact with it.

### API
1. `GET /robot` - to retrieve current state.

```Python
#Example response
{
    "current_temperature":20.0,  # Celsius
    "current_power_consumption":8.0,  # Watt
    "status":"idle",  # any of idle|running|offline|error
    "fan_speed":40,  # %
    "uptime":"0:00:35.304163",
    "logs":[]
}
```
2. `POST /robot/switch` - to switch robot status: `idle` <-> `running`
3. `POST /robot/reset` - to reset robot (doable only on status `idle` and `error`)
4. `POST /robot/fan {"mode": "proportional"|"static", "value": null|0-100}` - to change fan operation

Further API documentation is available under `/docs`, once server is running.

### Robot behavior:
 - Temperature is selected randomly within predefined fixed range
 - Power consumption proportionaly affects temperature range with highest possible temperature being acheivable during `running` status (largest power consumption)
 - Temperature is reduced by fan, proportionally to its speed
 - By default there is a fairly small chance for robot to randomly go offline for a brief period of time
 - If temperature reaches critical value (above 45°C by default), a warning will be issued about it.
 - If temperature reaches maximum value (by default 50°C) (`running` status with fan speed at 0%) robot **can overheat** and go into `error` state as result, while issuing **an error log about it**.
 - A warning is issued when fan is set to "static" mode.
 - Warnings are issued when status change operations are invoked on wrong states, for example `reset` on `running` or `switch off` on `error`

## Installation
Use poetry to install dependencies:
```shell
pip install poetry

poetry install
```

## Running
There are several approaches available to run the sever:

### 1. Running `./run.py`
Executing `python run.py` allows server to launch locally with **desired default parameters** and to [modify them with environment variables](#1-executing-runpy).

### 2. FastAPI CLI / Uvicorn CLI
 - `fastapi dev app/main.py` - for development server
 - `fastapi run app/main.py` - for production server
Starting server with **FastAPI CLI** enforces **FastAPI** fixed configuration.
 - `uvicorn app.main:app` - for manual production launch with **Uvicorn CLI**. This allows passing [additional arguments for custom configuration](#2-uvicorn-cli).

### 3. Docker
In order to launch server on Docker container with desired configuration, perform these steps:
```shell
docker build -t robot-api --build-arg log_level=info  .

docker run -p 5487:5487 --name robot-api robot-api
```
Aside from `log_level`, `host` and `port` can also be passed to change server configuration on container itself.

## Custom configuration
There are several environment variables, which can be used to alter application's behavior.

These values can be set with a `./.env` file to take effect with each launch method. The dotenv file is entirely optional for server to run.

 - `ROBOT_API_HOST` - server host configuration, defaults to `localhost`
 - `ROBOT_API_PORT` - server port configuration, defaults to `5487`
port: int = 5487
 - `ROBOT_API_LOG_LEVEL` - defaults to `info`
 - `ROBOT_API_REFRESH_RATE` - expressed in Hz, determines frequency with which robot's state is being updated, defaults to `10`
 - `ROBOT_API_ALLOWED_ORIGINS` - determines allowed origins for CORS policy, should be used to allow requests from client app, defaults to `["http://localhost:3000", "http://127.0.0.1:3000", "http://0.0.0.0:3000"]`

### Robot mock settings
These values can be used to affect robot simulation:

 - `ROBOT_API_MOCK_MAX_FAN_COOLING` - determines fan's cooling efficiency at 100% speed, expressed in Celsius, defaults to `10`
 - `ROBOT_API_MOCK_TEMPERATURE_RANGE` - determines range of robot's temperature in Celsius, defaults to `(20, 50)`
 - `ROBOT_API_MOCK_TEMPERATURE_THRESHOLD` - determines temperature threshold in Celsius above which a warning is issued, defaults to `45`
 - `ROBOT_API_MOCK_OFFLINE_CHANCE_THRESHOLD` - determines robot's probability of going offline, defaults to `0.01`

## Configuring host, port and log level
In order to change **host**, **port** and **log level** from default values, different approaches should be considered depending on how server start is handled:

### 1. Executing `./run.py`
Setting environment variables `ROBOT_API_HOST`, `ROBOT_API_PORT` and `ROBOT_API_LOG_LEVEL` either manually or with `./.env` file allows user to change **host**, **port** and **log level** settings respectively, **only when starting server with `./run.py`**

### 2. Uvicorn CLI
While starting server with **Uvicorn CLI**, `--host`, `--port` and `--log-level` arguments can be passed, like so:
```shell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --log-level debug
```
Alternatively, **Uvicorn** can be configured with environment variables prefixed with `UVICORN_*`. However, these must be set on system level, rather than with dotenv file.
You can learn more about it [here](https://www.uvicorn.org/settings/#configuration-methods).

### 3. Docker container
**Log level** can be defined on `docker build` command, by passing a `log_level` build argument, like so:
```shell
docker build -t robot-api --build-arg log_level=error  .
```

**Host** and **port** can be configured by publishing container's exposed port on `docker run` command with `-p` parameter, for example:
```shell
docker run -p 127.0.0.1:8000:5487 --name robot-api robot-api
```