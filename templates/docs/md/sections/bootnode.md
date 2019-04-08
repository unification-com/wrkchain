
**Note: It is recommended to only implement a `bootnode` for testing purposes.
In a production environment, defined `bootstrap` nodes, using `static-nodes.json`
are recommended. Set `bootnode.use=false`, or remove the `bootnode` section
in your config, and re-run the SDK to disable `bootnode`**

**Copy the required file**

Copy the generated `$__BUILD_DIR__/node_keys/bootnode.key` to  `$$HOME/$__WRKCHAIN_DATA_DIR__/node_keys/bootnode.key` on the
host assigned to run the `bootnode`


**Run the bootnode**

Run the bootnode with the following command:

```bash
$$GOPATH/bin/bootnode --datadir=$$HOME/$__WRKCHAIN_DATA_DIR__ -nodekey $$HOME/$__WRKCHAIN_DATA_DIR__/node_keys/bootnode.key -verbosity 4 --addr :$__BOOTNODE_PORT
```

For reference, your bootnode's `enode` address is:

`$__BOOTNODE_ENODE`