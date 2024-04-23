echo status: Rebuilding Docker Containers
sleep 1
echo status: shutting down docker
docker compose down cmp-2808-mysql
sleep 1
echo status: rebuild mysql
docker compose build --no-cache cmp-2808-mysql
sleep 1
echo status: start docker containers
docker compose up -d