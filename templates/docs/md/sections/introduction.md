**Configured for $__MAINCHAIN_TITLE__**

$__TESTNET_WARNING__

To Run your WRKChain, you will need to follow the steps below. Briefly, you
will need to:

1. Install the required node software on each of the hosts that will run
your WRKChain network 
2. Fund the public addresses used to write to your WRKChain Root smart 
contract  
3. Deploy the WRKCHain Root smart contract   
4. Run the Nodes  
5. Run the WRKCHain Oracle software

$__UND_JSON_RPC_NOTE__

## $__SECTION_NUMBER__.1 About your WRKChain

**This configuration is for:** $__MAINCHAIN_TITLE__  
**Your WRKChain Network ID:** $__WRKCHAIN_NETWORK_ID__  
**WRKChain's base blockchain:** $__BASE_CHAIN__  
**WRKChain's Consensus algorithm:** $__CONSENSUS__

### $__SECTION_NUMBER__.1.1 Generated Files

The `build` directory contains everything you need to get a WRKChain running:

```text
$__BUILD_DIR_STRUCTURE__
```

**README.md**: Quick info  
**ansible**: Directory containing Ansible configuration  
**docker**: Docker specific assets for testing
**docker-compose.yml**: Docker composition for testnet  
**documentation.md**: Markdown version of your documentation  
**documentation.html**: HTML version of your documentation  
**generated_config.json**: Full generated configuration file, with your overrides, 
which can be modified and used again with the SDK  
**genesis.json**: Your WRKChain's `genesis` block  
**node_keys**: Directory containing your bootnode key, or keys for your static nodes  
**ssh_keys**: SSH keys for Ansible  
**static-nodes.json**: Static nodes file, used when no `bootnode` is configured  
