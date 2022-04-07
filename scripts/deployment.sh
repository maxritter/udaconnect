# Install Zookeeper & Kafka
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install kafka-local bitnami/kafka \
     --set persistence.enabled=true,zookeeper.persistence.enabled=true

# Build and Push App
docker build -t udaconnect-app ./modules/frontend
docker tag udaconnect-app maxritter/udaconnect-app:latest
docker push maxritter/udaconnect-app:latest

# Build and Push Person API
docker build -t udaconnect-person ./modules/person
docker tag udaconnect-person maxritter/udaconnect-person:latest
docker push maxritter/udaconnect-person:latest

# Build and Push Connection API
docker build -t udaconnect-connection ./modules/connection
docker tag udaconnect-connection maxritter/udaconnect-connection:latest
docker push maxritter/udaconnect-connection:latest

# Build and Push Location Consumer
docker build -t udaconnect-location-consumer ./modules/location-consumer
docker tag udaconnect-location-consumer maxritter/udaconnect-location-consumer:latest
docker push maxritter/udaconnect-location-consumer:latest

# Build and Push Location Producer
docker build -t udaconnect-location-producer ./modules/location-producer
docker tag udaconnect-location-producer maxritter/udaconnect-location-producer:latest
docker push maxritter/udaconnect-location-producer:latest

# Install K8s Layer 2 Components
kubectl apply -f deployment/kafka-configmap.yaml
kubectl apply -f deployment/db-configmap.yaml
kubectl apply -f deployment/db-secret.yaml
kubectl apply -f deployment/postgres.yaml
sh scripts/run_db_command.sh <POD_NAME>

# Install K8s Layer 3 Components
kubectl apply -f deployment/udaconnect-app.yaml
kubectl apply -f deployment/udaconnect-connection.yaml
kubectl apply -f deployment/udaconnect-location-consumer.yaml
kubectl apply -f deployment/udaconnect-location-producer.yaml
kubectl apply -f deployment/udaconnect-person.yaml