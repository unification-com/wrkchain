
### $__SECTION_NUMBER__.2.$__SUB_SECTION_NUMBER__ WRKChain Oracle Deploy

The WRKChain Oracle contains a pre-compiled version of the WRKChain Root smart
contract, which can be easily be deployed. On _**one**_ of the hosts
on which the WRKChain Oracle software has been installed, run the following
command:

```bash
go run $$GOPATH/src/github.com/unification-com/haiku-core/oracle/apply.go "$__MAINCHAIN_WEB3_PROVIDER_URL__" "PRIVATE_KEY_FOR_ORACLE_WALLET" $__MAINCHAIN_NETWORK_ID__
```

This should return a result containing the Contract address and Tx ID:

```bash
Contract address: 0x123...
Transaction hash: 0xabc...

```

**Important**: Copy the returned Smart contract address somewhere safe. This
will be required for all future interaction with the Oracle.
