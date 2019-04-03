
## $__SECTION_NUMBER__.$__SUB_SECTION_NUMBER__ Appendix 5: Setting up a local Mainchain $__MAINCHAIN_NETWORK__ JSON RPC Node

It is possible to set up a local JSON RPC node for Unification's Mainchain 
`$__MAINCHAIN_NETWORK__`

**Installation**

First, install Unification's Mainchain software:

```bash
go get github.com/unification-com/mainchain
go install github.com/unification-com/mainchain/cmd/und
```

**Initialisation**

Initialise the client with the `$__MAINCHAIN_NETWORK__`'s `genesis` block:

```bash
und init $$GOPATH/src/github.com/unification-com/haiku-core/native/mainchain/Docker/assets/genesis.json
```

Copy the `$__MAINCHAIN_NETWORK__` static nodes:

_Linux_:

```bash
cp $$GOPATH/src/github.com/unification-com/haiku-core/native/mainchain/Docker/validator/bootnode_keys/static-nodes.json ~/.und_mainchain/static-nodes.json
```

_OSX_:

```bash
cp $$GOPATH/src/github.com/unification-com/haiku-core/native/mainchain/Docker/validator/bootnode_keys/static-nodes.json ~/Library/UndWRKChain/static-nodes.json
```

**Running**

Run your local Mainchain JSON RPC Node:

```bash
$$GOPATH/bin/und --networkid $__MAINCHAIN_NETWORK_ID__ \
--rpc \
--rpcapi "eth,personal,web3" \
--rpcport "8551" \
--syncmode=light \
--verbosity=4
```

It should now be possible to connect to the Mainchain `$__MAINCHAIN_NETWORK__`
via <http://localhost:8551> (for example, using MetaMask)
