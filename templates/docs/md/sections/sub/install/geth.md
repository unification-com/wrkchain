On each computer designated to run your network, you will need to install the 
relevant software:

$__NODE_COMPUTERS__

### $__SECTION_NUMBER__.$__SUB_SECTION_NUMBER__ Install Go and Geth

The recommended way to install geth is installing Go and then installing Geth
using Go.

First, install Go version 10.3:

```bash
wget https://dl.google.com/go/go1.10.3.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.10.3.linux-amd64.tar.gz
mkdir ~/.go
```

Then set your GOPATH and GOROOT

```bash
export GOPATH="$$HOME/.go"
export GOROOT="/usr/local/go"
export PATH=$$PATH:$$GOROOT/bin:$$GOPATH/bin
```

**Note:** it's advisable to permanently set these environment variables
 in your shell's `rc`, for example `~/.bashrc`.

The latest documentation regarding installing Go can be found here
<https://golang.org/doc/install>

Next, fetch the go-ethereum codebase:

`go get -d github.com/ethereum/go-ethereum`

And then install the geth binary:

`go install github.com/ethereum/go-ethereum/cmd/geth`

The latest documentation regarding installing go-ethereum can be found here:
<https://geth.ethereum.org/install/>
