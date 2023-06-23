FROM python:3.11.3-alpine3.18


RUN addgroup staff && adduser -S -G staff s_user

WORKDIR /app

RUN chown -R s_user:staff /app


USER s_user

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/home/s_user/.local/bin:${PATH}"


COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt  

COPY . .



