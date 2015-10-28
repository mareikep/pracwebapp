FROM openease/flask
MAINTAINER Mareike Picklum, mareikep@cs.uni-bremen.de
USER root

RUN apt-get update
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y -q bash build-essential \
              zlib1g-dev libxml2-dev libxslt1-dev libatlas-base-dev libffi-dev libssl-dev gfortran \
              texlive-latex-recommended curl git g++ wget libpq-dev \
              python2.7 python python2.7-dev python-all-dev python-pip python-setuptools python-tk python-support libffi-dev libssl-dev \
              openjdk-7-jre default-jre-headless \
              dvipng libjpeg-dev python-imaging


RUN update-java-alternatives --jre -s java-1.7.0-openjdk-amd64
ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64/jre
ENV PATH $JAVA_HOME/bin:$PATH

ENV DOCKER_LINKS postgres_db:postgres dockerbridge:dockerbridge
ENV DOCKER_VOLUMES prac_tools prac_data

COPY requirements.txt /tmp/
RUN echo $JAVA_HOME
RUN sudo pip install --upgrade pip && sudo pip install -U -r /tmp/requirements.txt

WORKDIR /opt/webapp
ADD . /opt/webapp/

ENTRYPOINT /bin/bash /opt/webapp/init.bash

