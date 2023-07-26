FROM python:3.11.3-alpine3.18

RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app
COPY pipeline.py pipeline.py

ENTRYPOINT [ "python", "pipeline.py" ]