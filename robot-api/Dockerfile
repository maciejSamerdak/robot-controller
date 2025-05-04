FROM python:3.12
WORKDIR /robot-api

ARG host=0.0.0.0
ARG port=5487
ARG log_level=info

ENV UVICORN_HOST=$host
ENV UVICORN_PORT=$port
ENV UVICORN_LOG_LEVEL=$log_level

RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock README.md /robot-api/
RUN poetry install --without dev --no-root

COPY ./.env* /robot-api/.env
COPY ./app /robot-api/app

EXPOSE $port

CMD ["poetry", "run", "uvicorn", "app.main:app"]