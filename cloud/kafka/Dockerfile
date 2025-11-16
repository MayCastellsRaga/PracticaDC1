FROM python:3.10.0-slim
WORKDIR /kafka
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY DataCleaner.py DataCleaner.py
CMD python3 -u DataCleaner.py
