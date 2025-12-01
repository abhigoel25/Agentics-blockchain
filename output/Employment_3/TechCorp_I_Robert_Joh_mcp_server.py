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
abi_path = Path(__file__).parent / 'TechCorp_I_Robert_Joh.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("TechCorp_I_Robert_Joh")

@mcp.tool()
def makePayment(_amount: int, _currency: str):
    """
    Makes a payment to the employee.
    
    Parameters:
    - _amount (int): The amount to be paid.
    - _currency (str): The currency of the payment.
    
    Returns:
    - dict: A dictionary containing the transaction hash.
    
    """

    try:
        txn = contract.functions.makePayment(_amount, _currency).buildTransaction({
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
def fulfillObligation(_party: str, _description: str):
    """
    Fulfills an obligation in the employment contract.
    
    Parameters:
    - _party (str): The party fulfilling the obligation.
    - _description (str): A description of the fulfillment.
    
    Returns:
    - dict: A dictionary containing the transaction hash.
    
    """
    
    try:
        txn = contract.functions.fulfillObligation(_party, _description).buildTransaction({
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
def terminateAgreement(_reason: str):
    """
    Terminates the employment agreement.
    
    Parameters:
    - _reason (str): The reason for the termination.
    
    Returns:
    - dict: A dictionary containing the transaction hash.
    
    """
    
    try:
        txn = contract.functions.terminateAgreement(_reason).buildTransaction({
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
def getObligations():
    """
    Retrieves the obligations under the employment agreement.
    
    Returns:
    - list: A list of obligations.
    
    """
    
    try:
        result = contract.functions.getObligations().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFinancialTerms():
    """
    Retrieves the financial terms of the employment agreement.
    
    Returns:
    - list: A list of financial terms.
    
    """
    
    try:
        result = contract.functions.getFinancialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()