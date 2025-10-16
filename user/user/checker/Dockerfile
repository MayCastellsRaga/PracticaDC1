FROM python:3.10.0-slim
WORKDIR /checker
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY checker.py checker.py
CMD python3 -u checker.py
