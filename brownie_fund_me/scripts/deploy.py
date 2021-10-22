from brownie import config, FundMe, MockV3Aggregator, network
from scripts.utils import deploy_mocks, get_account


def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contract
    # becase it is used in the contract's constructor
    # if we are on a persistent network like rinkeby, use associated address
    # otherwise, deploy mocks
    if network.show_active() != "development":
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
    # ValueError: Explorer API not set for this network
    # Terminating local RPC client...
    # means that we are trying to verify a transaction on a network which doesn't offer this option
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract depoyed to {fund_me.address}")


def main():
    deploy_fund_me()
