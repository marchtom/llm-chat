FROM node:21 AS build-stage

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 80
CMD [ "npm", "run", "serve", "--", "--port", "80" ]
