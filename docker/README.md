# Docker

To create the consistent environment for development, we use the docker to set up the services and use the docker-compose to manage all services that we have.

## Prerequirements

* [docker](https://www.docker.com/products/overview)
* [docker-compose](https://docs.docker.com/compose/)

## Quick start

Please change the path to `docker/` first, the below commands only works if the docker-compose.yml exist.

### Start services

The command will start up the service that is defined in the docker-compose.yml file. If the image does not exist, it will build it up automatically.

```
$ docker-compose up -d
```

### Stop services

The command will stop all services.

```
$ docker-compose stop
```

If you want to stop the specific service, you should give the service name.

```
$ docker-compose stop xmusic-db
```

### Remove services

The command will remove all service that has been created already. The argument `-f` is the option for force remove the service.

```
$ docker-compose rm -f
```
