## :rocket: Frozen facts center transform layel

The transform layer of the data pipeline is built using dbt, and duckdb.

## :pencil: Authors

- [Jaroslav Bezdek](https://www.github.com/jardabezdek)

## :construction_worker_man: Setup

### :wrench: Local development

In order to create a working environment, the [docker](https://www.docker.com/)
is used. To start it, please, follow the next steps.

1. Launch the docker daemon.
1. Get to the repository root folder: `cd infra/transform/`
1. Build the docker image with a proper tag: `docker build --build-arg S3_ACCESS_KEY_ID=foo --build-arg S3_SECRET_ACCESS_KEY=foo --tag frozen-facts-center-transform:latest -f DockerfileDev .`
1. Run docker container: `docker run -it -v $(pwd):/usr/src/app frozen-facts-center-transform:latest /bin/bash`

## dbt

### Using the starter project

Try running the following commands:

- dbt run
- dbt test

### Resources

- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
