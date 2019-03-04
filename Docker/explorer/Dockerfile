FROM node:6.11-alpine

WORKDIR "/opt"

RUN apk add --update git make g++ && \
    git clone https://bitbucket.org/designisdead/blockchain-explorer.git

WORKDIR "/opt/blockchain-explorer"
RUN git checkout c6e12f1 && \
    npm install

ARG WORKCHAIN_RPC_PORT
ARG WORKCHAIN_EXPLORER_PORT
ARG COIN_SYM
ARG WORKCHAIN_NAME

# change port from 8080 to configured port
RUN sed -i -E "s/8080/${WORKCHAIN_EXPLORER_PORT}/g" bin/www && \
    sed -i -E "s/localhost:8545/localhost:${WORKCHAIN_RPC_PORT}/g" views/layout/default_layout.jade && \
    grep -lr -e ' ETH' * | xargs sed -i -E "s/ ETH/ ${COIN_SYM}/g" && \
    grep -lr -e 'Ethereum' * | xargs sed -i "s/Ethereum/${WORKCHAIN_NAME}/g" && \
    grep -lr -e 'Ether' * | xargs sed -i "s/Ether/${WORKCHAIN_NAME}/g" && \
    grep -rl -e '(ethusd' * | xargs sed -i 's/(ethusd/(0.01/g'

CMD npm run start

EXPOSE $WORKCHAIN_EXPLORER_PORT
