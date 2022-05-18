

FROM python:3.8

WORKDIR /mydir

ENV PYTHONBUFFERED=1

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "src/index.py"]