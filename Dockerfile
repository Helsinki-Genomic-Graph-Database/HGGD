
FROM python:3.8 as builder

WORKDIR /mydir

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt > requirements.txt


FROM python:3.8

WORKDIR /mydir

ENV PYTHONUNBUFFERED=1

COPY --from=builder /mydir/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run]