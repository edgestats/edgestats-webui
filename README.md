# EdgeStats Web UI

A web interface to [EdgeStats](https://www.edgestats.io). For use with private [edgestats-server](https://github.com/edgestats/edgestats-server) and [edgestats-client](https://github.com/edgestats/edgestats-client) setup.
>
> Check your Theta Edge Node uptime stats without needing to view the edge node client GUI/CLI.

## Setup

### Setup EdgeStats server
Instructions for setting up an EdgeStats server available [here](https://github.com/edgestats/edgestats-server).

### Setup EdgeStats client
Instructions for setting up an EdgeStats client available [here](https://github.com/edgestats/edgestats-client).

### Clone repository
Execute the following commands to clone this repository:

```shell
git clone https://github.com/edgestats/edgestats-webui
cd edgestats-webui
```

### Install dependencies
Execute the following command to install the dependencies:

```shell
pip install -r requirements.txt
```

### Set environment variables
The following environment variables need to be set:

```shell
export EDGESTATS_API_ADDR=<http://127.0.0.1:port>
export EDGESTATS_API_KEY=<your-api-key>
# example: export EDGESTATS_API_ADDR=http://127.0.0.1:8000
# example: export EDGESTATS_API_KEY=thetaverse
```
<!-- # or custom EdgeStats server url -->

### Run webui on slected port
```shell
flask run --port <port>
# example: flask run --port 5000
```

## LICENSE
Copyright (c) EdgeStats