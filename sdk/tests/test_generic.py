import glob
import os

from pathlib import Path


def examples():
    current_script = Path(os.path.abspath(__file__))
    examples_path = current_script.parent.parent.parent / 'examples'
    query = os.path.join(examples_path, "*.json")
    config_files = glob.glob(query)
    return config_files


def test_basic():
    from workchain_sdk.config import parse_config

    config_files = examples()
    assert len(config_files) > 0

    for f in config_files:
        genesis_json = parse_config(f)
        print(genesis_json)


def test_composer():
    from workchain_sdk.composer import generate
    generate()
