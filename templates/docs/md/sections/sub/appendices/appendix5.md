
## $__SECTION_NUMBER__.$__SUB_SECTION_NUMBER__ Appendix 5: Setting up a local Mainchain $__MAINCHAIN_NETWORK__ JSON RPC Node

It is possible to set up a local JSON RPC node for Unification's Mainchain 
`$__MAINCHAIN_NETWORK__`

**Installation**

First, install Golang on the host, as outlined in section 2.1

Next, install Unification's Mainchain software:

```bash
go get github.com/unification-com/mainchain
go install github.com/unification-com/mainchain/cmd/und
```

**Initialising**

```bash
mkdir -p $$HOME/.und_mainchain/und
und account new
und init $${GOPATH}/src/github.com/unification-com/mainchain/genesis/$__UND_GENESIS_JSON__.json
```

**Running**

Run your local Mainchain JSON RPC Node:

```bash
und $__UND_NETWORK_FLAG__ \
  --rpc \
  --rpcport "8102" \
  --syncmode="full"
```

It should now be possible to interact with the Mainchain `$__MAINCHAIN_NETWORK__`
via <http://localhost:8102> (for example, using MetaMask, or MEW to generate
and send transactions)
