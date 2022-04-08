import logging
import grpc
import json
import location_pb2
import location_pb2_grpc
import os
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError
from concurrent import futures
import logging
import sys

logger = logging.getLogger('location-producer')
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

print('Init producer...')
producer = KafkaProducer(bootstrap_servers=[os.getenv(
    "KAFKA_PRODUCER")], value_serializer=lambda v: json.dumps(v).encode('utf-8'))


class LocationService(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        # Parse gRPC message
        location = {
            "person_id": request.person_id,
            "latitude": request.latitude,
            "longitude": request.longitude
        }
        print("Received Location via gRPC: {}".format(location))

        # Send to Kafka topic
        future = producer.send('location', location)
        try:
            record_metadata = future.get(timeout=10)
        except KafkaError:
            logger.exception(KafkaError)
            pass
        print('Sending metadata to Kafka:')
        print(record_metadata.topic)
        print(record_metadata.partition)
        print(record_metadata.offset)

        return location_pb2.LocationMessage(**location)


# Init gRPC server
print("gRPC Server starting on port 5555..")
server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
location_pb2_grpc.add_LocationServiceServicer_to_server(
    LocationService(), server)
server.add_insecure_port("[::]:5555")
server.start()

# Forever running thread
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
