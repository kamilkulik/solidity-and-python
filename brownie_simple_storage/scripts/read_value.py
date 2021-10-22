from brownie import accounts, config, SimpleStorage


def read_contract():
    simple_storage = SimpleStorage[-1]  # the latest deployment
    # ABI
    # ADDRESS
    simple_storage.retrieve()


def main():
    read_contract()
