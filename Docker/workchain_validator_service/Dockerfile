FROM node:8

COPY ./assets/ /root/
COPY ./assets/build/.env /root/workchain-validator-ui/.env

WORKDIR /root/workchain-validator-ui
RUN npm install

CMD cd /root/workchain-validator-ui && node server.js
