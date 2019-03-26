### $__SECTION_NUMBER__.$__NODE_NUM__ Node $__NODE_NUM__: $__NODE_TITLE__

**Node Type:** $__NODE_TYPE__

**Node IP:** $__NODE_IP__

**Copying the required files**

Copy the following files to the computer you will be running "$__NODE_TITLE__"

1. `$__BUILD_DIR__/genesis.json` to `~/.ethereum`
$__COPY_NODE_KEY__
$__COPY_STATIC_NODES_JSON__

**Initialising the Node**

The first time you run the node, you will need to initialise it by running
the following:

```bash
geth init ~/ethereum/genesis.json
geth account import --password 'YOUR_WALLET_PASSWORD' PRIVATE_KEY_FOR_$__EV_PUBLIC_ADDRESS__
```

**Running the Node**

Run the node using:

```bash
$__GETH_COMMAND__
```
