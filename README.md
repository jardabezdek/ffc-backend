# :rocket: Frozen facts center backend

Welcome to the FFC backend repository!

This project serves as a comprehensive data analytics platform built on freely available data from
the official NHL API.

The repository is organized into these primary sections:

1. [Cloud Infrastructure](./stacks/README.md) (details below)
2. [Data Models for Transformation](./transform/README.md)
3. [Research Notebooks](./notebooks/README.md)

## :pencil: Authors

- [Jaroslav Bezdek](https://www.github.com/jardabezdek)

## :construction_worker_man: Setup

We leverage AWS CDK to define AWS services for data storage and transformation.

The project follows a standard Python project setup. Upon initialization, a virtualenv is created
within the project, stored under the `.venv` directory. To set up the virtualenv, assuming
a `python3` (or `python` for Windows) executable in your path with access to the `venv` package,
follow these steps:

1. Run `python3 -m venv .venv` in the project root directory.
2. Activate the virtualenv: `. .venv/bin/activate`
3. Install required dependencies: `pip install -r requirements.txt`
4. Synthesize the CloudFormation template for AWS CDK code: `cdk synth`

### :envelope: Deployment

Before deployment, some useful commands include:

- `cdk ls`: list all stacks in the app
- `cdk diff`: compare deployed stack with current state
- `cdk docs`: open CDK documentation

To deploy all stacks, run `cdk deploy`. For deploying a specific stack, use the stack ID,
such as `cdk deploy StorageStack|ComputeStack|TransformStack`.

## :floppy_disk: Data

> No guarantees are made regarding the quality of the data. NHL data might contain known issues
> and biases.

Production data is downloaded and saved to AWS S3 via
the [`download-raw-games` lambda function](./stacks/lambdas/download-raw-games/).
Triggered daily, it fetches details about the previous night's games.

For historical data, follow these steps to download to local disk within the Docker container
defined in the [`notebooks/` folder](./notebooks/), then manually upload to AWS S3:

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
