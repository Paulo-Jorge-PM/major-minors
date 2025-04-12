FROM python:3.11.6-slim-bullseye
WORKDIR /flask-site
#COPY --chown=nonroot:nonroot . .
COPY app app
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
COPY README.md README.md

RUN pip install poetry
#RUN pip install gunicorn

RUN poetry config virtualenvs.in-project true
#RUN poetry install --without dev
RUN poetry install

EXPOSE 5000

CMD [".venv/bin/python3","-m","gunicorn","--bind","0.0.0.0:5000","runner:app"]