// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract SeriesAPreferredStock is Ownable {
    string public constant name = "Series A Preferred Stock";
    uint256 public constant totalShares = 1250000;
    uint256 public constant purchasePricePerShare = 8e18; // 8 USD (assume 18 decimal places)
    uint256 public constant investmentAmount = 10000000e18; // 10,000,000 USD
    address public companyAddress;
    address public investorAddress;
    uint256 public redemptionDeadline;
    bool public ipoQualified = false;
    uint256 public dividendsAccrued;
    uint256 public constant dividendPercentage = 8; // 8% non-cumulative dividend

    event InvestmentReceived(address indexed investor, uint256 amount);
    event SharesRedeemed(address indexed company, uint256 amount);
    event IpoQualified(bool qualified);
    
    modifier onlyInvestor() {
        require(msg.sender == investorAddress, "Only investor can call this function");
        _;
    }

    constructor(address _investorAddress) {
        companyAddress = msg.sender; // Assign the contract deployer as the company
        investorAddress = _investorAddress;
        redemptionDeadline = block.timestamp + 5 * 365 days; // January 1, 2030
    }
    
    function invest() external payable onlyInvestor {
        require(msg.value == investmentAmount, "Incorrect investment amount");
        require(block.timestamp >= block.timestamp + 1 days, "Investment starts January 1, 2025");

        emit InvestmentReceived(msg.sender, msg.value);
    }
    
    function redeemShares() external {
        require(block.timestamp > redemptionDeadline, "Redemption can only occur after the deadline");
        require(!ipoQualified, "Cannot redeem shares if IPO is qualified");

        // Logic to handle company compliance for share redemption
        payable(companyAddress).transfer(investmentAmount);
        emit SharesRedeemed(companyAddress, totalShares);
    }

    function qualifyIpo() external onlyOwner {
        ipoQualified = true;
        emit IpoQualified(ipoQualified);
    }
    
    function calculateDividends() external view returns (uint256) {
        return (totalShares * dividendPercentage) / 100;
    }
    
    function withdrawDividends() external onlyInvestor {
        uint256 dividendsToWithdraw = calculateDividends();
        require(dividendsToWithdraw > dividendsAccrued, "No dividends available");

        dividendsAccrued += dividendsToWithdraw;
        payable(msg.sender).transfer(dividendsToWithdraw);
    }

    function getContractDetails() external view returns (address, address, uint256, bool) {
        return (companyAddress, investorAddress, redemptionDeadline, ipoQualified);
    }
}