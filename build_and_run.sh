#/bin/bash
clear
docker build -t frd-ac:latest .
echo "##################"
echo "##################"
docker run -d --rm --name frd-ac -p 80:80 --env-file env.secret frd-ac
docker container logs -f frd-ac