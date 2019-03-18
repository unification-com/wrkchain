#!/bin/bash

cd /root/init

cat /root/assets/templates/autogen.env >> /root/assets/build/.env

# Generate a unique workchain ID
CHAIN_ID=$(od -N 4 -t uL -An /dev/urandom | tr -d " ")

# generate a unique wallet mnemonic
MNEMONIC=$(node init.js mnemonic)

#Generate bootnode key
/root/.go/bin/bootnode -genkey /root/assets/build/bootnode.key
BOOTNODE_ID=$(/root/.go/bin/bootnode -nodekey /root/assets/build/bootnode.key -writeaddress)
chmod +rw /root/assets/build/bootnode.key
sed -i "s/BOOTNODE_ID=/BOOTNODE_ID=$BOOTNODE_ID/g" /root/assets/build/.env

# Write Mnemonic to .env
sed -i "s/MNEMONIC=/MNEMONIC=$MNEMONIC/g" /root/assets/build/.env

# Get EV and RPC node addresses and keys, then write to .env
EV1_PUBLIC_ADDRESS=$(node init.js address "$MNEMONIC" 0)
sed -i "s/EV1_PUBLIC_ADDRESS=/EV1_PUBLIC_ADDRESS=$EV1_PUBLIC_ADDRESS/g" /root/assets/build/.env

EV1_PRIVATE_KEY=$(node init.js private_key "$MNEMONIC" 0)
sed -i "s/EV1_PRIVATE_KEY=/EV1_PRIVATE_KEY=$EV1_PRIVATE_KEY/g" /root/assets/build/.env

EV2_PUBLIC_ADDRESS=$(node init.js address "$MNEMONIC" 1)
sed -i "s/EV2_PUBLIC_ADDRESS=/EV2_PUBLIC_ADDRESS=$EV2_PUBLIC_ADDRESS/g" /root/assets/build/.env

EV2_PRIVATE_KEY=$(node init.js private_key "$MNEMONIC" 1)
sed -i "s/EV2_PRIVATE_KEY=/EV2_PRIVATE_KEY=$EV2_PRIVATE_KEY/g" /root/assets/build/.env

RPC_NODE_PUBLIC_ADDRESS=$(node init.js address "$MNEMONIC" 2)
sed -i "s/RPC_NODE_PUBLIC_ADDRESS=/RPC_NODE_PUBLIC_ADDRESS=$RPC_NODE_PUBLIC_ADDRESS/g" /root/assets/build/.env

RPC_NODE_PRIVATE_KEY=$(node init.js private_key "$MNEMONIC" 2)
sed -i "s/RPC_NODE_PRIVATE_KEY=/RPC_NODE_PRIVATE_KEY=$RPC_NODE_PRIVATE_KEY/g" /root/assets/build/.env

# Write EV1 and EV2 public addresses to "WRKCHAIN_EVS" variable in .env
# Used when the Workchain Root smart contract is deployed
sed -i "s/WRKCHAIN_EV_2/$EV2_PUBLIC_ADDRESS/g" /root/assets/build/.env
sed -i "s/WRKCHAIN_EV_1/$EV1_PUBLIC_ADDRESS/g" /root/assets/build/.env

# Set the Workchain's CHain ID in .env
sed -i "s/WRKCHAIN_NETWORK_ID=/WRKCHAIN_NETWORK_ID=$CHAIN_ID/g" /root/assets/build/.env

# Psuedo generate the genesis.json
WRKCHAIN_GENESIS_JSON_FILENAME=$(grep 'WRKCHAIN_GENESIS_JSON_FILENAME' /root/assets/build/.env)
cp /root/assets/templates/genesis_template.json /root/assets/build/${WRKCHAIN_GENESIS_JSON_FILENAME##*=}
sed -i "s/SEALERADDRESSES/${EV1_PUBLIC_ADDRESS:2}${EV2_PUBLIC_ADDRESS:2}/g" /root/assets/build/${WRKCHAIN_GENESIS_JSON_FILENAME##*=}

sed -i "s/EV1/${EV1_PUBLIC_ADDRESS:2}/g" /root/assets/build/${WRKCHAIN_GENESIS_JSON_FILENAME##*=}
sed -i "s/EV2/${EV2_PUBLIC_ADDRESS:2}/g" /root/assets/build/${WRKCHAIN_GENESIS_JSON_FILENAME##*=}
sed -i "s/RPC/${RPC_NODE_PUBLIC_ADDRESS:2}/g" /root/assets/build/${WRKCHAIN_GENESIS_JSON_FILENAME##*=}
sed -i "s/WRKCHAIN_ID/${CHAIN_ID}/g" /root/assets/build/${WRKCHAIN_GENESIS_JSON_FILENAME##*=}

# Write the genesis.json to .env. Used when deploying the Workchain Root smart contract
while IFS='' read -r line || [[ -n "$line" ]]; do
    sed -i "s/WRKCHAIN_GENESIS=/WRKCHAIN_GENESIS=${line}/g" /root/assets/build/.env
done < /root/assets/build/${WRKCHAIN_GENESIS_JSON_FILENAME##*=}

# Fund the generated addresses on Mainchain using the faucet
MAINCHAIN_FAUCET_URL=$(grep 'MAINCHAIN_FAUCET_URL' /root/assets/build/.env)
echo "fund $EV1_PUBLIC_ADDRESS"
wget -T 5 -t 2 -O - ${MAINCHAIN_FAUCET_URL##*=}/sendtx?to=${EV1_PUBLIC_ADDRESS}
sleep 6s
echo "fund $EV2_PUBLIC_ADDRESS"
wget -T 5 -t 2 -O - ${MAINCHAIN_FAUCET_URL##*=}/sendtx?to=${EV2_PUBLIC_ADDRESS}
sleep 6s
echo "fund $RPC_NODE_PUBLIC_ADDRESS"
wget -T 5 -t 2 -O - ${MAINCHAIN_FAUCET_URL##*=}/sendtx?to=${RPC_NODE_PUBLIC_ADDRESS}

# Copy the generated .env to the Smart Contract deployment directory
# since it needs some values during deployment
cp /root/assets/build/.env /root/workchain-root-contract/.env

# Compile Workchain Root smart contract
MAINCHAIN_NETWORK_ID=$(grep 'MAINCHAIN_NETWORK_ID' /root/assets/build/.env)
cd /root/workchain-root-contract
truffle compile
truffle migrate --reset
WRKCHAIN_ROOT_CONTRACT_ADDRESS=$(node abi.js addr ${MAINCHAIN_NETWORK_ID##*=})
sed -i "s/WRKCHAIN_ROOT_CONTRACT_ADDRESS=/WRKCHAIN_ROOT_CONTRACT_ADDRESS=${WRKCHAIN_ROOT_CONTRACT_ADDRESS}/g" /root/assets/build/.env
sed -i "s/WRKCHAIN_ROOT_ABI=/WRKCHAIN_ROOT_ABI=$(node abi.js)/g" /root/assets/build/.env

echo "======================================="
echo "= ENVIRONMENT INITIALISATION COMPLETE ="
echo "======================================="
echo ""
echo "Workchain EV1"
echo "---"
echo "Public address: ${EV1_PUBLIC_ADDRESS}"
echo "Private Key: ${EV1_PRIVATE_KEY}"
echo ""
echo "Workchain EV2"
echo "---"
echo "Public address: ${EV2_PUBLIC_ADDRESS}"
echo "Private Key: ${EV2_PRIVATE_KEY}"
echo ""
echo "Workchain RPC Node"
echo "--------"
echo "Public address: ${RPC_NODE_PUBLIC_ADDRESS}"
echo "Private Key: ${RPC_NODE_PRIVATE_KEY}"
echo ""
echo "Generated Wallet Mnemonic: ${MNEMONIC}"
echo ""
echo "(Wallets will work on both Mainchain and Workchain)"
echo ""
echo "Workchain Network ID: ${CHAIN_ID}"
echo "Workchain Root smart contract address on Mainchain: ${WRKCHAIN_ROOT_CONTRACT_ADDRESS}"
echo ""
echo "now run:"
echo ""
echo "  make build"
echo ""
