function WRKChainEventWatcher(_contractAddress, _web3ProviderUrl, _abi) {

    let abi = _abi.replace(/\\(.)/mg, "$1");

    this.web3js = null;
    this.contractAddress = _contractAddress;
    this.abi = JSON.parse(abi);
    this.lastEvent = null;

    let self = this;

    this.web3js = new Web3(new Web3.providers.HttpProvider(_web3ProviderUrl));

    this.wrkchainRootContract = new this.web3js.eth.Contract(this.abi, this.contractAddress);

}

WRKChainEventWatcher.prototype.getLatestRecordedHeader = function(_callback) {

    let self = this;

    this.getCurrentBlockNumber().then(blockNumber => {
        self.wrkchainRootContract.getPastEvents('RecordHeader', {
            fromBlock: blockNumber -1,
            toBlock: 'latest'
        }, (error, events) => {
           console.log(events);
           if(error) {
               console.log("error", error);
               if(self.lastEvent != null) {
                   _callback(true, self.lastEvent);
               } else {
                   _callback(false, error);
               }
           } else {
               self.lastEvent = events;
               _callback(true, events);
           }
         });
        return;
    });
}

WRKChainEventWatcher.prototype.getCurrentBlockNumber = async function () {
    let blockNumber = await this.web3js.eth.getBlockNumber();
    console.log("blockNumber:",blockNumber);
    return blockNumber;
}