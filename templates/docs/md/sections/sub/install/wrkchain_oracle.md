## $__SECTION_NUMBER__.$__SUB_SECTION_NUMBER__ Install WRKChain Oracle

One each host assigned to run the WRKChain Oracle:

$__ASSIGNED_ORACLE_HOSTS__

1. Follow the instructions above to install Golang.

2. Clone the repo:

```bash
git clone https://github.com/unification-com/oracle
```

3. Install the `wrkoracle` CMD:

```bash
cd oracle
go install ./cmd/wrkoracle
```

4. Check it installed OK:

```bash
wrkoracle --version
```
