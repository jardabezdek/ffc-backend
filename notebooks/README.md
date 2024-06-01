## :rocket: Notebooks

The `notebooks/` folder consists of notebooks used for research and random tests.

## :construction_worker_man: Setup

### :wrench: Local development

In order to create a working environment, the [docker](https://www.docker.com/)
is used. To start it, please, follow the next steps.

1. Launch the docker daemon.
1. Get to the repository root folder: `cd notebooks/`
1. Build the docker image with a proper tag: `docker build -t ffc-be-notebooks:latest .`
1. Run docker container: `docker run -p 8888:8888 -v $(pwd):/usr/src/app ffc-be-notebooks:latest`
