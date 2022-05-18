# FROM ubuntu:20.04

# WORKDIR /mydir


# RUN apt-get update && apt-get install -y curl python3

# RUN pip3 install poetry

# COPY pyproject.toml poetry.lock /mydir/

# COPY . .

# RUN poetry install

# ENTRYPOINT ["python3"]

# CMD ["src/index.py"]

FROM python:3.7
RUN mkdir /app 
COPY . /app
COPY pyproject.toml /app 
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
ENTRYPOINT ["python3"]

CMD ["src/index.py"]