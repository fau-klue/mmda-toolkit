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
# INSTALL LATEST CWB
#####################
RUN svn co http://svn.code.sf.net/p/cwb/code/cwb/trunk /cwb
WORKDIR /cwb
RUN sed -i 's/SITE=beta-install/SITE=standard/' config.mk && \
    ./install-scripts/install-linux && \
    ldconfig


########################
# ENVIRONMENT VARIABLES
########################
ENV SECRET_KEY 'changemewhenstartingthecontainer'

ENV ENVIRONMENT 'production'
ENV SQL_DATABASE_URI 'sqlite:////opt/database/mmda-docker.sqlite'
ENV CWB_REGISTRY_PATH '/opt/cwb/registry/'

ENV HOST 0.0.0.0
ENV PORT 5000
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONIOENCODING utf-8
ENV DEBIAN_FRONTEND noninteractive

ENV TLS_ENABLE ''
ENV TLS_CERTFILE '/var/local/cert.pem'
ENV TLS_KEYFILE '/var/local/key.pem'


############################
# SET UP PYTHON ENVIRONMENT
############################
WORKDIR /app

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -q pipenv

COPY Pipfile Pipfile.lock /app/

# Pipenv
RUN pipenv install --dev --system --ignore-pipfile --deploy


###################
# COPY AND RUN APP
###################
# We copy the application here, so that the previous layers can be cached
COPY . /app

# Start the Application
CMD ["/app/entrypoint.sh"]
