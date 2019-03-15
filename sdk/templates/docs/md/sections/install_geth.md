On each computer designated to run your network, you will need to install the 
relevant software.

### $__SECTION_NUMBER__.1 Install Debian packages

`sudo add-apt-repository -y ppa:ethereum/ethereum`

After that you can install the stable version of Go Ethereum:

`
sudo apt-get update
sudo apt-get install ethereum
`

### $__SECTION_NUMBER__.2 Install from source

Assuming that you have Go installed:

`go get -d github.com/ethereum/go-ethereum`

And then install the relevant binary:

`go install github.com/ethereum/go-ethereum/cmd/geth`

The latest documentation regarding installing go-ethereum can be found here:
<https://geth.ethereum.org/install/>
