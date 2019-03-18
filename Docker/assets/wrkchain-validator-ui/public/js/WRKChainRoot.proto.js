function WRKChain(_wrkchainRootContractAddress,
                       _mainchainWeb3ProviderUrl,
                       _wrkchainWeb3ProviderUrl,
                       _wrkchainRootAbi) {

    let abi = _wrkchainRootAbi.replace(/\\(.)/mg, "$1");

    this.web3jsMainchain = null;
    this.contractAddress = _wrkchainRootContractAddress;
    this.abi = JSON.parse(abi);

    let self = this;

    this.web3jsMainchain = new Web3(new Web3.providers.HttpProvider(_mainchainWeb3ProviderUrl));
    this.web3jsWrkchain = new Web3(new Web3.providers.HttpProvider(_wrkchainWeb3ProviderUrl));

    this.wrkchainRootContract = new this.web3jsMainchain.eth.Contract(this.abi, this.contractAddress);

}

WRKChain.prototype.validateBlock = function(_block_num, _callback) {

    let self = this;
    this.getWrkchainBlock(_block_num).then(wrkchain_block => {
        this.runBlockHeaderFromRoot(_block_num).then(wrkchain_root_data => {
            _callback(wrkchain_block, wrkchain_root_data);
            return;
        });
        return;
    });
}

WRKChain.prototype.getWrkchainBlock = async function(_block_num) {
    let wrkchain_block = await this.web3jsWrkchain.eth.getBlock(_block_num);
    return wrkchain_block;
}

WRKChain.prototype.runBlockHeaderFromRoot = async function (_block_num) {
    let wrkchain_root_data = await this.getBlockHeaderFromRoot(_block_num);
    return wrkchain_root_data;
}

WRKChain.prototype.getBlockHeaderFromRoot = function (_block_num) {
    let self = this;
    return new Promise(resolve => {
        self.wrkchainRootContract.methods.getHeader(_block_num).call().then(function (wrkchain_root_data) {
            resolve(wrkchain_root_data);
        })
    });
}

WRKChain.prototype.getCurrentBlockNumber = async function () {
    let blockNumber = await this.web3js.eth.getBlockNumber();
    return blockNumber;
}

