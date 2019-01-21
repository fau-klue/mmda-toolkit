FROM node:alpine as builder
LABEL maintainer="markus.opolka@fau.de"

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN yarn install
RUN yarn run build

# Production Ready Image
FROM nginx:alpine
LABEL maintainer="markus.opolka@fau.de"

ENV API_BASE_URL=http://localhost:5000/api/
ENV BASE_URL=http://localhost/

COPY --from=builder /usr/src/app/dist /usr/share/nginx/html/
# TODO: nginx.config
# COPY nginx-mmda.conf /etc/nginx/conf.d/default.conf

# The nginx passwd and ssl certificates gets mounted during start

EXPOSE 80
EXPOSE 443
