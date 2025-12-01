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
abi_path = Path(__file__).parent / 'CloudTech__MediCare_N.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("CloudTech__MediCare_N")

@mcp.tool()
def addObligation():
    """Add an obligation to the service agreement. 
    Can be called by the contract owner.
    
    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.addObligation().buildTransaction({
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
def makeMonthlyPayment():
    """Make a monthly payment to the service provider.
    Can be called by the client.
    
    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.makeMonthlyPayment().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'value': web3.to_wei(1, 'ether')  # Example amount
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def makeSetupPayment():
    """Make a setup payment to the service provider.
    Can be called by the client.
    
    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.makeSetupPayment().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'value': web3.to_wei(0.5, 'ether')  # Example amount
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def terminateContract():
    """Terminate the service agreement contract.
    Can be called by the contract owner.
    
    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.terminateContract().buildTransaction({
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
    """Retrieve the list of obligations in the service agreement.
    
    Returns:
        dict: A dictionary containing the list of obligations.
    """
    try:
        result = contract.functions.getObligations().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def isContractActive():
    """Check if the contract is currently active.
    
    Returns:
        dict: A dictionary indicating the status of the contract.
    """
    try:
        result = contract.functions.isContractActive().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def timeUntilTermination():
    """Get the time remaining until the contract termination.
    
    Returns:
        dict: A dictionary containing the time until termination.
    """
    try:
        result = contract.functions.timeUntilTermination().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()