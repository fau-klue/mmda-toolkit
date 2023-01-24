FROM ubuntu:20.04


##########################
# INSTALL OS DEPENDENCIES
##########################
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends -y \
    apt-utils \
    autoconf \
    bison \
    flex \
    gcc \
    libc6-dev \
    libglib2.0-0 \
    libglib2.0-dev \
    libncurses5 \
    libncurses5-dev \
    libpcre3-dev \
    libreadline8 \
    libreadline-dev \
    make \
    pkg-config \
    subversion \
    python3 \
    python3-pip \
    python3-dev \
    python3-setuptools \
    less \
    mg \
    git

#####################
# SYSTEM ENVIRONMENT
#####################
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONIOENCODING utf-8
ENV DEBIAN_FRONTEND noninteractive

#####################
# INSTALL LATEST CWB
#####################
RUN svn co http://svn.code.sf.net/p/cwb/code/cwb/trunk /cwb
WORKDIR /cwb
RUN sed -i 's/SITE=beta-install/SITE=standard/' config.mk && \
    ./install-scripts/install-linux && \
    ldconfig


############################
# SET UP PYTHON ENVIRONMENT
############################
# application is copied later so that all previous layers and python environment can be cached
WORKDIR /app

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -q pipenv

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --dev --system --ignore-pipfile --deploy


###########
# COPY APP
###########
COPY . /app


#############################
# SET UP AND START THE SEVER
#############################
ENV CORPORA_SETTINGS /opt/mmda-corpora.py
ENV CWB_REGISTRY_PATH /opt/cwb/registry/
ENV SQL_DATABASE_URI sqlite:////opt/mmda/mmda.sqlite

ENV WORKERS 16
ENV TIMEOUT 3600

CMD /app/entrypoint.sh
# CMD /bin/bash