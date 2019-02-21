FROM martialblog/docker-corpus-tool:cwb-ucs
LABEL maintainer="markus.opolka@fau.de"

ENV CQP_REGISTRY_PATH '/var/registry'
ENV DEBIAN_FRONTEND noninteractive
ENV ENVIRONMENT development
ENV HOST 0.0.0.0
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PORT 5000
ENV PYTHONIOENCODING utf-8
ENV SECRET_KEY changemewhenstartingthecontainer
ENV SQL_DATABASE_URI 'sqlite:////var/local/mmda.sqlite'
ENV TLS_ENABLE ''
ENV TLS_CERTFILE '/var/local/cert.pem'
ENV TLS_KEYFILE '/var/local/key.pem'

WORKDIR /app

# Install system dependencies
RUN set -ex; \
        apt-get update && \
        apt-get install --no-install-recommends -y \
        \
        python3 \
        python3-pip \
        && rm -rf /var/lib/apt/lists/* ; \
        \
        pip3 install pipenv

# Copy and install Python dependencies
COPY Pipfile Pipfile.lock /app/
RUN set -ex; \
        # --dev cause of sklearn
        pipenv install --dev --system

# We copy the application here, so that the previous layers can be cached
COPY . /app

# Start the Application
CMD ["/app/entrypoint.sh"]
