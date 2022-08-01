#/bin/bash
clear
docker container stop frd-ac
docker build -t frd-ac:latest .
echo "##################"
echo "##################"
docker run -d --rm --name frd-ac -p 8020:8020 --env-file env.secret frd-ac
docker container logs -f frd-ac