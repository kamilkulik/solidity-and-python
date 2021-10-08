from solcx import compile_standard, install_solc
import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simplate_storage_file = file.read()

    install_solc("0.6.0")
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"SimpleStorage.sol": {"content": simplate_storage_file}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.6.0",
    )

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to rinkeby

w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/361adfb1c44349bb9fe2bd69ed1e5316")
)
chain_id = 4
my_address = "0x4A257Dc2c32B4FA61Ca7cb71376896d77dFE66c5"
private_key = os.getenv("PRIVATE_KEY")

# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# get the latest transation
nonce = w3.eth.getTransactionCount(my_address)
# 1. Build a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
# 2. Sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# 3. Send a transaction
print("Deploying the contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# await block confirmation to happen
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")
# WORKING WITH A CONTRACT
# 2 things alwats required:
# contract address
# contract ABI

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# call -> simulate making the call and getting a return value
# transact -> actually making a state change

# initial value of favourite number
print("Updating the contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!")
print(simple_storage.functions.retrieve().call())
