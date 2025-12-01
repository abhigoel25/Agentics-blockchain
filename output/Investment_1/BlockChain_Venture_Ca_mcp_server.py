import os
import json
from pathlib import Path
from dotenv import load_dotenv
from web3 import Web3
from fastmcp import FastMCP

# Load .env from the same directory as this script
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Load ABI from the same directory as this script
abi_path = Path(__file__).parent / 'BlockChain_Venture_Ca.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("BlockChain_Venture_Ca")

@mcp.tool()
def calculateDividends():
    """Calculates the dividends from the investment contract.
    
    This function can be called by anyone.

    Returns:
        dict: A dictionary containing the result of the dividend calculation.
    """
    try:
        result = contract.functions.calculateDividends().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getContractDetails():
    """Retrieves the details of the investment contract.

    This function can be called by anyone.

    Returns:
        dict: A dictionary containing the contract details including addresses and status.
    """
    try:
        details = contract.functions.getContractDetails().call()
        return {
            "company_address": details[0],
            "investor_address": details[1],
            "investment_amount": details[2],
            "qualified": details[3]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def invest():
    """Allows an investor to make an investment in the contract.

    This function can be called by the investor.

    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.invest().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'value': web3.to_wei(1, 'ether')  # Example amount to invest
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def qualifyIpo():
    """Qualifies the investment for an IPO.

    This function can be called by the company.

    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.qualifyIpo().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def redeemShares():
    """Allows the investor to redeem their shares in the contract.

    This function can be called by the investor.

    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.redeemShares().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def withdrawDividends():
    """Allows the investor to withdraw their dividends.

    This function can be called by the investor.

    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.withdrawDividends().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()