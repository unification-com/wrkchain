
### $__SECTION_NUMBER__.1 About your WRKChain

**Your WRKChain Network ID:** $__WRKCHAIN_NETWORK_ID__

### $__SECTION_NUMBER__.1.1 Generated Files

The `build` directory contains everything you need to get a WRKChain running:

```text
$__BUILD_DIR_STRUCTURE__
```

**README.md**: This file  
**documentation.html**: HTML version of your documentation  
**generated_config.json**: Full generated configuration file, with your overrides, 
which can be modified and used again with the SDK  
**genesis.json**: Your WRKChain's `genesis` block  
**docker-compose.yml**: Docker composition for testnet  
**static-nodes.json**: Static nodes file, used when no `bootnode` is configured  
**node_keys**: Directory containing your bootnode key, or keys for your static nodes  
