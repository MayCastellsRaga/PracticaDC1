FROM python:3.10.0-slim
WORKDIR /ingestor
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY save_data.py save_data.py
CMD ["python3", "-u", "save_data.py"]