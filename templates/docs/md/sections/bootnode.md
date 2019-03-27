
**Copy the required files**

Copy the generated `$__BUILD_DIR__/node_keys/bootnode.key` to  `~/.ethereum/node_keys/bootnode.key` on the
computer assigned to run the `bootnode`


**Run the bootnode**

Run the bootnode with the following command:

```bash
$$GOPATH/bin/bootnode -nodekey ~/.ethereum/node_keys/bootnode.key -verbosity 4 --addr :$__BOOTNODE_PORT
```

For reference, your bootnode's `enode` address is:

`$__BOOTNODE_ENODE`