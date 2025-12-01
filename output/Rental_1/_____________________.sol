// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleRentalAgreement {
    address public tenant;
    address public landlord;

    uint256 public paymentDueDate;
    uint256 public rentalStart;
    uint256 public rentalEnd;

    mapping(address => bool) public obligationsMet;

    event PaymentMade(address indexed payer, uint256 amount, uint256 date);
    event ObligationFulfilled(address indexed party, string obligation);
    event RentalTerminated(address indexed party, string reason);

    modifier onlyTenant() {
        require(msg.sender == tenant, "Not authorized: Only tenant can call this.");
        _;
    }

    modifier onlyLandlord() {
        require(msg.sender == landlord, "Not authorized: Only landlord can call this.");
        _;
    }

    modifier rentalActive() {
        require(block.timestamp >= rentalStart && block.timestamp < rentalEnd, "Rental is not active.");
        _;
    }

    constructor(
        address _tenant,
        address _landlord,
        uint256 _rentalStart,
        uint256 _rentalEnd,
        uint256 _paymentDueDate
    ) {
        require(_tenant != address(0), "Invalid tenant address");
        require(_landlord != address(0), "Invalid landlord address");
        require(_rentalStart < _rentalEnd, "Rental start date must be before end date");

        tenant = _tenant;
        landlord = _landlord;
        rentalStart = _rentalStart;
        rentalEnd = _rentalEnd;
        paymentDueDate = _paymentDueDate;
    }

    function payRent() external payable onlyTenant rentalActive {
        require(msg.value > 0, "Payment must be greater than zero");
        emit PaymentMade(msg.sender, msg.value, block.timestamp);
        // Additional payment handling logic (e.g., updating balance or escrow) can be added here.
    }

    function fulfillObligation(string calldata obligation) external {
        require(msg.sender == tenant || msg.sender == landlord, "Only tenant or landlord can fulfill obligations");
        obligationsMet[msg.sender] = true;
        emit ObligationFulfilled(msg.sender, obligation);
    }

    function terminateRental(string calldata reason) external {
        require(msg.sender == tenant || msg.sender == landlord, "Only tenant or landlord can terminate rental");
        rentalEnd = block.timestamp; // Set rental end to now
        emit RentalTerminated(msg.sender, reason);
    }

    function isObligationMet(address party) external view returns (bool) {
        return obligationsMet[party];
    }
}