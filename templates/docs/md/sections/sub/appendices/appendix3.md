
### $__SECTION_NUMBER__.$__SUB_SECTION_NUMBER__ Appendix 3: WRKChain Block Validator

Unification Foundation has released a simple WRKChain Validator application, which
can be downloaded and run on any computer:

```bash
git clone https://github.com/unification-com/wrkchain-validator
cd wrkchain-validator
npm install
```

In order to run, you will need to configure a `.env`, as follows:

```text
MAINCHAIN_EXPLORER_URL=
MAINCHAIN_WEB3_PROVIDER_URL=$__MAINCHAIN_WEB3_PROVIDER_URL__
WRKCHAIN_NAME=$__WRKCHAIN_NAME__
WRKCHAIN_ROOT_ABI=[{"constant":true,"inputs":[],"name":"chain_id","outputs":[{"name":"","type":"uint64"}],"payable":false,"stateMutability":"view","type":"function","signature":"0x3af973b1"},{"constant":true,"inputs":[{"name":"","type":"uint64"}],"name":"block_headers","outputs":[{"name":"height","type":"uint64"},{"name":"hash","type":"bytes32"},{"name":"parent_hash","type":"bytes32"},{"name":"receipt_root","type":"bytes32"},{"name":"tx_root","type":"bytes32"},{"name":"state_root","type":"bytes32"},{"name":"sealer","type":"address"}],"payable":false,"stateMutability":"view","type":"function","signature":"0xa794c9fd"},{"constant":true,"inputs":[],"name":"genesis_hash","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function","signature":"0xc366ea9e"},{"inputs":[{"name":"_chain_id","type":"uint64"},{"name":"_genesis_hash","type":"bytes32"},{"name":"_evs","type":"address[]"}],"payable":false,"stateMutability":"nonpayable","type":"constructor","signature":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"height","type":"uint64"},{"indexed":false,"name":"hash","type":"bytes32"},{"indexed":false,"name":"parent_hash","type":"bytes32"},{"indexed":false,"name":"receipt_root","type":"bytes32"},{"indexed":false,"name":"tx_root","type":"bytes32"},{"indexed":false,"name":"state_root","type":"bytes32"},{"indexed":false,"name":"sealer","type":"address"}],"name":"RecordHeader","type":"event","signature":"0xceec4c706f6e91cdd751ea972853f6862c309ad04ec22a41ca891868e495dd2c"},{"constant":false,"inputs":[{"name":"_height","type":"uint64"},{"name":"_hash","type":"bytes32"},{"name":"_parent_hash","type":"bytes32"},{"name":"_receipt_root","type":"bytes32"},{"name":"_tx_root","type":"bytes32"},{"name":"_state_root","type":"bytes32"},{"name":"_sealer","type":"address"},{"name":"_chain_id","type":"uint64"}],"name":"recordHeader","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function","signature":"0x3f10cc1e"},{"constant":false,"inputs":[{"name":"_new_evs","type":"address[]"}],"name":"setEvs","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function","signature":"0xdb829798"},{"constant":true,"inputs":[{"name":"_height","type":"uint64"}],"name":"getHeader","outputs":[{"name":"hash","type":"bytes32"},{"name":"parent_hash","type":"bytes32"},{"name":"receipt_root","type":"bytes32"},{"name":"tx_root","type":"bytes32"},{"name":"state_root","type":"bytes32"},{"name":"sealer","type":"address"}],"payable":false,"stateMutability":"view","type":"function","signature":"0xb203e111"},{"constant":true,"inputs":[],"name":"getGenesis","outputs":[{"name":"genesis_hash_","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function","signature":"0x1a43bcb5"},{"constant":true,"inputs":[],"name":"getChainId","outputs":[{"name":"chain_id_","type":"uint64"}],"payable":false,"stateMutability":"view","type":"function","signature":"0x3408e470"},{"constant":true,"inputs":[],"name":"getEvs","outputs":[{"name":"current_evs_idx_","type":"address[]"}],"payable":false,"stateMutability":"view","type":"function","signature":"0xc5cb0a98"},{"constant":true,"inputs":[{"name":"_ev","type":"address"}],"name":"isEv","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function","signature":"0x9e186c93"}]
WRKCHAIN_ROOT_CONTRACT_ADDRESS=
WRKCHAIN_ROOT_WRITE_TIMEOUT=$__ORACLE_WRITE_FREQUENCY__
WRKCHAIN_WEB3_PROVIDER_URL=
WRKCHAIN_VALIDATOR_SERVICE_PORT=4040
```

Once configured, run:

```bash
npm start
```
