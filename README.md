# get-scrt-events

### Alpha release -> if you find an error come let us know in discord #analytics

The json returned from the Secret Node /block_results endpoint requires some parsing to be useful for analysis. This application queries a remote node for all block_results and stores the parsed data in a [postgresql](https://www.postgresql.org/) database. 

For a more thorough explanation of how the data is parsed, click [here](docs/parsing.md).

[Hasura](https://hasura.io/docs/) is then used to make this data queryable via [graphql](https://graphql.org/learn/). 




## Quickstart - Docker

This quickstart requires [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) to be installed. 

The get-scrt-events application can be built with the following command. 

```bash
docker build . -t scrt_events:latest
```

To customize the chain-id and remote node queried, the environment variables for the events-api application in  the docker-compose.yml can be adjusted. 

The application can then be started with the following command. 

```bash
docker-compose up -d
```

