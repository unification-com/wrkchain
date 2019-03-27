**Configured for `$__MAINCHAIN_NETWORK__`**

$__TESTNET_WARNING__

To Run your WRKChain, you will need to follow the steps below. Briefly, you
will need to:

1. Fund the public addresses used to write to your WRKChain Root smart 
contract with UND  
2. Deploy the WRKCHain Root smart contract  
3. Install the required node software on each of the computers that will run
your WRKCHain network  
4. Run the Nodes  
5. Run the WRKCHain Oracle software

### $__SECTION_NUMBER__.1 About your WRKChain

**Your WRKChain Network ID:** $__WRKCHAIN_NETWORK_ID__  
**This configuration is for:** $__MAINCHAIN_NETWORK__  
**Your base blockchain:** $__BASE_CHAIN__  
**Your Consensus algorithm:** $__CONSENSUS__

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
**ansible**: Directory containing Ansible configuration