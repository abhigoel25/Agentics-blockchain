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
def getFinancialTerms():
    """
    Retrieve the financial terms of the employment contract.
    
    Returns:
        dict: The financial terms as a list of tuples containing amount, currency, purpose, and frequency.
    """
    try:
        result = contract.functions.getFinancialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligations():
    """
    Retrieve the obligations outlined in the employment contract.
    
    Returns:
        dict: The obligations as a list of tuples containing party and description.
    """
    try:
        result = contract.functions.getObligations().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getTerminationConditions():
    """
    Retrieve the termination conditions of the employment contract.
    
    Returns:
        dict: The termination conditions as a list of tuples containing description.
    """
    try:
        result = contract.functions.getTerminationConditions().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()