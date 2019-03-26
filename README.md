# WRKChain SDK

The WRKChain SDK is a set of tools to quickly configure and deploy a WRKChain environment

WRKChains are rooted on Mainchain with their own WRKChainRoot smart contract, and also run their own 
WRKChain Oracle, which periodically reads the WRKChain's block headers, and writes the hashes/merkle roots
to its WRKChainRoot smart contract on Mainchain.

The WRKChain SDK will accept a configurable JSON, and generate for your WRKChain:

- The genesis.json Genesis block
- A Docker Composition for testing
- Full documentation on how to deploy in a production environment

## Configuring a WRKChain


## Running a WRKChain

Once the configuration options have been set and saved in a `config.json`, the WRKChain environment can be 
generated.

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

This will generate everything required in the `build` directory

### Running the Python script directly

It is also possible to run the SDK without Docker.

First, install the requirements:

```bash
pip install -r requirements.txt
```

Then, run:

```bash
mkdir build
cd sdk
python -m wrkchain.sdk generate_wrkchain /path/to/config.json ../build
```
