FROM python:2.7-alpine

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY webhook.py ./

CMD python webhook.py
