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
# Use the .env.production for settings

COPY --from=builder /usr/src/app/dist /usr/share/nginx/html/
COPY nginx-mmda.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
EXPOSE 443
