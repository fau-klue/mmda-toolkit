FROM node:latest as build-stage
WORKDIR /app
COPY package*.json ./
RUN yarn install
COPY ./ .
RUN yarn run build

# Production Ready Image
FROM nginx as production-stage
# Use the .env.production for settings
COPY --from=build-stage /app/dist /usr/share/nginx/html/
# Custom Webserver Config
COPY nginx-mmda.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
EXPOSE 443
