echo status: Rebuilding Docker Containers
sleep 1
echo status: shutting down docker
docker stop cmp2808-ao1-cmp-2808-mysql-1
sleep 1
echo status: rebuild mysql
docker compose build --no-cache cmp-2808-mysql
sleep 1
echo status: start docker containers
docker compose up -d