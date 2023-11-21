# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.1
FROM python:${PYTHON_VERSION}-slim as base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /
COPY . .
RUN pip install poetry
RUN poetry install
CMD poetry run uvicorn he21_atl_material_lager.main:app --reload --proxy-headers --host 0.0.0.0 --port 8000
EXPOSE 8000
