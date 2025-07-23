import asyncio
from web3 import Web3
from eth_account import Account

async def deploy_contract(web3, account, contract_interface, constructor_args):
    Contract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bytecode'])
    tx = Contract.constructor(**constructor_args).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei')
    })
    signed_tx = account.sign_transaction(tx)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

# Usage example
async def main():
    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_PROJECT_ID'))
    account = Account.from_key('YOUR_PRIVATE_KEY')
    # contract_input_json should be loaded from your compiler output
    contract_interface = {
        'abi': contract_input_json['abi'],
        'bytecode': contract_input_json['bytecode']
    }
    constructor_args = {"param": "value"}
    receipt = await deploy_contract(web3, account, contract_interface, constructor_args)
    print("Contract deployed at:", receipt.contractAddress)

asyncio.run(main())