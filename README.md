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

## :floppy_disk: Data

> No guarantees are made to the quality of the data. NHL data is known to have issues and biases.

The whole analytics part is based on data from the [MoneyPuck.com](https://moneypuck.com/data.htm)
website. The data can be downloaded by running the following command in the docker container.

```bash
python /usr/src/app/scripts/download_data.py
```

The [/scripts/download_data.py](./scripts/download_data.py) script creates a new `/data` folder
in the project root directory, downloads data, and organizes the files within the folder.

### :book: Data dictionary

Data dictionary can be found in the [/data_dictionary.json](./data_dictionary.json) file.
The dictionary is divided into two sections: players, and shots. The first section covers all the
columns related to skaters, goalies, lines, and teams. The second section describes the shots
datasets columns.

The minor purpose of the data dictionary is to create a mapper between the
[MoneyPuck.com](https://moneypuck.com/data.htm) original data columns and our own column names.
This mapper is used for renaming and filtering the original columns during the data download,
implemented inside the [/scripts/download_data.py](./scripts/download_data.py) script.
