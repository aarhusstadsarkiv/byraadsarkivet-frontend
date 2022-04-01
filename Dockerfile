FROM python:3.9.7-slim-bullseye as build

ARG VERSION=0.61.1

RUN apt-get update && \
    apt-get install -y --no-install-recommends libsqlite3-mod-spatialite && \
    apt clean && \
    rm -rf /var/lib/apt && \
    rm -rf /var/lib/dpkg/info/*

RUN pip install https://github.com/simonw/datasette/archive/refs/tags/${VERSION}.zip && \
    find /usr/local/lib -name '__pycache__' | xargs rm -r && \
    rm -rf /root/.cache/pip

# copy static files
ADD /templates templates/
ADD /plugins plugins/
ADD /static static/
ADD metadata.json metadata.json
ADD db.db db.db

# Datasette defaults
# EXPOSE 8001
# CMD ["datasette"]

# My commands
EXPOSE 80
CMD ["datasette", "-i", "db.db", "--host", "0.0.0.0", "--port", "80", "--cors", "--plugins-dir", "plugins/", "--template-dir", "templates/", "--static", "static:static/", "--metadata", "metadata.json", "--setting", "allow_facet", "off", "--setting", "cache_size_kb", "1500", "--setting", "num_sql_threads", "10", "--setting", "suggest_facets", "off", "--setting", "default_page_size", "25", "--setting", "allow_csv_stream", "off", "--setting", "allow_download", "off", "--setting", "sql_time_limit_ms", "3500"]
