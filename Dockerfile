FROM python:2

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY webhook.py ./

CMD python webhook.py
