# Frontend Dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine

WORKDIR /app
RUN npm install -g http-server

COPY --from=build /app/dist ./dist

EXPOSE 4200

CMD ["http-server", "dist", "-p", "4200", "--cors"]
