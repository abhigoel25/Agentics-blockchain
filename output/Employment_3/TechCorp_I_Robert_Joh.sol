// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EmploymentAgreement {
    enum Role { Employer, Employee }
    
    struct Party {
        string name;
        Role role;
        string address;  // In future implementations, consider using address type for blockchain addresses
    }
    
    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
    }
    
    struct Obligation {
        string party;
        string description;
    }
    
    struct TerminationCondition {
        string condition;
    }
    
    struct AgreementDates {
        string commencement;
        string termination;
    }

    Party public employer;
    Party public employee;
    FinancialTerm[] public financialTerms;
    Obligation[] public obligations;
    TerminationCondition[] public terminationConditions;
    AgreementDates public dates;

    address public owner;
    
    event PaymentMade(address indexed _to, uint256 _amount, string _currency);
    event ObligationFulfilled(string _party, string _description);
    event AgreementTerminated(string _reason);

    constructor() {
        owner = msg.sender;
        
        employer = Party({
            name: "TechCorp Industries, Inc.",
            role: Role.Employer,
            address: ""
        });

        employee = Party({
            name: "Robert Johnson",
            role: Role.Employee,
            address: "456 Oak Avenue, San Francisco, CA 94102"
        });

        financialTerms.push(FinancialTerm(150000 * 1e18, "USD", "salary", "monthly"));
        financialTerms.push(FinancialTerm(25000 * 1e18, "USD", "performance bonus", "annual"));

        obligations.push(Obligation("employee", "serves as Senior Software Engineer, develops enterprise-level applications, mentors junior developers, makes architectural decisions"));
        obligations.push(Obligation("employer", "provides salary, bonuses, health insurance and retirement benefits"));

        terminationConditions.push(TerminationCondition("Either party may terminate with 30 days written notice."));
        terminationConditions.push(TerminationCondition("Severance: 3 months base salary upon termination without cause."));
        terminationConditions.push(TerminationCondition("Termination for cause includes breach of confidentiality, gross negligence, or policy violation."));

        dates = AgreementDates({
            commencement: "February 1, 2025",
            termination: "January 31, 2028"
        });
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }

    function makePayment(uint256 _amount, string memory _currency) public onlyOwner {
        // Here you would implement the actual payment logic
        emit PaymentMade(employee.address, _amount, _currency);
    }

    function fulfillObligation(string memory _party, string memory _description) public onlyOwner {
        emit ObligationFulfilled(_party, _description);
    }

    function terminateAgreement(string memory _reason) public onlyOwner {
        emit AgreementTerminated(_reason);
    }

    function getObligations() public view returns (Obligation[] memory) {
        return obligations;
    }

    function getFinancialTerms() public view returns (FinancialTerm[] memory) {
        return financialTerms;
    }
}