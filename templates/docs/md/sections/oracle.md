Ensure the following addresses have sufficient funds on your selected
network: **$__MAINCHAIN_NETWORK_TITLE__** (See section [3. Setup](#setup)),
since they will be used to send data to the WRKChain Root Smart Contract:

```text
$__ORACLE_ADDRESSES__
```

### Initialising the Oracle with the `init` command

1. create a data directory:

```bash
mkdir $$HOME/$__ORACLE_DATA_DIR__
```

2. Use a text editor such as `nano` to create and save the private key and
password files:

```bash
nano $$HOME/$__ORACLE_DATA_DIR__/.password
nano $$HOME/$__ORACLE_DATA_DIR__/.pkey
```

The files should only contain the selected password and private key respectively

3. Initialise the Oracle

```bash
wrkoracle init --password $$HOME/$__ORACLE_DATA_DIR__/.password --key $$HOME/$__ORACLE_DATA_DIR__/.pkey 
```

4. Delete the private key file - it's no longer required

```bash
rm -f $$HOME/$__ORACLE_DATA_DIR__/.pkey
```

### Registering your WRKChain with the `register` command

Before any WRKChain header hashes can be recorded, it requires registering with the
WRKChain Root smart contract on Mainchain.

1. `$__BUILD_DIR__/genesis.json` to `$$HOME/$__ORACLE_DATA_DIR__/genesis.json`
2. Run:

```bash
wrkoracle register --password $$HOME/.und_mainchain/.password \
  --account $__MAIN_ORACLE_ADDRESS__ \
  --genesis $$HOME/$__ORACLE_DATA_DIR__/genesis.json \
  --auth $__ORACLE_ADDRESSES_CMD__ \
  --mainchain.rpc "$__MAINCHAIN_WEB3_PROVIDER_URL__"
```

**Note**: The `register` command only needs to be run once.

### Recording WRKChain header hashes with the `record` command

```bash
wrkoracle record --password $$HOME/.und_mainchain/.password \
  --account $__MAIN_ORACLE_ADDRESS__ \
  --mainchain.rpc "$__MAINCHAIN_WEB3_PROVIDER_URL__" \
  --wrkchain.rpc "$__WRKCHAIN_WEB3_PROVIDER_URL__" \
$__ORACLE_HASHES__
  --freq $__ORACLE_WRITE_FREQUENCY__
```

For more information on flags and configuration, see <https://github.com/unification-com/oracle>

$__NO_JSON_RPC_NOTE__
