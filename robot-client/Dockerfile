FROM node:22.14
WORKDIR /robot-client

ARG host=0.0.0.0
ARG port=3000
ARG api=http://localhost:5487
ARG refresh_rate=10

ENV HOSTNAME=$host
ENV PORT=$port
ENV ROBOT_CLIENT_BACKEND_URL=$api
ENV ROBOT_CLIENT_REFRESH_RATE=$refresh_rate

COPY ./package.json ./package-lock.json /robot-client/
RUN npm ci

COPY ./jsconfig.json ./launch.json ./next.config.mjs ./postcss.config.mjs ./eslint.config.mjs ./.env* /robot-client/
COPY ./src /robot-client/src

EXPOSE $port

ENV NODE_ENV=production
RUN npm run build

CMD ["npm", "run", "start"]