## :rocket: Transform layer

The transform layer of the data pipeline is constructed using dbt and duckdb.

## :construction_worker_man: Setup

### :wrench: Local development

In order to create a working environment, the [docker](https://www.docker.com/)
is used. To start it, please, follow the next steps.

1. Launch the docker daemon.
1. Get to the repository root folder: `cd transform/`
1. Build the docker image with a proper tag: `docker build --build-arg S3_ACCESS_KEY_ID=foo --build-arg S3_SECRET_ACCESS_KEY=foo --tag ffc-be-transform:latest -f DockerfileDev .`
1. Run docker container: `docker run -it -p 8080:8080 -v $(pwd):/usr/src/app ffc-be-transform:latest /bin/bash`
1. Run dbt transformation inside the docker container. For example: `dbt run --select +fact_standings --target prod`
1. To view the documentation, generate it using `dbt docs generate && dbt docs serve` Then, navigate
to [http://localhost:8080](http://localhost:8080) to access the documentation.

## :link: Links

- [dbt docs](https://docs.getdbt.com/docs/introduction) to learn more about the tool
- [dbt discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- [dbt slack](https://community.getdbt.com/) for live discussions and support
- [dbt blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
- [duckdb docs](https://duckdb.org/docs/) to learn more about the tool
