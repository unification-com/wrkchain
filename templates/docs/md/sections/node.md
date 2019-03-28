### $__SECTION_NUMBER__.$__NODE_NUM__ Node $__NODE_NUM__: $__NODE_TITLE__: $__NODE_IP__

**Node Type:** $__NODE_TYPE__  
**Node IP:** $__NODE_IP__  
**Wallet Address:** $__EV_PUBLIC_ADDRESS__  

**Copying the required files**

Copy the following files to the computer you will be running "**$__NODE_TITLE__**"

1. `$__BUILD_DIR__/genesis.json` to `~/.ethereum/genesis.json`
$__COPY_NODE_KEY__
$__COPY_STATIC_NODES_JSON__

**Initialising the Node**

The first time you run the node, you will need to initialise it by running
the following:

**Note:** this only needs to be run _once_.

```bash
$$GOPATH/bin/geth init ~/.ethereum/genesis.json
$$GOPATH/bin/geth account import --password 'YOUR_WALLET_PASSWORD' PRIVATE_KEY_FOR_$__EV_PUBLIC_ADDRESS__
```

**Running the Node**

Run the node using:

```bash
$__GETH_COMMAND__
```
