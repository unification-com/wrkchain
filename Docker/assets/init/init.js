var bip39 = require('bip39')
var hdkey = require('ethereumjs-wallet/hdkey')

function get_address(mnemonic, _path) {
    var hdwallet = hdkey.fromMasterSeed(bip39.mnemonicToSeed(mnemonic));
    var path = "m/44'/60'/0'/0/" + _path;
    var wallet = hdwallet.derivePath(path).getWallet();
    console.log(wallet.getAddressString());
}

function get_private_key(mnemonic, _path) {
    var hdwallet = hdkey.fromMasterSeed(bip39.mnemonicToSeed(mnemonic));
    var path = "m/44'/60'/0'/0/" + _path;
    var wallet = hdwallet.derivePath(path).getWallet();
    var private_key = wallet.getPrivateKeyString();
    console.log(private_key.substr(2));
}

function gen_mnemonic() {
  const mnemonic = bip39.generateMnemonic();
  console.log(mnemonic);
}

function main() {
     let args = process.argv.slice(2);

     switch (args[0]) {
       case 'mnemonic':
           gen_mnemonic();
           break;
       case 'address':
           var mnemonic = args[1];
           var path = args[2];
           get_address(mnemonic, path);
           break;
       case 'private_key':
           var mnemonic = args[1];
           var path = args[2];
           get_private_key(mnemonic, path);
           break;
    }
}

main();

//patient rabbit volcano depth wrong shrug car soldier because parade journey extend