# https://docs.docker.com/build/building/best-practices/

# Build stage
FROM python:3.13-bullseye AS build

WORKDIR /app

COPY . /app

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

# Dev stage
FROM python:3.13-slim-bullseye AS dev

WORKDIR /app

COPY --from=build /app /app
COPY --from=build /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

CMD ["flask", "--app", "app", "run", "--host=0.0.0.0", "--port=8000", "--debug"]