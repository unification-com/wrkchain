
## $__SECTION_NUMBER__.$__SUB_SECTION_NUMBER__ Appendix 5: Setting up a local Mainchain $__MAINCHAIN_NETWORK__ JSON RPC Node

It is possible to set up a local JSON RPC node for Unification's Mainchain 
`$__MAINCHAIN_NETWORK__`

**Installation**

First, install Unification's Mainchain software:

```bash
go get github.com/unification-com/mainchain
go install github.com/unification-com/mainchain/cmd/und
```

**Running**

Run your local Mainchain JSON RPC Node:

```bash
$$GOPATH/bin/und $__UND_NETWORK_FLAG__ \
--rpc \
--rpcapi "db,eth,net,web3,personal" \
--rpcport "8551" \
--syncmode=light \
--verbosity=4
```

It should now be possible to interact with the Mainchain `$__MAINCHAIN_NETWORK__`
via <http://localhost:8551> (for example, using MetaMask, or MEW to generate
and send transactions)
