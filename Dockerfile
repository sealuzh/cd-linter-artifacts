FROM ubuntu:18.04

# install Java 11
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -q \
 && apt-get upgrade -q -y \
 && apt-get install -q -y \
        binutils \
        openjdk-11-jdk-headless

# install Maven
RUN apt-get -y install maven=3.6.0-1~18.04.1

# install Python 3.7
RUN apt install software-properties-common -y \
&& add-apt-repository ppa:deadsnakes/ppa -y \
&& apt install python3.7=3.7.7-1+bionic1 -y

# install pip
RUN apt install python3-pip=9.0.1-2.3~ubuntu1.18.04.1 -y

# install R
# RUN apt-get install r-base -y
# RUN R -e "install.packages('devtools',dependencies=TRUE, repos='http://cran.rstudio.com/')"
# RUN R -e "install.packages('likert',dependencies=TRUE, repos='http://cran.rstudio.com/')"
# > require(devtools)
# > install_github("likert","jbryer")

# install an editor
RUN apt-get install vim -y

# copy all content inside
RUN mkdir /home/cd-linter-artifacts
COPY . /home/cd-linter-artifacts
WORKDIR /home/cd-linter-artifacts

# install the required dependencies
RUN pip3 install -r requirements.txt