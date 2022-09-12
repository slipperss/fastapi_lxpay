#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
#
#WORKDIR /app
#
#RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
#    cd /usr/local/bin && \
#    ln -s /opt/poetry/bin/poetry && \
#    poetry config virtualenvs.create false
#
#COPY ./pyproject.toml ./poetry.lock* /app/
#
#RUN poetry install
## --no-root --no-dev
##CMD uvicorn main:app --reload
#COPY . /app

FROM python:3.10.7

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/

RUN pip install -r requirements.txt

#RUN aerich init -t src.config.settings.TORTOISE_ORM

#RUN aerich init-db

COPY . /usr/src/

#RUN aerich upgrade

#docker exec -it lxpay_db_service aerich upgrade

#RUN docker-compose.yml up --build

CMD ["docker-compose", "up", "--build"]

CMD ["./start.sh"]