// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EmploymentContract {
    address public employer;
    address public employee;

    // Financial terms
    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
        string dueDate;
    }
    
    FinancialTerm[] public financialTerms;

    // Dates
    struct ContractDates {
        string dateType;
        string value;
    }
    
    ContractDates[] public dates;

    // Obligations
    struct Obligation {
        string party;
        string description;
    }
    
    Obligation[] public obligations;

    // Special terms and termination conditions
    string[] public specialTerms;
    string[] public terminationConditions;

    // Events
    event EmploymentTermAdded(string indexed purpose, uint256 amount, string currency);
    event ObligationAdded(string indexed party, string description);
    event SpecialTermAdded(string term);
    event TerminationConditionAdded(string condition);

    // Modifiers for access control
    modifier onlyEmployer() {
        require(msg.sender == employer, "Only employer can call this function.");
        _;
    }

    modifier onlyEmployee() {
        require(msg.sender == employee, "Only employee can call this function.");
        _;
    }

    constructor(address _employee) {
        employer = msg.sender; // The deployer of the contract is the employer
        employee = _employee;
        
        // Adding financial terms
        financialTerms.push(FinancialTerm(150000 * 10**18, "USD", "salary", "annual", "monthly"));
        financialTerms.push(FinancialTerm(25000 * 10**18, "USD", "performance bonus", "annual", ""));
        financialTerms.push(FinancialTerm(5000 * 10**18, "options", "stock options", "vesting over 4 years", ""));
        
        // Contract dates
        dates.push(ContractDates("start", "February 1, 2025"));
        dates.push(ContractDates("end", "February 1, 2028"));
        dates.push(ContractDates("contract_date", "January 15, 2025"));
        
        // Obligations
        obligations.push(Obligation("Employee", "Develop enterprise-level applications, mentor junior developers, and make architectural decisions."));
        obligations.push(Obligation("Employee", "Maintain confidentiality of all proprietary information."));
        
        // Special terms
        specialTerms.push("Health Insurance: Full coverage for employee and family");
        specialTerms.push("Retirement: 401(k) with 5% employer match");
        specialTerms.push("Paid Time Off: 20 vacation days, 10 sick days, 6 company holidays annually");
        specialTerms.push("Non-Compete Period: 12 months post-employment within 100-mile radius of headquarters");
        
        // Termination conditions
        terminationConditions.push("Either party may terminate with 30 days written notice");
        terminationConditions.push("Severance: 3 months base salary upon termination without cause");
        terminationConditions.push("Cause includes breach of confidentiality, gross negligence, or policy violation");
    }

    // Functions for adding new financial terms, obligations, or special terms
    function addFinancialTerm(uint256 _amount, string memory _currency, string memory _purpose, string memory _frequency, string memory _dueDate) public onlyEmployer {
        financialTerms.push(FinancialTerm(_amount, _currency, _purpose, _frequency, _dueDate));
        emit EmploymentTermAdded(_purpose, _amount, _currency);
    }

    function addObligation(string memory _party, string memory _description) public {
        require(
            msg.sender == employer || msg.sender == employee,
            "Only employer or employee can add obligations."
        );
        obligations.push(Obligation(_party, _description));
        emit ObligationAdded(_party, _description);
    }

    function addSpecialTerm(string memory _term) public onlyEmployer {
        specialTerms.push(_term);
        emit SpecialTermAdded(_term);
    }

    function addTerminationCondition(string memory _condition) public onlyEmployer {
        terminationConditions.push(_condition);
        emit TerminationConditionAdded(_condition);
    }

    // Function to retrieve contract details
    function getContractDetails() public view returns (
        address _employer,
        address _employee,
        FinancialTerm[] memory _financialTerms,
        ContractDates[] memory _dates,
        Obligation[] memory _obligations,
        string[] memory _specialTerms,
        string[] memory _terminationConditions
    ) {
        _employer = employer;
        _employee = employee;
        _financialTerms = financialTerms;
        _dates = dates;
        _obligations = obligations;
        _specialTerms = specialTerms;
        _terminationConditions = terminationConditions;
    }
}