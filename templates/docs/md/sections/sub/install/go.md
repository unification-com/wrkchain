
## $__SECTION_NUMBER__.$__SUB_SECTION_NUMBER__ Install Golang

The recommended way to install many of the packages used in this SDK
is to first install Go, then use `go get`.

First, install Go version $__GO_VERSION__:

```bash
wget https://dl.google.com/go/go1.$__GO_VERSION__.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.$__GO_VERSION__.linux-amd64.tar.gz
mkdir $$HOME/.go
```

Then set your `GOPATH` and `GOROOT`:

```bash
export GOPATH="$$HOME/.go"
export GOROOT="/usr/local/go"
export PATH=$$PATH:$$GOROOT/bin:$$GOPATH/bin
```

**Note:** it's advisable to permanently set these environment variables
 in your shell's `rc`, for example `$$HOME/.bashrc`.

The latest documentation regarding installing Go can be found here
<https://golang.org/doc/install>
