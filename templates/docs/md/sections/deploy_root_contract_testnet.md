
#### $__SECTION_NUMBER__.2.1 Using Truffle & HDWalletProvider

<span style="color:red">**Please only do this with test addresses, and not production wallets!**</span>

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
MNEMONIC=CHANGE THIS TO YOUR MNEMONIC FOR ORACLE ADDRESS WALLET!
MAINCHAIN_WEB3_PROVIDER_URL=$__MAINCHAIN_WEB3_PROVIDER_URL__
WORKCHAIN_GENESIS=$__WORKCHAIN_GENESIS__
WORKCHAIN_NETWORK_ID=$__WORKCHAIN_NETWORK_ID__
WORKCHAIN_EVS=[$__WORKCHAIN_EVS__]
```

Then run:

```bash
truffle compile
truffle migrate
```