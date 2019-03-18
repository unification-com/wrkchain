FROM node:8

COPY ./assets/ /root/
COPY ./assets/build/.env /root/wrkchain-validator-ui/.env

WORKDIR /root/wrkchain-validator-ui
RUN npm install

CMD cd /root/wrkchain-validator-ui && node server.js
