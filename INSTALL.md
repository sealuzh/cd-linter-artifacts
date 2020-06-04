# Installation

In this document, you will find all the information you need to setup an environment that can execute our artifacts.

## Execute the artifacts in a Docker Container (Recommended)

In the root of our replication package, you find a `Dockerfile`. This file can be used the build an image that your Docker installation can run.

1. Install [Docker for Desktop](https://www.docker.com/products/docker-desktop)
2. Open the terminal and position in the root folder of the replication package.
3. Build the image `docker build --no-cache -t artifact:v1 .`
4. Run the image `docker run -it  artifact:v1`
5. (add dockerignore)

## Setup your own environment

If you like, you can build your own environment to execute the artifacts. You need to manually install the following tools and copy the content of our replication package.

* Java 11
* Maven 3.6.0
* Python 3.6
* pip ...
* R ...