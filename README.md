# Workchain SDK

The Workchain SDK is a set of tools to quickly configure and deply a Workchain environment

Workchains are rooted on Mainchain with their own WorkchainRoot smart contract, and also run their own 
Workchain Oracle, which periodically reads the Workchain's block headers, and writes the hashes/merkle roots
to its WorkchainRoot smart contract on Mainchain.

## Configuring a Workchain


## Running a Workchain

By default, a Workchain is configured to run on the Unitication's Testnet, which is
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

## Viewing Workchain info

### Block explorer
The Workchain's blocks can be viewed via http://localhost:8081


### Bringing it all down

Bing down the Workchain composition by pressing <kbd>CTRL</kbd>+<kbd>C</kbd> then running:

`make down`

## Docker containers

`workchain_bootnode`: Workchain's own bootnode. Listening on port `30304  `  
`workchain_validator_1`: A Workhcain validator node. Listening on port `30305`  
`workchain_validator_2`: A 2nd Workchain validator node. Listening on port `30306`  
`workchain_node_1`: Workchain's RPC API node, for sending Txs. Runs on http://localhost:8547  
`workchain_explorer`: Workchain's own block explorer. Runs on http:/localhost:8081  
`workchain_oracle`: Workchain's Workchain Oracle. Reads Workchain's block headers and sends them to its
WorkchainRoot smart contract on Mainchain. Posts Txs to Mainchain via http://52.14.173.249:8101  
`init_workchain_environment`: Initialises the Workchain's environment.
Only run during the `make init` target.

## Init: further notes

`make init` will initialise a unique environment for the Workchain demo each time it is run. 
It will generate the necessary genesis block, chain ID, and wallets required to run the demo. 
It generates new wallets, chain ID and re-deploys a new Workchain Root to prevent any potential 
clashes with an existing demo system. 

Initialisation calls the Mainchain Testnet Faucet to fund the Workchain's addresses with UND
so that the workchain can deposit hashes to its Workchain Root smart contract.

## Account notes

The Workhain demo generates accounts, and smart contract addresses during the `make init` target.

