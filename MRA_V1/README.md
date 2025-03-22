# MRA Setup


# Folder structure

- `prisma/`: contains the prisma schema and migration files

# Prerequisites

Tools to install:

- docker >= 27: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
  - To run database and infrastructure locally
- poetry : https://python-poetry.org/
  - for package management and virtual env
- task: https://taskfile.dev/installation/
  - To centralize all the commands in the Taskfile.yml files

# VSCode extension

VSCode extensions to install:

- pylance
- autopep
- Prisma
-

## Setup the env

To install all the dependencies and setup the local project please run the following command:

```
$ task init
```

## Run the app

To start the whole project locally, please run the following command:

```
$ task run
```

It will:

- run, migrate and seed the database
- run the streamlit app

## Run the app

To cleanup the env,

```
$ task clean
```

You can also launch multiple goals

```
$ task clean init
```

## others

You can also run different parts of the project separately:

```
$ task run-database
```
