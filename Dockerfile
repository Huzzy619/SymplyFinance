FROM python:3.11.3-alpine3.18


RUN addgroup app && adduser -S -G app app

USER app

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# Set appropriate permissions for the directory
USER root
RUN chown -R app:app /app
USER app

