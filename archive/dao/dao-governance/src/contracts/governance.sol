// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Governance {
    struct Proposal {
        uint id;
        string description;
        uint voteCount;
        mapping(address => bool) voters;
        bool executed;
    }

    mapping(uint => Proposal) public proposals;
    uint public proposalCount;

    event ProposalCreated(uint id, string description);
    event Voted(uint proposalId, address voter);
    event ProposalExecuted(uint proposalId);

    function createProposal(string memory _description) public {
        proposalCount++;
        proposals[proposalCount] = Proposal(proposalCount, _description, 0, false);
        emit ProposalCreated(proposalCount, _description);
    }

    function vote(uint _proposalId) public {
        Proposal storage proposal = proposals[_proposalId];
        require(!proposal.voters[msg.sender], "You have already voted.");
        require(!proposal.executed, "Proposal has already been executed.");

        proposal.voters[msg.sender] = true;
        proposal.voteCount++;
        emit Voted(_proposalId, msg.sender);
    }

    function executeProposal(uint _proposalId) public {
        Proposal storage proposal = proposals[_proposalId];
        require(proposal.voteCount > 0, "No votes for this proposal.");
        require(!proposal.executed, "Proposal has already been executed.");

        proposal.executed = true;
        emit ProposalExecuted(_proposalId);
        // Logic for executing the proposal goes here
    }
}