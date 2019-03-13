
#### $__SECTION_NUMBER__.2.1 Using Truffle

```bash
cd workchain-root-contract
npm install -g truffle
npm install
```

Create a file called `.env` in the `workchain-root-contract` directory 
containing the following:

```text
MAINCHAIN_RPC_HOST=$__MAINCHAIN_RPC_HOST__
MAINCHAIN_RPC_PORT=$__MAINCHAIN_RPC_PORT__
MAINCHAIN_NETWORK_ID=$__MAINCHAIN_NETWORK_ID__
MAINCHAIN_WEB3_PROVIDER_URL=$__MAINCHAIN_WEB3_PROVIDER_URL__
WORKCHAIN_GENESIS=$__WORKCHAIN_GENESIS__
WORKCHAIN_NETWORK_ID=$__WORKCHAIN_NETWORK_ID__
WORKCHAIN_EVS=[$__WORKCHAIN_EVS__]
```

**Configuring HDWalletProvider**

<span style="color:red">**Please only do this with test addresses, and not production wallets!**</span>

Modify the `.env` file in the `workchain-root-contract` directory 
adding the following:

```text

MNEMONIC=CHANGE THIS TO YOUR MNEMONIC FOR ORACLE ADDRESS WALLET!
```

Then run:

```bash
truffle compile
truffle migrate --network development
```

**Configuring PrivateKeyProvider**

Alternatively, edit the `.env`, adding the following:

```text
PRIVATE_KEY=CHANGE THIS TO PRIVATE KEY FOR ORACLE ADDRESS WALLET!
```

Then run:

```bash
truffle compile
truffle migrate --network development-pk
```

**Post Deployment**

Once deployed using either of the methods above, make a note of the contract
address. You can obtain this by running:

```bash
node abi.js addr $__MAINCHAIN_NETWORK_ID__
```

**Important**: you will need this Contract Address in order to run the Oracle

#### $__SECTION_NUMBER__.2.2 Manual Deployment

Using your preferred method for Smart Contract compilation, compile
`workchain-root-contract/contracts/WorkchainRoot.sol`

When deploying, the `WorkchainRoot` constructor requires three arguments:

`genesis_block` is the web3.SHA3 result from the minified `genesis.json` content: `$__GENESIS_SHA3__`  
`chain_id` is your Workchain ID: `$__WORKCHAIN_NETWORK_ID__`  
`current_evs` is an array of the initial EVs' public addresses: `[$__WORKCHAIN_EVS__]`

