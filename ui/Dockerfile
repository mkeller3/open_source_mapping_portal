# Working here
# FROM node:12 as dev
# WORKDIR /usr/src/app
# COPY package*.json ./
# RUN npm install --silent
# COPY . .
# RUN npm run build

# FROM bitnami/nginx as prod
# COPY --from=dev /usr/src/app/dist /app

# This works as well
# FROM node:12 as dev
# WORKDIR /usr/src/app
# ENV PATH /usr/src/app/node_modules/.bin:$PATH
# COPY package*.json ./
# RUN npm install --silent
# RUN npm install @vue/cli@3.7.0 -g
# COPY . .
# RUN npm run build


# FROM bitnami/nginx as prod
# COPY --from=dev /usr/src/app/dist /opt/bitnami/nginx/html/
# COPY --from=dev /usr/src/app/dist /app
# COPY nginx/nginx.conf opt/bitnami/nginx/conf/server_blocks/nginx.conf

ARG NODE_VERSION=latest
ARG NGINX_VERSION=1.18.0
FROM node:$NODE_VERSION as build

WORKDIR /build
COPY ./package*.json ./
COPY ./vue.config.js .
COPY ./babel.config.js .
COPY ./.eslintrc.js .
RUN [ "npm", "install", "-g", "@vue/cli" ]
RUN [ "npm", "install" ]
COPY ./src/ ./src/

RUN [ "npm", "run", "build" ]

FROM bitnami/nginx:$NGINX_VERSION

WORKDIR /app
USER 1001

COPY --from=build /build/dist .

EXPOSE 8080
