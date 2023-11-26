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

The data from NHL API are used for the analytics platform. They can be downloaded by running
the following commands in the docker container.

```bash
python /usr/src/app/src/extract/teams.py
python /usr/src/app/src/extract/players.py
python /usr/src/app/src/extract/games.py
```

## :link: Links

- Articles
  - [How to Get Started in Hockey Analytics](https://hockey-graphs.com/2018/11/27/how-to-get-started-in-hockey-analytics/)
- Data sources
  - [MoneyPuck.com](https://moneypuck.com/data.htm)
  - [NaturalStatTrick.com](https://naturalstattrick.com/)
  - [NHL API docs](https://gitlab.com/dword4/nhlapi)
  - [NHL API docs (new)](https://github.com/Zmalski/NHL-API-Reference)
- Inspiration for analysis
  - [HockeyViz talks & articles](https://hockeyviz.com/)
