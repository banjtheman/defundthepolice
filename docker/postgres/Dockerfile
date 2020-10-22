FROM postgres:12

# Need dos2unix since some CSVs have inconsistent line endings.
RUN apt update && apt install -y dos2unix

RUN mkdir /data
RUN mkdir /data/states
ADD ./data/ /tmp

# create 1 csv with all other CSV data
RUN touch /tmp/allbudgets.csv
RUN echo "state,county,year,item,budget,source" >> /tmp/allbudgets.csv
RUN for file in /tmp/states/*/*/*.csv;  do  dos2unix "$file"; sed -i -e '$a\' "$file"; tail -n +2 "$file" >> /tmp/allbudgets.csv; done


# Set Postgres ENV variables
ENV POSTGRES_USER docker
ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB docker

# Create Table and Load CSV Data
ADD CreateDB.sql /docker-entrypoint-initdb.d/

