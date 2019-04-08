## $__SECTION_NUMBER__.$__SUB_SECTION_NUMBER__ Running a local WRKChain JSON RPC Node

It is also possible to install and run a local JSON RPC node, to which you can send
transactions and queries for your WRKChain. This is the preferred method, since
it is more secure, and is only available to the host running the node.

**Install geth**

Follow the instructions to install `geth` on the computer you would like to
 run a local JSON RPC Node.

**Copying the required files**

Copy the following files to the computer

1. `$__BUILD_DIR__/genesis.json` to `$$HOME/$__WRKCHAIN_DATA_DIR__/genesis.json`
$__COPY_STATIC_FILES__

**Initialise the node**

```bash
$$GOPATH/bin/geth --datadir=$$HOME/$__WRKCHAIN_DATA_DIR__ init $$HOME/$__WRKCHAIN_DATA_DIR__/genesis.json
```

**Running the Node**

Finally, run the node using:

```bash
$$GOPATH/bin/geth --networkid $__WRKCHAIN_NETWORK_ID__ \
--rpc \
--rpcapi "db,eth,net,web3,personal" \
--rpcport "8550" \
--syncmode=light \
--datadir=$$HOME/$__WRKCHAIN_DATA_DIR__
```

You will be able to connect (for example, via MetaMask) using the following parameters:

**Web3 Provider URL:** http://localhost:8550  
**Web3 Provider Host:** localhost  
**Web3 Provider Port:** 8550  
**Network ID:** $__WRKCHAIN_NETWORK_ID__  
