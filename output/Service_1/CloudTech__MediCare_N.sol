// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ServiceAgreement {
    address private serviceProvider;
    address private client;

    uint256 public setupFee = 5000 * 10**18; // Assuming fee is in wei
    uint256 public monthlyFee = 15000 * 10**18; // Assuming fee is in wei
    uint256 public lastPaymentTime;
    uint256 public contractStart;
    uint256 public contractEnd;
    uint256 public totalPaymentsMade;

    enum State { Active, Terminated }
    State public contractState;

    struct Obligation {
        string party;
        string description;
        string penaltyForBreach;
    }

    Obligation[] public obligations;

    event PaymentMade(address indexed payer, uint256 amount, uint256 timestamp);
    event ContractTerminated(address terminatedBy, uint256 timestamp);
    event ObligationAdded(string party, string description, string penalty);

    modifier onlyServiceProvider() {
        require(msg.sender == serviceProvider, "Not authorized: Service Provider");
        _;
    }

    modifier onlyClient() {
        require(msg.sender == client, "Not authorized: Client");
        _;
    }

    modifier isActive() {
        require(contractState == State.Active, "Contract is not active");
        _;
    }

    constructor(address _client) {
        serviceProvider = msg.sender;
        client = _client;
        contractStart = block.timestamp; // Assuming starting at deployment
        contractEnd = block.timestamp + 365 days; // 1 year duration
        contractState = State.Active;

        obligations.push(Obligation("CloudTech Solutions, Inc.", 
            "Provide services including cloud infrastructure management, 24/7 monitoring, technical support, and monthly optimization", 
            "10% monthly credit for each hour below 99.95% uptime"));
        
        obligations.push(Obligation("MediCare Network, Inc.", 
            "Make payments as outlined in financial terms", 
            "1.5% per month on overdue amounts"));
    }

    function makeSetupPayment() external payable onlyClient isActive {
        require(msg.value >= setupFee, "Insufficient funds for setup fee");
        totalPaymentsMade += msg.value;
        emit PaymentMade(msg.sender, msg.value, block.timestamp);
    }

    function makeMonthlyPayment() external payable onlyClient isActive {
        require(block.timestamp >= lastPaymentTime + 30 days, "Payment not due yet");
        require(msg.value >= monthlyFee, "Insufficient funds for monthly fee");
        
        totalPaymentsMade += msg.value;
        lastPaymentTime = block.timestamp;
        emit PaymentMade(msg.sender, msg.value, block.timestamp);
    }

    function terminateContract() external {
        require(msg.sender == serviceProvider || msg.sender == client, "Not authorized to terminate");
        require(contractState == State.Active, "Contract is already terminated");

        contractState = State.Terminated;
        emit ContractTerminated(msg.sender, block.timestamp);
    }

    function addObligation(string memory _party, string memory _description, string memory _penalty) external onlyServiceProvider {
        obligations.push(Obligation(_party, _description, _penalty));
        emit ObligationAdded(_party, _description, _penalty);
    }

    function getObligations() external view returns (Obligation[] memory) {
        return obligations;
    }

    function isContractActive() external view returns (bool) {
        return contractState == State.Active;
    }

    function timeUntilTermination() external view returns (uint256) {
        if (contractState == State.Active) {
            return (contractEnd > block.timestamp) ? contractEnd - block.timestamp : 0;
        }
        return 0;
    }
    
    receive() external payable {}
}