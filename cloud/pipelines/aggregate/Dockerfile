FROM python:3.10.0-slim
WORKDIR /aggregate
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY aggregate.py aggregate.py
CMD ["faust", "-A", "aggregate", "worker", "-l", "info"]