### 2.3 Bootnode

Copy the generated `/PATH/TO/GENERATED/bootnode.key` to the computer assigned to run the `bootnode`

`bootnode -nodekey /path/to/bootnode.key -verbosity 4 --addr :$__BOOTNODE_PORT`

Your bootnode `enode` address is:

`$__BOOTNODE_ENODE`