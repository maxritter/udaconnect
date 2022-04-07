# Assumes a working cluster for DB connection!
# Check out deployment.sh for more information

# Start Local Zookeeper & Kafka with Docker
docker-compose up -d
export KAFKA_PRODUCER="127.0.0.1:9092"
export KAFKA_CONSUMER="127.0.0.1:9092"

# Connect to the DB on Local K8s Cluster
kubectl port-forward service/postgres 5432:5432
export DB_USERNAME="ct_admin"
export DB_PASSWORD="wowimsosecure"
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="geoconnections"

# Running services (each in a separate terminal)
cd modules/frontend && npm start
cd ../../modules/connection && flask run --host 0.0.0.0
cd ../../modules/person && flask run --host 0.0.0.0
cd ../../modules/location-consumer && python -u app/udaconnect/consumer.py
cd ../../modules/location-producer && python -u app/udaconnect/producer.py