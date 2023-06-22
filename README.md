## :rocket: ds-nhl

NHL data analytics project providing insights on the following topics:

- players segmentation

## :pencil: Authors

- [Jaroslav Bezdek](https://www.github.com/jardabezdek)

## :construction_worker_man: Setup

### :wrench: Local development

In order to create a working environment, the [docker](https://www.docker.com/)
is used. To start it, please, follow the next steps.

1. Launch the docker daemon.
1. Get to the repository root folder: `cd ~/projects/ds-nhl/`
1. Build the docker image with a proper tag: `docker build -t ds-nhl:latest .`
1. Run docker container: `docker run -it -p 8888:8888 -v $(pwd):/usr/src/app ds-nhl:latest /bin/bash`
1. Run notebook inside the docker container: `jupyter notebook --ip 0.0.0.0 --no-browser --allow-root`

### :floppy_disk: Data download

Data were downloaded from the [MoneyPuck.com](https://moneypuck.com/data.htm) website.
