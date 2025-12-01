// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SalesAndPurchaseAgreement {

    // Parties
    struct Party {
        string name;
        address wallet;
        bool isSeller;
    }

    Party public seller;
    Party public buyer;

    // Financial terms
    struct FinancialTerm {
        uint256 amount; // amount in wei (for USD conversion, this should be handled off-chain)
        string purpose;
        bool paid;
    }

    FinancialTerm[] public financialTerms;

    // Dates
    struct Date {
        string dateType;
        string value; // e.g. "December 20, 2024"
    }

    Date public contractSigningDate;
    Date public deliveryDate;

    // Assets
    struct Asset {
        string assetType;
        string description;
        string location;
        uint256 quantity;
        uint256 value; // in wei (should reflect USD value converted)
    }

    Asset public asset;

    // Obligations
    struct Obligation {
        string party; // Party name
        string description;
    }

    Obligation[] public obligations;

    // Special terms
    string[] public specialTerms;

    // Termination conditions
    struct TerminationCondition {
        string condition;
        string penalty;
    }

    TerminationCondition[] public terminationConditions;

    // Events
    event PaymentMade(address indexed by, uint256 amount, string purpose);
    event ObligationsMet(string party, string description);
    event ContractTerminated(string reason);

    // Access control
    modifier onlySeller() {
        require(msg.sender == seller.wallet, "Not authorized: Only seller can perform this action");
        _;
    }

    modifier onlyBuyer() {
        require(msg.sender == buyer.wallet, "Not authorized: Only buyer can perform this action");
        _;
    }

    // Constructor
    constructor(
        address _sellerWallet,
        address _buyerWallet
    ) {
        seller = Party("TechGear Manufacturing LLC", _sellerWallet, true);
        buyer = Party("RetailChain Corp", _buyerWallet, false);
        
        // Initialize financial terms
        financialTerms.push(FinancialTerm(1275000 ether, "Down payment", false));
        financialTerms.push(FinancialTerm(1700000 ether, "Payment upon production completion", false));
        financialTerms.push(FinancialTerm(1275000 ether, "Payment upon delivery and inspection", false));

        // Set contract signing and delivery dates
        contractSigningDate = Date("contract_signing", "December 20, 2024");
        deliveryDate = Date("delivery", "January 31, 2025");

        // Initialize asset
        asset = Asset("goods", "Industrial Robotic Arms, Model X-500", "Buyer's warehouse in New Jersey", 50, 4250000 ether);

        // Initialize obligations
        obligations.push(Obligation("Seller", "Warrant the goods free from defects for 24 months from delivery"));
        obligations.push(Obligation("Buyer", "Inspect goods within 15 days and report defects within 30 days"));

        // Initialize special terms
        specialTerms.push("Defective units are subject to replacement or repair.");
        specialTerms.push("Manufacturer warranty transferred to Buyer.");

        // Initialize termination conditions
        terminationConditions.push(TerminationCondition("Either party may terminate if payment not received by due date.", "Termination Fee: 10% of undelivered goods value."));
    }

    // Function to make payments
    function makePayment(uint256 termIndex) external payable {
        require(termIndex < financialTerms.length, "Invalid financial term index");
        FinancialTerm storage term = financialTerms[termIndex];
        require(!term.paid, "Payment for this term has already been made");
        require(msg.value == term.amount, "Incorrect payment amount");

        term.paid = true; // Mark term as paid
        emit PaymentMade(msg.sender, msg.value, term.purpose);
    }

    // Function for buyer to confirm obligations met
    function confirmObligationMet(uint256 obligationIndex) external onlyBuyer {
        require(obligationIndex < obligations.length, "Invalid obligation index");
        emit ObligationsMet(obligations[obligationIndex].party, obligations[obligationIndex].description);
    }
    
    // Function for termination notice
    function terminateContract(string memory reason) external {
        require(msg.sender == seller.wallet || msg.sender == buyer.wallet, "Not authorized: Only parties can terminate");
        emit ContractTerminated(reason);
        // Implement termination logic here as required
    }

    // Additional getter functions can be added for viewing contract details if needed
}