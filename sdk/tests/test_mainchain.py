import time


def example_addresses():
    addresses = [
        '0xDccc523747B80c56cdF45aF1aB8bc6E9234b59F9'
    ]
    return addresses


def test_check_und_funds():
    from workchain_sdk.mainchain import check_und_funds

    addresses = example_addresses()
    assert len(addresses) > 0

    for address in addresses:
        current_balance = check_und_funds(address)
        assert current_balance >= 0
