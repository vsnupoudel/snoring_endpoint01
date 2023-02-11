FROM python:3.8-slim

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc

WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

CMD ["sh", "-c", "tail -f /dev/null"]
# CMD ["python", "predict.py"]