function WorkchainRoot(_workchainRootContractAddress,
                       _mainchainWeb3ProviderUrl,
                       _workchainWeb3ProviderUrl,
                       _workchainRootAbi) {

    let abi = _workchainRootAbi.replace(/\\(.)/mg, "$1");

    this.web3jsMainchain = null;
    this.contractAddress = _workchainRootContractAddress;
    this.abi = JSON.parse(abi);

    let self = this;

    this.web3jsMainchain = new Web3(new Web3.providers.HttpProvider(_mainchainWeb3ProviderUrl));
    this.web3jsWorkchain = new Web3(new Web3.providers.HttpProvider(_workchainWeb3ProviderUrl));

    this.workchainRootContract = new this.web3jsMainchain.eth.Contract(this.abi, this.contractAddress);

}

WorkchainRoot.prototype.validateBlock = function(_block_num, _callback) {

    let self = this;
    this.getWorkchainBlock(_block_num).then(workchain_block => {
        this.runBlockHeaderFromRoot(_block_num).then(workchain_root_data => {
            _callback(workchain_block, workchain_root_data);
            return;
        });
        return;
    });
}

WorkchainRoot.prototype.getWorkchainBlock = async function(_block_num) {
    let workchain_block = await this.web3jsWorkchain.eth.getBlock(_block_num);
    return workchain_block;
}

WorkchainRoot.prototype.runBlockHeaderFromRoot = async function (_block_num) {
    let workchain_root_data = await this.getBlockHeaderFromRoot(_block_num);
    return workchain_root_data;
}

WorkchainRoot.prototype.getBlockHeaderFromRoot = function (_block_num) {
    let self = this;
    return new Promise(resolve => {
        self.workchainRootContract.methods.getHeader(_block_num).call().then(function (workchain_root_data) {
            resolve(workchain_root_data);
        })
    });
}

WorkchainRoot.prototype.getCurrentBlockNumber = async function () {
    let blockNumber = await this.web3js.eth.getBlockNumber();
    return blockNumber;
}

