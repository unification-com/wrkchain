### $__SECTION_NUMBER__.$__NODE_NUM__ JSON RPC Node $__NODE_NUM__

Copy the generated `genesis.json` to the computer you will be running JSON RPC Node $__NODE_NUM__

Run

```bash
geth init /PATH/TO/YOUR/GENERATED/genesis.json
geth $__BOOTNODE__--networkid "$__WORKCHAIN_NETWORK_ID__" --verbosity=4 --rpc --rpcaddr "0.0.0.0" --rpcport "$__WORKCHAIN_RPC_PORT__" --rpcapi "eth,web3,net,admin,debug,db" --rpccorsdomain "*" --syncmode="full"
```