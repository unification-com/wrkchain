# WRKChain SDK

The WRKChain SDK is a set of tools to quickly configure and deploy a WRKChain environment

WRKChains are rooted on Mainchain with their own WRKChainRoot smart contract, and also run their own 
WRKChain Oracle, which periodically reads the WRKChain's block headers, and writes the hashes/merkle roots
to its WRKChainRoot smart contract on Mainchain.

The WRKChain SDK will accept a configurable JSON, and generate for your 
WRKChain:

- The WRKChain's `genesis.json` Genesis block
- Node keys and associated files
- A Docker Composition for testing purposes
- An Ansible configuration to aid production deployment
- Full customised documentation on how to deploy and run your WRKChain

## Configuring a WRKChain

See the [WRKChain SDK Wiki](https://github.com/unification-com/wrkchain/wiki) 
for full documentation and configuration options

## Generating a WRKChain

Once the configuration options have been set and saved in a `config.json`, 
the WRKChain environment can be generated using one of the following methods.

### Docker

The quickest method is to run the Dockerised SDK. You will need to install both 
Docker and Docker compose.

Either copy one of the sample config files from `sdk/tests/test_data` to
`wrkchain.json`, or roll your own. For example

```bash
cp sdk/tests/test_data/simple.json ./wrkchain.json
```

Edit as `wrkchain.json` required, then run:

```bash
make sdk
```

This will generate everything required in the `build` directory.

### Running the Python script directly

It is also possible to run the SDK without Docker.

#### Dependencies

The SDK is dependent upon
go-ethereum's `bootnode` CMD, which can be installed as follows:

1. install Go from <https://golang.org/doc/install>
2. `go get github.com/ethereum/go-ethereum`
3. `go install github.com/ethereum/go-ethereum/cmd/bootnode`

Then, install the Python requirements:

```bash
pip install -r requirements.txt
```

#### Running the SDK

Once the dependencies are satisfied, the SDK can be run as follows:

```bash
cd sdk
python -m wrkchain.sdk generate_wrkchain /path/to/config.json ../build
```
