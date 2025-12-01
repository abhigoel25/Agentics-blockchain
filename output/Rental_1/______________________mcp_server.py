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
abi_path = Path(__file__).parent / 'rental_contract.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("RentalContract")

@mcp.tool()
def isObligationMet():
    """Check if the rental obligations are met.
    
    Returns:
        dict: Result of the obligation status, example: {"result": True}
    """
    try:
        result = contract.functions.isObligationMet().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def payRent():
    """Pay the rent for the rental period.
    
    Returns:
        dict: Transaction hash of the rent payment.
    """
    try:
        txn = contract.functions.payRent().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'value': web3.to_wei(5, 'ether')  # Adjust the amount as needed
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def fulfillObligation(obligation: str):
    """Fulfill a rental obligation.
    
    Args:
        obligation (str): The obligation to fulfill.

    Returns:
        dict: Transaction hash of the obligation fulfillment.
    """
    try:
        txn = contract.functions.fulfillObligation(obligation).buildTransaction({
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
def terminateRental(reason: str):
    """Terminate the rental agreement.
    
    Args:
        reason (str): Reason for terminating the rental.

    Returns:
        dict: Transaction hash of the rental termination.
    """
    try:
        txn = contract.functions.terminateRental(reason).buildTransaction({
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
def tenant():
    """Get the tenant's address.
    
    Returns:
        dict: Tenant's address, example: {"result": "0x..."}
    """
    try:
        result = contract.functions.tenant().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def landlord():
    """Get the landlord's address.
    
    Returns:
        dict: Landlord's address, example: {"result": "0x..."}
    """
    try:
        result = contract.functions.landlord().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def paymentDueDate():
    """Get the payment due date.
    
    Returns:
        dict: Payment due date, example: {"result": 1234567890}
    """
    try:
        result = contract.functions.paymentDueDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def rentalStart():
    """Get the rental start date.
    
    Returns:
        dict: Rental start date, example: {"result": 1234567890}
    """
    try:
        result = contract.functions.rentalStart().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def rentalEnd():
    """Get the rental end date.
    
    Returns:
        dict: Rental end date, example: {"result": 1234567890}
    """
    try:
        result = contract.functions.rentalEnd().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()