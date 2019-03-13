### $__SECTION_NUMBER__.$__NODE_NUM__ Node $__NODE_NUM__: $__NODE_NAME__

Node Type: ($__NODE_TYPE__)

Copy the generated `genesis.json` to the computer you will be running Node $__NODE_NUM__

The first time you run the node, you will need to initialise it by running
the following

```bash
geth init /PATH/TO/YOUR/GENERATED/genesis.json
geth account import --password 'YOUR_WALLET_PASSWORD' YOUR_WALLET_PRIVATE_KEY
```

Run the node using:

```bash
$__GETH_COMMAND__
```
