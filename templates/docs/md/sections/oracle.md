Ensure the following addresses have UND on the Mainchain **`$__MAINCHAIN_NETWORK__`**,
since they will be used to send data to the WRKChain Root Smart Contract:

```text
$__ORACLE_ADDRESSES__
```

On each computer responsible for running the WRKChain Oracle (usually one or
more Validator nodes), run:

```bash
go run $$GOPATH/src/github.com/unification-com/oracle/cmd/oracle/main.go \
    "WRKCHAIN_WEB3_PROVIDER_URL" \
    "$__MAINCHAIN_WEB3_PROVIDER_URL__" \
    "PRIVATE_KEY_FOR_ORACLE_ADDRESS" \
    "WRKCHAIN_ROOT_CONTRACT_ADDRESS" \
    $__ORACLE_WRITE_FREQUENCY__ \
    $__WRKCHAIN_NETWORK_ID__
```

Where:

`WRKCHAIN_WEB3_PROVIDER_URL` = a Web3 provider URL for your WRKChain, for example
**$__WRKCHAIN_WEB3_PROVIDER_URL__**  
`PRIVATE_KEY_FOR_ORACLE_ADDRESS` = the private key for the Oracle Address which 
will write to the WRKChain Root smart contract  
`WRKCHAIN_ROOT_CONTRACT_ADDRESS` = the address of your deployed WRKChain Root
smart contract on Mainchain, acquired during Section 2.2
