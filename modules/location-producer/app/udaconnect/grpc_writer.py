import grpc
import location_pb2
import location_pb2_grpc

print("Connecting to GRPC server on port 5555..")
channel = grpc.insecure_channel("localhost:5555")
stub = location_pb2_grpc.LocationServiceStub(channel)

print("Sending a sample location from Muchich, Germany..")
location = location_pb2.LocationMessage(
    person_id=1,
    latitude=11.576124,
    longitude=48.137154
)
response = stub.Create(location)

print("Done!")
