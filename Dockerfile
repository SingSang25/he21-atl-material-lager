ARG PYTHON_VERSION=3.11.1

FROM python:${PYTHON_VERSION}-slim as build
WORKDIR /temp
COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --without test

FROM python:${PYTHON_VERSION}-slim
WORKDIR /app
COPY --from=build /temp/requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt
COPY ./he21_atl_material_lager/ /app/he21_atl_material_lager
CMD uvicorn he21_atl_material_lager.main:app --reload --proxy-headers --host 0.0.0.0 --port 8000
EXPOSE 8000