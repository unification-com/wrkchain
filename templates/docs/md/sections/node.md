### $__SECTION_NUMBER__.$__NODE_NUM__ Node $__NODE_NUM__: $__NODE_TITLE__: $__NODE_IP__

**Node Type:** $__NODE_TYPE__  
**Node IP:** $__NODE_IP__  
**Wallet Address:** $__EV_PUBLIC_ADDRESS__  

**Copying the required files**

Copy the following files to the host you will be running "**$__NODE_TITLE__**"

1. `$__BUILD_DIR__/genesis.json` to `~/.ethereum/genesis.json`
$__COPY_STATIC_FILES__

**Initialising the Node**

The first time you run the node, you will need to initialise it by running
the following:

**Note:** this only needs to be run _once_.

```bash
$$GOPATH/bin/geth init ~/.ethereum/genesis.json
```

```bash
export PRIVATE_KEY="PRIVATE_KEY_FOR_$__EV_PUBLIC_ADDRESS__"

echo "Enter the private key. CTRL-D to end"
cp /dev/stdin  ~/.privatekey
$$GOPATH/bin/geth account import --password $$WALLET_PASSWORD ~/.privatekey
rm ~/.privatekey
```

The `geth account import` command will create a new wallet file in `~/.ethereum`,
locking it with the value input for `YOUR_WALLET_PASSWORD`. Set a secure password,
and remember it for the next step.

**Running the Node**

Run the node using:

```bash
$__GETH_COMMAND__
```
