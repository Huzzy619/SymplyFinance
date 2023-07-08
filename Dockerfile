# FROM python:3.10-alpine3.18
# FROM python:3.9-slim-buster
FROM python:3.10-slim

RUN apt-get update && apt-get install -y libblas-dev liblapack-dev
# Install build essentials (including C++ compiler)
RUN apt-get install -y build-essential
RUN apt-get update && apt-get install -y rustc


# Set environment variables for C++11 support
ENV CXX=g++
ENV CXXFLAGS="-std=c++11"

WORKDIR /app


ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV OPENAI_API_KEY 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


COPY requirements.txt requirements.txt


RUN pip install -r requirements.txt  


COPY . .
COPY ./docker-compose-entry.sh ./app/docker-compose-entry.sh
RUN chmod +x docker-compose-entry.sh


ENV SECRET_KEY=${SECRET_KEY}
 

ENV TREBLLE_API_KEY=${TREBLLE_API_KEY}
ENV TREBLLE_PROJECT_ID=${TREBLLE_PROJECT_ID}
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV DEBUG=${DEBUG}
ENV DATABASE_URL=${DATABASE_URL}
ENV STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}

RUN python3  manage.py collectstatic --no-input

RUN python3 manage.py migrate

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "SymplyFinance.wsgi"]


