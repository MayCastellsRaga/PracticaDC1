FROM python:3.10.0-slim
WORKDIR /actuate
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY actuate.py actuate.py
CMD ["python3", "-u", "actuate.py"]