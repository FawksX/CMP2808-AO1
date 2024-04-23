echo status: Rebuilding Docker Containers
sleep 1
echo status: shutting down docker
docker compose down cmp2808-rest-api
sleep 1
echo status: rebuild rest-api
docker compose build --no-cache cmp2808-rest-api
sleep 1
echo status: start docker containers
docker compose up -d