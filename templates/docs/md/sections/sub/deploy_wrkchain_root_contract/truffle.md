
### $__SECTION_NUMBER__.2.$__SUB_SECTION_NUMBER__ Using Truffle

Clone the WRKChain Root smart contract repo into a suitable directory:

```bash
git clone https://github.com/unification-com/wrkchain-root-contract
```

Then run:

```bash
cd wrkchain-root-contract
npm install -g truffle
npm install
```

Create a file called `.env` in the `wrkchain-root-contract` directory
containing the following:

```text
MAINCHAIN_RPC_HOST=$__MAINCHAIN_RPC_HOST__
MAINCHAIN_RPC_PORT=$__MAINCHAIN_RPC_PORT__
MAINCHAIN_NETWORK_ID=$__MAINCHAIN_NETWORK_ID__
MAINCHAIN_WEB3_PROVIDER_URL=$__MAINCHAIN_WEB3_PROVIDER_URL__
WRKCHAIN_GENESIS=$__WRKCHAIN_GENESIS__
WRKCHAIN_NETWORK_ID=$__WRKCHAIN_NETWORK_ID__
WRKCHAIN_EVS=[$__WRKCHAIN_EVS__]
```

**Configuring HDWalletProvider**

<span style="color:red">**Please only do this with test addresses, and 
not production wallets!**</span>

Modify the `.env` file in the `wrkchain-root-contract` directory
adding the following:

```text
PRIVATE_KEY=CHANGE THIS TO YOUR PRIVATE_KEY FOR ORACLE ADDRESS WALLET
```

Then run:

```bash
truffle compile
truffle migrate --network und_mainchain
```

**Post Deployment**

Once deployed using either of the methods above, make a note of the contract
address. You can obtain this by running:

```bash
node abi.js addr $__MAINCHAIN_NETWORK_ID__
```

**Important**: you will need this Contract Address in order to run the Oracle
