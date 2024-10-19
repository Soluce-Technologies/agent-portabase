FROM python:3.12-bookworm

ENV PYTHONUNBUFFERED 1

COPY requirements/requirements.txt /tmp/requirements.txt
COPY requirements/requirements.dev.txt /tmp/requirements.dev.txt

WORKDIR /src
ARG DEV=false


RUN python -m venv /py && \
        /py/bin/pip install --upgrade pip && \
        apt-get update && \
        apt-get install -y postgresql postgresql-client binutils libproj-dev gdal-bin && \
        /py/bin/pip install -r /tmp/requirements.txt && \
        if [ $DEV="true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
        fi && \
        rm -rf /tmp

COPY src /src

ENV PATH="/scripts:/py/bin:$PATH"

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:80","--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker"]
