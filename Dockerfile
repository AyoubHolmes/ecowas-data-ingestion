FROM python:3.11.3

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "main.py" ]