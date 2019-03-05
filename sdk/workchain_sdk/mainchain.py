import requests

from web3 import Web3


def clean_address(address):
    return Web3.toChecksumAddress(address)


def check_und_funds(address):
    und_balance = 0
    address = clean_address(address)

    # Todo: set provider based on selected Mainchain network
    web3 = Web3(Web3.HTTPProvider("http://52.14.173.249:8101"))

    if web3.isAddress(address):
        und_balance = web3.eth.getBalance(address)

    return und_balance


def fund_address(address):
    address = clean_address(address)
    # Todo: set faucet URL based on selected Mainchain network
    faucet_url = "http://52.14.173.249:6969/sendtx"
    params = {"to": address}

    # Todo: catch exceptions
    req = requests.request('GET', faucet_url, params=params, timeout=1)
    return req.text
