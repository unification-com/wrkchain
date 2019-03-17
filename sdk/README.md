# WRKChain SDK

The WRKChain SDK is a set of tools to quickly configure and deply a WRKChain environment

WRKChains are rooted on Mainchain with their own WRKChainRoot smart contract, and also run their own 
WRKChain Oracle, which periodically reads the WRKChain's block headers, and writes the hashes/merkle roots
to its WRKChainRoot smart contract on Mainchain.

## Configuring a WRKChain


## Running a WRKChain

By default, a WRKChain is configured to run on the Unitication's Testnet, which is
currently running on AWS. Simply run:

1. `make init`
2. `make build`
3. `make run`

to bring up the environment.

During the `make init` target, you will be prompted to customise your environment. This can be 
done by editing the generated `./Docker/assets/build/.env` file.

### Logging

Logging can be enabled at runtime, by executing:

`RUN_LOG=TRUE make run`

This will save all `stdout` and `stderr` messages to `./log.txt` for debugging

## Viewing WRKChain info

### Block explorer
The WRKChain's blocks can be viewed via http://localhost:8081


### Bringing it all down

Bing down the WRKChain composition by pressing <kbd>CTRL</kbd>+<kbd>C</kbd> then running:

`make down`

## Docker containers

`WRKChain_bootnode`: WRKChain's own bootnode. Listening on port `30304  `  
`WRKChain_validator_1`: A Workhcain validator node. Listening on port `30305`  
`WRKChain_validator_2`: A 2nd WRKChain validator node. Listening on port `30306`  
`WRKChain_node_1`: WRKChain's RPC API node, for sending Txs. Runs on http://localhost:8547  
`WRKChain_explorer`: WRKChain's own block explorer. Runs on http:/localhost:8081  
`WRKChain_oracle`: WRKChain's WRKChain Oracle. Reads WRKChain's block headers and sends them to its
WRKChainRoot smart contract on Mainchain. Posts Txs to Mainchain via http://52.14.173.249:8101  
`init_WRKChain_environment`: Initialises the WRKChain's environment.
Only run during the `make init` target.

## Init: further notes

`make init` will initialise a unique environment for the WRKChain demo each time it is run. 
It will generate the necessary genesis block, chain ID, and wallets required to run the demo. 
It generates new wallets, chain ID and re-deploys a new WRKChain Root to prevent any potential 
clashes with an existing demo system. 

Initialisation calls the Mainchain Testnet Faucet to fund the WRKChain's addresses with UND
so that the WRKChain can deposit hashes to its WRKChain Root smart contract.

## Account notes

The Workhain demo generates accounts, and smart contract addresses during the `make init` target.
