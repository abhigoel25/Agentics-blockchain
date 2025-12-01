// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EmploymentAgreement {
    address public employer;
    address public employee;

    enum PaymentFrequency { Monthly, Annually }
    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        PaymentFrequency frequency;
    }

    struct Obligation {
        string party;
        string description;
    }

    struct TerminationCondition {
        string description;
    }

    FinancialTerm[] public financialTerms;
    Obligation[] public obligations;
    TerminationCondition[] public terminationConditions;

    event AgreementCreated(address indexed employer, address indexed employee);
    event FinancialTermAdded(uint256 indexed index, uint256 amount, string purpose);
    event ObligationAdded(uint256 indexed index, string party);
    event TerminationConditionAdded(uint256 indexed index);

    modifier onlyEmployer() {
        require(msg.sender == employer, "Only employer can perform this action");
        _;
    }

    modifier onlyEmployee() {
        require(msg.sender == employee, "Only employee can perform this action");
        _;
    }

    constructor(address _employee) {
        employer = msg.sender;
        employee = _employee;

        emit AgreementCreated(employer, employee);

        // Adding financial terms
        addFinancialTerm(150000 * 1 ether, "USD", "salary", PaymentFrequency.Monthly);
        addFinancialTerm(25000 * 1 ether, "USD", "performance bonus", PaymentFrequency.Annually);
        addFinancialTerm(5000 * 1 ether, "options", "stock options", PaymentFrequency.Monthly);

        // Adding obligations
        addObligation("Employee", "Serve as Senior Software Engineer, report to Chief Technology Officer, develop enterprise-level applications, mentor junior developers, and make architectural decisions.");
        addObligation("Employer", "Provide full health insurance coverage and 401(k) with 5% employer match.");

        // Adding termination conditions
        addTerminationCondition("Either party may terminate with 30 days written notice.");
        addTerminationCondition("3 months base salary upon termination without cause.");
        addTerminationCondition("Cause includes breach of confidentiality, gross negligence, or policy violation.");
    }

    function addFinancialTerm(uint256 _amount, string memory _currency, string memory _purpose, PaymentFrequency _frequency) internal {
        financialTerms.push(FinancialTerm(_amount, _currency, _purpose, _frequency));
        emit FinancialTermAdded(financialTerms.length - 1, _amount, _purpose);
    }

    function addObligation(string memory _party, string memory _description) internal {
        obligations.push(Obligation(_party, _description));
        emit ObligationAdded(obligations.length - 1, _party);
    }

    function addTerminationCondition(string memory _description) internal {
        terminationConditions.push(TerminationCondition(_description));
        emit TerminationConditionAdded(terminationConditions.length - 1);
    }

    function getFinancialTerms() external view returns (FinancialTerm[] memory) {
        return financialTerms;
    }

    function getObligations() external view returns (Obligation[] memory) {
        return obligations;
    }

    function getTerminationConditions() external view returns (TerminationCondition[] memory) {
        return terminationConditions;
    }
}