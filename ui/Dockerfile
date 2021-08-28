# # build environment
# FROM node:12 as dev
# WORKDIR /usr/src/app
# ENV PATH /usr/src/app/node_modules/.bin:$PATH
# COPY package*.json ./
# RUN npm install --silent
# RUN npm install @vue/cli@3.7.0 -g
# COPY . .
# RUN npm run build

# # production environment
# FROM nginx:alpine
# COPY --from=build /usr/src/app/dist /usr/share/nginx/html
# RUN rm /etc/nginx/conf.d/default.conf
# COPY nginx/nginx.conf /etc/nginx/conf.d
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]

# Working here
# FROM node:12 as dev
# WORKDIR /usr/src/app
# COPY package*.json ./
# RUN npm install --silent
# COPY . .
# RUN npm run build

# FROM bitnami/nginx as prod
# COPY --from=dev /usr/src/app/dist /app

FROM node:12 as dev
WORKDIR /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH
COPY package*.json ./
RUN npm install --silent
RUN npm install @vue/cli@3.7.0 -g
COPY . .
RUN npm run build

FROM nginx:alpine as prod
COPY --from=dev /usr/src/app/dist /app
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]