### JSON RPC Node [__NODE_NUM__]

Run

`git clone [__BASE_TO_CLONE__]`  

`geth --bootnodes "enode://[__BOOTNODE__]" --networkid "[__WORKCHAIN_NETWORK_ID__]" --verbosity=4 --rpc --rpcaddr "0.0.0.0" --rpcport "8545" --rpcapi "eth,web3,net,admin,debug,db" --rpccorsdomain "*" --syncmode="full"
`