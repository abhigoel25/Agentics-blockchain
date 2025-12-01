import os
from web3 import Web3
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

# Setup Web3
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "_company", "type": "address"},
            {"internalType": "address", "name": "_investor", "type": "address"}
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [],
        "name": "company",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "investor",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "priceAmount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalInvestmentAmount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "startDate",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "redemptionTriggerDate",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "preMoneyValuation",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "postMoneyValuation",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "investorOwnershipPercentage",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "fundsRaised",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "obligationTriggered",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "obligationDeadline",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "raiseFunds",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "triggerRedemptionObligation",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "redeemShares",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "withdrawFunds",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": false,
        "inputs": [
            {"indexed": true, "internalType": "address", "name": "investor", "type": "address"},
            {"indexed": false, "internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "InvestmentReceived",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {"indexed": false, "internalType": "uint256", "name": "deadline", "type": "uint256"}
        ],
        "name": "RedemptionObligationTriggered",
        "type": "event"
    },
    {
        "payable": true,
        "stateMutability": "payable",
        "type": "receive"
    }
]

contract = web3.eth.contract(address=Web3.toChecksumAddress(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("BlockChain_Venture_Ca")

@mcp.tool()
def company():
    """Returns the address of the company.
    
    Accessible by: Anyone
    Returns:
        str: Company address.
    """
    try:
        return {"result": contract.functions.company().call()}
    except Exception as e:
        return {"error": str(e)}

@tool()
def investor():
    """Returns the address of the investor.
    
    Accessible by: Anyone
    Returns:
        str: Investor address.
    """
    try:
        return {"result": contract.functions.investor().call()}
    except Exception as e:
        return {"error": str(e)}

@tool()
def priceAmount():
    """Returns the price amount of the investment.
    
    Accessible by: Anyone
    Returns:
        int: Price amount as uint256.
    """
    try:
        return {"result": contract.functions.priceAmount().call()}
    except Exception as e:
        return {"error": str(e)}

@tool()
def totalInvestmentAmount():
    """Returns the total investment amount.
    
    Accessible by: Anyone
    Returns:
        int: Total investment amount as uint256.
    """
    try:
        return {"result": contract.functions.totalInvestmentAmount().call()}
    except Exception as e:
        return {"error": str(e)}

@tool()
def startDate():
    """Returns the start date of the investment.
    
    Accessible by: Anyone
    Returns:
        int: Start date as uint256.
    """
    try:
        return {"result": contract.functions.startDate().call()}
    except Exception as e:
        return {"error": str(e)}

@tool()
def redemptionTriggerDate():
    """Returns the redemption trigger date.
    
    Accessible by: Anyone
    Returns:
        int: Redemption trigger date as uint256.
    """
    try:
        return {"result": contract.functions.redemptionTriggerDate().call()}
    except Exception as e:
        return {"error": str(e)}

@tool()
def preMoneyValuation():
    """Returns the pre-money valuation.
    
    Accessible by: Anyone
    Returns:
        int: Pre-money valuation as uint256.
    """
    try:
        return {"result": contract.functions.preMoneyValuation().call()}
    except Exception as e:
        return {"error": str(e)}

@tool()
def postMoneyValuation():
    """Returns the post-money valuation.
    
    Accessible by: Anyone
    Returns:
        int: Post-money valuation as uint256.
    """
    try:
        return {"result": contract.functions.postMoneyValuation().call()}
    except Exception as e:
        return {"error": str(e)}

@tool()
def investorOwnershipPercentage():
    """Returns the ownership percentage of the investor.
    
    Accessible by: Anyone
    Returns:
        int: Ownership percentage as uint256.
    """
    try:
        return {"result": contract.functions.investorOwnershipPercentage().call()}
    except Exception as e:
        return {"error": str(e)}

@tool()
def fundsRaised():
    """Checks if the funds have been raised.
    
    Accessible by: Anyone
    Returns:
        bool: True if funds are raised, otherwise False.
    """
    try:
        return {"result": contract.functions.fundsRaised().call()}
    except Exception as e:
        return {"error": str(e)}

@tool()
def obligationTriggered():
    """Checks if the obligation has been triggered.
    
    Accessible by: Anyone
    Returns:
        bool: True if obligation triggered, otherwise False.
    """
    try:
        return {"result": contract.functions.obligationTriggered().call()}
    except Exception as e:
        return {"error": str(e)}

@tool()
def obligationDeadline():
    """Returns the deadline for obligation.
    
    Accessible by: Anyone
    Returns:
        int: Obligation deadline as uint256.
    """
    try:
        return {"result": contract.functions.obligationDeadline().call()}
    except Exception as e:
        return {"error": str(e)}

@tool()
def raiseFunds():
    """Initiates the fund raising process.
    
    Accessible by: Company
    Returns:
        str: Transaction hash.
    """
    try:
        tx = contract.functions.raiseFunds().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.getTransactionCount(account.address),
            'gas': 2000000,
            'gasPrice': web3.toWei('20', 'gwei')
        })
        signed_tx = web3.eth.account.signTransaction(tx, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return {"tx_hash": web3.toHex(tx_hash)}
    except Exception as e:
        return {"error": str(e)}

@tool()
def triggerRedemptionObligation():
    """Triggers the redemption obligation.
    
    Accessible by: Company
    Returns:
        str: Transaction hash.
    """
    try:
        tx = contract.functions.triggerRedemptionObligation().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.getTransactionCount(account.address),
            'gas': 2000000,
            'gasPrice': web3.toWei('20', 'gwei')
        })
        signed_tx = web3.eth.account.signTransaction(tx, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return {"tx_hash": web3.toHex(tx_hash)}
    except Exception as e:
        return {"error": str(e)}

@tool()
def redeemShares():
    """Redeems shares for the investor.
    
    Accessible by: Investor
    Returns:
        str: Transaction hash.
    """
    try:
        tx = contract.functions.redeemShares().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.getTransactionCount(account.address),
            'gas': 2000000,
            'gasPrice': web3.toWei('20', 'gwei')
        })
        signed_tx = web3.eth.account.signTransaction(tx, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return {"tx_hash": web3.toHex(tx_hash)}
    except Exception as e:
        return {"error": str(e)}

@tool()
def withdrawFunds():
    """Withdraws funds raised from the investment.
    
    Accessible by: Company
    Returns:
        str: Transaction hash.
    """
    try:
        tx = contract.functions.withdrawFunds().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.getTransactionCount(account.address),
            'gas': 2000000,
            'gasPrice': web3.toWei('20', 'gwei')
        })
        signed_tx = web3.eth.account.signTransaction(tx, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return {"tx_hash": web3.toHex(tx_hash)}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run(transport="stdio")