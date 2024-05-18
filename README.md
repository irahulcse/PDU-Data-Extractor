# PDU Data Extractor

## Project Overview

This project contains two Python scripts: `update-script.py` and `prometheus.py`.

- `update-script.py`: This script fetches data from a Power Distribution Unit (PDU) using the Simple Network Management Protocol (SNMP) and writes the fetched data to a CSV file.

- `prometheus.py`: This script fetches data from a PDU, updates a Prometheus gauge with the fetched data, and serves the gauge over HTTP for Prometheus to scrape.

The project also includes a Dockerfile and a docker-compose.yml file for running the scripts in Docker containers, and a prometheus.yml file for configuring Prometheus.

## Setup Instructions

1. Install the required Python packages:

The requirements.txt file should contain:
`pip install -r requirements.txt`

```bash
ply==3.11
pyasn1==0.6.0
pycryptodomex==3.20.0
pysmi==0.3.4
pysnmp==4.4.12
pysnmp-mibs==0.1.6
prometheus_client
```

Run `update-script.py` to fetch data from the PDU and write it to a CSV file:

`python update-script.py`
Run `prometheus.py` to fetch data from the PDU and expose it for Prometheus to scrape:
`python prometheus.py`

Configure your Prometheus server to scrape metrics from prometheus.py. Add the following to your prometheus.yml configuration file:
```bash
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.

scrape_configs:
  - job_name: 'pdu_data'
    static_configs:
      - targets: ['host.docker.internal:8000']
```

Replace host.docker.internal with the hostname or IP address where prometheus.py is running.

## Dockerization
Dockerizing this project could be beneficial if you want to ensure that it runs in the same environment regardless of where it's deployed. This can help avoid issues caused by differences in Python versions or installed packages.

Here's a basic Dockerfile that you could use:

```bash
FROM python:3.8

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "prometheus.py"]
```

And here's how you could build and run the Docker image:

```bash
docker build -t pdu-data-extractor .
docker run -p 8000:8000 pdu-data-extractor
```

If you want to run both scripts in the same Docker container, you could modify the CMD line in the Dockerfile to run a shell script that starts both scripts. Alternatively, you could use a process manager like Supervisor.

You can also use Docker Compose to run your application. Here's how you can do it:

Install Docker Compose if you haven't already. You can find the installation instructions here.

Run the following command in your project directory:


```bash 
docker-compose up --build
```

To shutdown the container and stop run it:

```bash
docker-compose down
```
This will start both the Prometheus server and your prometheus.py script.

