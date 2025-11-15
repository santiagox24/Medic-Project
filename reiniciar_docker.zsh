echo "Deteniendo contenedores..."
docker compose stop

echo "Eliminando contenedores..."
docker compose down

echo "Reconstruyendo e iniciando servicios..."
docker compose up --build