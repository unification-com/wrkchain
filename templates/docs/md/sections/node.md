## $__SECTION_NUMBER__.$__NODE_NUM__ Node $__NODE_NUM__: $__NODE_TITLE__: $__NODE_IP__

**Node Type:** $__NODE_TYPE__  
**Node IP:** $__NODE_IP__  
**Wallet Address:** $__EV_PUBLIC_ADDRESS__  

**Copying the required files**

Copy the following files to the host you will be running "**$__NODE_TITLE__**"

1. `$__BUILD_DIR__/genesis.json` to `$$HOME/$__WRKCHAIN_DATA_DIR__/genesis.json`
$__COPY_STATIC_FILES__

**Initialising the Node**

The first time you run the node, you will need to initialise it by both
initialising the genesis block and creating a wallet file:

**Note:** this only needs to be run _once_.

First, initialise the genesis block:
```bash
$$GOPATH/bin/geth --datadir=$$HOME/$__WRKCHAIN_DATA_DIR__ init $$HOME/$__WRKCHAIN_DATA_DIR__/genesis.json
```

Next, create a new wallet file:
```bash
echo "Enter the private key for PRIVATE_KEY_FOR_$__EV_PUBLIC_ADDRESS__. CTRL-D to end"
cp /dev/stdin  $$HOME/.privatekey

$$GOPATH/bin/geth --datadir=$$HOME/$__WRKCHAIN_DATA_DIR__ account import $$HOME/.privatekey
rm $$HOME/.privatekey
```

The `geth account import` command will create a new wallet file in `$$HOME/$__WRKCHAIN_DATA_DIR__`,
locking it with the value input for `YOUR_WALLET_PASSWORD`. Set a secure password,
and remember it for the next step. Remember to delete the `.privatekey` file
from the file system after creating the wallet.

**Running the Node**

Run the node using:

```bash
$__GETH_COMMAND__
```
