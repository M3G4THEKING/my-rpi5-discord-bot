FROM python:3.10-slim
COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

ADD . /app
WORKDIR /app
CMD ["python", "app.py"]
