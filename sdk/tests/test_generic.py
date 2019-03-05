def test_basic():
    f = "/examples/config.json"

    from workchain_sdk.config import check_valid
    check_valid(f)


def test_genesis():
    from workchain_sdk.genesis import build_genesis
    build_genesis()
