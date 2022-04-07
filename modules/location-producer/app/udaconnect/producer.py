import logging
import grpc
import location_pb2
import location_pb2_grpc
import os
import time
from kafka import KafkaProducer
from concurrent import futures
import logging
import sys

logger = logging.getLogger('location-producer')
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

print('Init producer...')
producer = KafkaProducer(bootstrap_servers=[os.getenv("KAFKA_PRODUCER")])


class LocationService(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        print("received")
        location = {
            "person_id": request.person_id,
            "latitude": request.latitude,
            "longitude": request.longitude
        }
        producer.send("location", location)
        producer.flush()
        return location_pb2.LocationMessage(**location)


# Init gRPC server
print("Server starting on port 5555..")
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
