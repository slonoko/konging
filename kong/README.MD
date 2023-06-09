docker network create kong-net

 docker run -d --name kong-database \
  --network=kong-net \
  -p 5432:5432 \
  -e "POSTGRES_USER=kong" \
  -e "POSTGRES_DB=kong" \
  -e "POSTGRES_PASSWORD=kongpass" \
  postgres:9.6

docker run --rm --network=kong-net \
  -e "KONG_DATABASE=postgres" \
  -e "KONG_PG_HOST=kong-database" \
  -e "KONG_PG_PASSWORD=kongpass" \
 kong:3.1.1 kong migrations bootstrap

docker run -d --name kong-gateway \
  --network=kong-net \
  -e "KONG_DATABASE=postgres" \
  -e "KONG_PG_HOST=kong-database" \
  -e "KONG_PG_USER=kong" \
  -e "KONG_PG_PASSWORD=kongpass" \
  -e "KONG_PROXY_ACCESS_LOG=/dev/stdout" \
  -e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" \
  -e "KONG_PROXY_ERROR_LOG=/dev/stderr" \
  -e "KONG_ADMIN_ERROR_LOG=/dev/stderr" \
  -e "KONG_ADMIN_LISTEN=0.0.0.0:8001, 0.0.0.0:8444 ssl" \
  -p 8000:8000 \
  -p 8443:8443 \
  -p 127.0.0.1:8001:8001 \
  -p 127.0.0.1:8444:8444 \
  kong:3.1.1

  docker build -t my-app:0.1 --build-arg APP_IMAGE=python:3.9.5-alpine -f Dockerfile .
  docker run -p 8080:8080 -dit --network=kong-net --name my-app-01 my-app:0.1
  docker run -p 8090:8080 -dit --network=kong-net --name my-app-02 my-app:0.1

https://dev.to/souravatta/writing-a-dockerfile-for-flask-app-2g1n

https://docs.konghq.com/gateway/3.1.x/install/docker/


curl -i -s -X POST http://localhost:8001/services \
  --data name=tf-01 \
  --data url='http://my-app-01:8080'

curl -i -s -X POST http://localhost:8001/services \
  --data name=torch-01 \
  --data url='http://my-app-02:8080'

curl -i -X POST http://localhost:8001/services/tf-01/routes \
  --data name=ms \
  --data 'headers.x-model=tensorflow'

curl -i -X POST http://localhost:8001/services/torch-01/routes \
  --data name=ms2 \
  --data 'headers.x-model=pytorch'