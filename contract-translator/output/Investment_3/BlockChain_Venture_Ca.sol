// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPreferredStockPurchaseAgreement {
    address public company;
    address public investor;

    uint256 public constant priceAmount = 8000000 ether; // Price in USD, converted to wei for payment handling
    uint256 public constant totalInvestmentAmount = 10000000 ether; // Total investment amount in wei
    uint256 public constant startDate = 1735689600; // 2025-01-01 in UNIX timestamp
    uint256 public constant redemptionTriggerDate = 1893561600; // 2030-01-01 in UNIX timestamp
    uint256 public constant preMoneyValuation = 30000000 ether;
    uint256 public constant postMoneyValuation = 40000000 ether;
    uint256 public constant investorOwnershipPercentage = 25; // 25%
    
    bool public fundsRaised = false;
    bool public obligationTriggered = false;
    uint256 public obligationDeadline;

    event InvestmentReceived(address indexed investor, uint256 amount);
    event RedemptionObligationTriggered(uint256 deadline);

    modifier onlyCompany() {
        require(msg.sender == company, "Only company can call this function");
        _;
    }

    modifier onlyInvestor() {
        require(msg.sender == investor, "Only investor can call this function");
        _;
    }

    modifier afterStartDate() {
        require(block.timestamp >= startDate, "Investment period has not started");
        _;
    }

    modifier beforeRedemptionDate() {
        require(block.timestamp < redemptionTriggerDate, "Redemption trigger date has passed");
        _;
    }

    constructor(address _company, address _investor) {
        company = _company;
        investor = _investor;
        obligationDeadline = redemptionTriggerDate + 365 days; // 12 months from redemption trigger event
    }

    function raiseFunds() external onlyInvestor afterStartDate {
        require(!fundsRaised, "Investment already raised");
        require(msg.value == totalInvestmentAmount, "Incorrect investment amount");

        fundsRaised = true;
        emit InvestmentReceived(msg.sender, msg.value);
    }

    function triggerRedemptionObligation() external onlyCompany beforeRedemptionDate {
        require(!obligationTriggered, "Redemption obligation has already been triggered");
        obligationTriggered = true;
        emit RedemptionObligationTriggered(obligationDeadline);
    }

    function redeemShares() external onlyCompany {
        require(obligationTriggered, "Redemption obligation not triggered");
        require(block.timestamp <= obligationDeadline, "Obligation deadline has passed");
        
        // Logic for redeeming shares would go here

        obligationTriggered = false; // Reset the state for next potential redemption
    }

    // Fallback function to receive Ether
    receive() external payable {
        require(msg.sender == investor, "Only investor can send Ether");
        require(msg.value == totalInvestmentAmount, "Investment amount must be exactly the total investment amount");
        raiseFunds();
    }

    // Function to withdraw funds by company after successful fundraising
    function withdrawFunds() external onlyCompany {
        require(fundsRaised, "No funds to withdraw");
        payable(company).transfer(address(this).balance);
        fundsRaised = false; // Reset funds raised state after withdrawal
    }
}