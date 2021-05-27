FROM node as builder
LABEL maintainer="markus.opolka@fau.de"

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

# Install and Build Application for production
RUN yarn install
RUN yarn run build

# Production Ready Image
FROM nginx:alpine
LABEL maintainer="markus.opolka@fau.de"
# Use the .env.production for settings

COPY --from=builder /usr/src/app/dist /usr/share/nginx/html/
# Custom Webserver Config
COPY nginx-mmda.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
EXPOSE 443
