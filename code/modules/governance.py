"""Municipal Governance Module
Manages democratic decision-making, proposals, voting, and policy implementation
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import random
import threading
from loguru import logger

@dataclass
class Proposal:
    id: str
    title: str
    description: str
    proposer: str
    created: datetime
    votes_for: int = 0
    votes_against: int = 0
    status: str = "active"  # active, approved, rejected, expired
    
    @property
    def total_votes(self) -> int:
        return self.votes_for + self.votes_against
    
    @property
    def approval_rate(self) -> float:
        if self.total_votes == 0:
            return 0.0
        return (self.votes_for / self.total_votes) * 100

class MunicipalGovernance:
    def __init__(self, voting_threshold: int = 100, quorum_percentage: float = 20.0):
        self.lock = threading.Lock()
        self.proposals: Dict[str, Proposal] = {}
        self.active_policies: Dict[str, str] = {}
        self.voting_history: List[Dict[str, Any]] = []
        self.voting_threshold = voting_threshold
        self.quorum_percentage = quorum_percentage
        self.proposal_counter = 0

    def run(self):
        """Continuously manage governance processes."""
        while True:
            self.process_proposals()
            self.update_policies()
            self.generate_random_proposal()  # Simulate citizen proposals

    def create_proposal(self, title: str, description: str, proposer: str = "Citizen") -> str:
        """Create a new governance proposal."""
        with self.lock:
            self.proposal_counter += 1
            proposal_id = f"PROP-{self.proposal_counter:04d}"
            
            proposal = Proposal(
                id=proposal_id,
                title=title,
                description=description,
                proposer=proposer,
                created=datetime.now()
            )
            
            self.proposals[proposal_id] = proposal
            logger.info(f"New proposal created: {proposal_id} - {title}")
            return proposal_id
    
    def vote(self, proposal_id: str, vote_for: bool, votes: int = 1):
        """Cast votes on a proposal."""
        with self.lock:
            if proposal_id not in self.proposals:
                logger.error(f"Proposal {proposal_id} not found")
                return
            
            proposal = self.proposals[proposal_id]
            if proposal.status != "active":
                logger.warning(f"Cannot vote on {proposal_id} - status: {proposal.status}")
                return
            
            if vote_for:
                proposal.votes_for += votes
            else:
                proposal.votes_against += votes
            
            logger.debug(f"Votes cast on {proposal_id}: {votes} ({'for' if vote_for else 'against'})")

    def process_proposals(self):
        """Process active proposals and determine outcomes."""
        with self.lock:
            for proposal_id, proposal in list(self.proposals.items()):
                if proposal.status != "active":
                    continue
                
                # Check if quorum reached
                if proposal.total_votes >= self.voting_threshold:
                    quorum_met = (proposal.total_votes / self.voting_threshold) * 100 >= self.quorum_percentage
                    
                    if quorum_met:
                        if proposal.approval_rate >= 50:
                            proposal.status = "approved"
                            self.implement_policy(proposal)
                            logger.info(f"Proposal {proposal_id} APPROVED ({proposal.approval_rate:.1f}% approval)")
                        else:
                            proposal.status = "rejected"
                            logger.info(f"Proposal {proposal_id} REJECTED ({proposal.approval_rate:.1f}% approval)")
                        
                        self.voting_history.append({
                            "proposal_id": proposal_id,
                            "title": proposal.title,
                            "outcome": proposal.status,
                            "votes_for": proposal.votes_for,
                            "votes_against": proposal.votes_against
                        })

    def implement_policy(self, proposal: Proposal):
        """Implement an approved proposal as policy."""
        policy_id = f"POL-{len(self.active_policies) + 1:04d}"
        self.active_policies[policy_id] = proposal.title
        logger.info(f"New policy implemented: {policy_id} - {proposal.title}")
    
    def update_policies(self):
        """Update existing policies based on new data."""
        # Placeholder for future policy evolution logic
        pass

    def generate_random_proposal(self):
        """Simulate citizens creating proposals."""
        if random.random() < 0.1:  # 10% chance each cycle
            topics = [
                ("Increase Park Funding", "Allocate additional budget for park maintenance"),
                ("New Bike Lanes", "Construct protected bike lanes on main streets"),
                ("Extend Library Hours", "Keep library open until 9 PM on weekdays"),
                ("Community Center Renovation", "Modernize community center facilities"),
                ("Traffic Calming Measures", "Install speed bumps in residential areas")
            ]
            title, description = random.choice(topics)
            self.create_proposal(title, description, f"Citizen_{random.randint(1,100)}")
            
            # Simulate some votes
            if self.proposals:
                latest_id = list(self.proposals.keys())[-1]
                for _ in range(random.randint(5, 30)):
                    self.vote(latest_id, random.random() > 0.4)  # 60% approval bias

    def get_governance_status(self) -> Dict[str, Any]:
        """Get current governance status."""
        with self.lock:
            active_proposals = [p for p in self.proposals.values() if p.status == "active"]
            return {
                "active_proposals": len(active_proposals),
                "total_policies": len(self.active_policies),
                "total_votes_cast": sum(p.total_votes for p in self.proposals.values()),
                "recent_proposals": [
                    {
                        "id": p.id,
                        "title": p.title,
                        "votes_for": p.votes_for,
                        "votes_against": p.votes_against,
                        "status": p.status
                    }
                    for p in list(self.proposals.values())[-5:]
                ]
            }