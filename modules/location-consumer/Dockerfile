FROM python:3.9.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 6666

COPY . .
CMD ["python", "-u", "app/udaconnect/consumer.py"]