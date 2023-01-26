# data-engineering-zoomcamp

docker network create postgres-nw

create the folders to mount the data for pgadmin and pg_db

sudo chown -R 5050:5050 ${pag_admin_mount_path}

docker commands
--------------------------------------------------------------------
docker run -it --name postgres-db --network postgres-nw -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB=pg_db -v /home/alenjam/MySpace/Programming/Tutorials/Testing/dez-week1-assgn/pg_db_data:/var/lib/postgresql/data -p 5433:5432 postgres
--------------------------------------------------------------------
docker run -it --name postgres-admin --network postgres-nw -e PGADMIN_DEFAULT_EMAIL=admin@admin.com -e PGADMIN_DEFAULT_PASSWORD=root -v /home/alenjam/MySpace/Programming/Tutorials/Testing/dez-week1-assgn/pg_admin_data:/var/lib/pgadmin -p 8083:80 dpage/pgadmin4
--------------------------------------------------------------------
pg_admin (can be accessed from localhost:8083)

host : host.docker.internal  ip address can be found in /etc/hosts
port : 5433

once the dockers are set up

create a docker file to run the data ingestion script

--------------------------------------------------------------------
FROM python:3.9
RUN apt-get install wget
RUN pip install psycopg2-binary pandas sqlalchemy
WORKDIR /app
COPY data_ingest.py /
ENTRYPOINT [ "python","data_ingest" ]
--------------------------------------------------------------------

sudo docker build -t data_ingest_python .

run the data ingestion script

docker run -it data_ingest_python -url https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv -pg_user_name root -pg_password root -pg_host host.docker.internal -pg_port 5433 -pg_database pg_db -table_name zone_lookup


docker run -it data_ingest_python -url https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv -pg_user_name root -pg_password root -pg_host host.docker.internal -pg_port 5433 -pg_database pg_db -table_name zone_lookup


docker run -it data_ingest_python -url https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz -pg_user_name root -pg_password root -pg_host host.docker.internal -pg_port 5433 -pg_database pg_db -table_name green_taxi_trips


now the data would be present in 
/home/alenjam/MySpace/Programming/Tutorials/Testing/dez-week1-assgn/pg_db_data
/home/alenjam/MySpace/Programming/Tutorials/Testing/dez-week1-assgn/pg_admin_data
