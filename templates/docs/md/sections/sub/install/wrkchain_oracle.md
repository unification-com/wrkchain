## $__SECTION_NUMBER__.$__SUB_SECTION_NUMBER__ Install WRKChain Oracle

One each host assigned to run the WRKChain Oracle:

$__ASSIGNED_ORACLE_HOSTS__

Follow the instructions above to install Golang.

Install the WRKChain Oracle dependencies:

```bash
go get gopkg.in/urfave/cli.v1
go get github.com/unification-com/mainchain
```

Install the WRKChain Oracle software:

```bash
go get github.com/unification-com/oracle
go install github.com/unification-com/oracle/cmd/wrkoracle
```

Check it installed OK:

```bash
wrkoracle --version
```
