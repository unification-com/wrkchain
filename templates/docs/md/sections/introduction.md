**Configured for `$__MAINCHAIN_NETWORK__`**

$__TESTNET_WARNING__

To Run your WRKChain, you will need to follow the steps below. Briefly, you
will need to:

1. Install the required node software on each of the hosts that will run
your WRKChain network 
2. Fund the public addresses used to write to your WRKChain Root smart 
contract with UND  
3. Deploy the WRKCHain Root smart contract   
4. Run the Nodes  
5. Run the WRKCHain Oracle software

**Note regarding Mainchain transactions**

This documentation uses the Unification public JSON RPC Node 
(<$__MAINCHAIN_WEB3_PROVIDER_URL__>) when outlining
any interaction with Unification's Mainchain `$__MAINCHAIN_NETWORK__`. To set
up your own local JSON RPC node (the preferred method for interacting
with Mainchain), please see 
[Appendix 5: Setting up a local Mainchain JSON RPC Node](#appendix-5-setting-up-a-local-mainchain-testnet-json-rpc-node).

To use your own local JSON RPC node follow the instructions in Appendix 5,
 then replace any instance of 
**$__MAINCHAIN_WEB3_PROVIDER_URL__** in the documentation below with 
**http://localhost:8551**


## $__SECTION_NUMBER__.1 About your WRKChain

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