import os
import psycopg2
import json
import time
from kafka import KafkaConsumer

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

consumer = KafkaConsumer("location", bootstrap_servers=[
                         os.getenv("KAFKA_CONSUMER")])


def _add_to_location(location):
    session = psycopg2.connect(
        dbname=DB_NAME,
        port=DB_PORT,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST)

    cursor = session.cursor()
    cursor.execute(
        'INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}));'.format(
            int(location["person_id"]),
            float(location["latitude"]),
            float(location["longitude"])))
    session.commit()

    cursor.close()
    session.close()

    print("Location added to DB!")
    return location


def consume_message():
    for message in consumer:
        location = json.loads(message.value.decode("utf-8"))
        _add_to_location(location)


# Forever running thread
print("Starting consumer and waiting for messages..")
try:
    while True:
        consume_message()
        time.sleep(0.1)
except KeyboardInterrupt:
    exit(0)
