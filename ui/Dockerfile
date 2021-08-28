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
FROM node:12 as dev
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json /app/package.json
RUN npm install --silent
RUN npm install @vue/cli -g
COPY . /app
RUN npm run build

FROM nginx:latest as prod
COPY --from=dev /app/dist /usr/share/nginx/html/
COPY nginx/nginx.conf etc/nginx/
EXPOSE 8080
CMD ["nginx", "-g", "dameon off;"]

# FROM bitnami/nginx as prod
# COPY --from=dev /usr/src/app/dist /opt/bitnami/nginx/html/
# COPY --from=dev /usr/src/app/dist /app
# COPY nginx/nginx.conf opt/bitnami/nginx/conf/server_blocks/nginx.conf


