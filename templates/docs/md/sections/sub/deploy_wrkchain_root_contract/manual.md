
#### $__SECTION_NUMBER__.2.$__SUB_SECTION_NUMBER__ Manual Deployment

Clone the WRKChain Root smart contract repo into a suitable directory:

```bash
git clone https://github.com/unification-com/wrkchain-root-contract
```

Using your preferred method for Smart Contract compilation, compile
`wrkchain-root-contract/contracts/WRKChainRoot.sol`

The `WRKChainRoot` constructor requires three arguments:

`genesis_block` is the `web3.SHA3` result from the minified `genesis.json` 
content: `$__GENESIS_SHA3__`  
`chain_id` is your WRKChain ID: `$__WRKCHAIN_NETWORK_ID__`  
`current_evs` is an array of the initial Validator's public addresses:
 `[$__WRKCHAIN_EVS__]`

The following information can be used to determine where to deploy your 
WRKChain Root smart contract:  

**Mainchain RPC Host**: $__MAINCHAIN_RPC_HOST__  
**Mainchain RPC Port**: $__MAINCHAIN_RPC_PORT__  
**Mainchain Network ID**: $__MAINCHAIN_NETWORK_ID__  
**Mainchain Web3 Provider URL**: $__MAINCHAIN_WEB3_PROVIDER_URL__
