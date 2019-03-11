
## 3. Running your Validators

### 3.$__VALIDATOR_NUM__ Validator $__VALIDATOR_NUM__

Copy the generated `genesis.json` to the computer you will be running Validator $__VALIDATOR_NUM__

Run

`geth init /PATH/TO/YOUR/GENERATED/genesis.json`  
`geth $__BOOTNODE__--networkid "$__WORKCHAIN_NETWORK_ID__" --verbosity=4  --syncmode=full --mine --gasprice "0" --etherbase $__EV_PUBLIC_ADDRESS__ --unlock $__EV_PUBLIC_ADDRESS__ --password ~/.walletpassword`

