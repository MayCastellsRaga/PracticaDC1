FROM python:3.10.0-slim
WORKDIR /ingestor
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY clean_data.py clean_data.py
CMD ["python3", "-u", "clean_data.py"]