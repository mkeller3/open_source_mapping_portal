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
CMD ["nginx", "-g", "daemon off;"]


