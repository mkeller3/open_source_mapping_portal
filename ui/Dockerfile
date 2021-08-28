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

# First step: Build with Node.js
FROM node:12 as dev
WORKDIR /app
COPY package.json /app
RUN npm install --silent
COPY . /app
RUN npm run build

# Deliver the dist folder with Nginx
FROM nginx:stable-alpine

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=dev /app/dist /usr/share/nginx/html
COPY entrypoint.sh /

CMD ["/entrypoint.sh"]