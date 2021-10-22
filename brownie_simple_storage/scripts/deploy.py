from brownie import accounts, config, network, SimpleStorage


def deploy_simple_storage():
    # # getting private key from password protected brownie managed secrets store
    # account = accounts.load("freecodecamp-account")
    # # getting private key from the .env file using os
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # # getting account from explicitly defined variable in brownie config
    # account = accounts.add(config["wallets"]["from_key"])
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)  # how many blocks we want to wait for the transaction to finish
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
