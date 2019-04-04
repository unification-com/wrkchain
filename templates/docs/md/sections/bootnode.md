
**Copy the required file**

Copy the generated `$__BUILD_DIR__/node_keys/bootnode.key` to  `~/$__WRKCHAIN_DATA_DIR__/node_keys/bootnode.key` on the
host assigned to run the `bootnode`


**Run the bootnode**

Run the bootnode with the following command:

```bash
$$GOPATH/bin/bootnode --datadir=~/$__WRKCHAIN_DATA_DIR__ -nodekey ~/$__WRKCHAIN_DATA_DIR__/node_keys/bootnode.key -verbosity 4 --addr :$__BOOTNODE_PORT
```

For reference, your bootnode's `enode` address is:

`$__BOOTNODE_ENODE`