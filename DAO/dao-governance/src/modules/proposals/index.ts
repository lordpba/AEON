// filepath: /dao-governance/dao-governance/src/modules/proposals/index.ts

import { Proposal } from '../../types';
import { ProposalStatus } from '../../utils/constants';

class ProposalManager {
    private proposals: Proposal[] = [];

    public submitProposal(proposal: Proposal): void {
        proposal.status = ProposalStatus.Pending;
        this.proposals.push(proposal);
    }

    public getProposals(): Proposal[] {
        return this.proposals;
    }

    public updateProposalStatus(id: number, status: ProposalStatus): void {
        const proposal = this.proposals.find(p => p.id === id);
        if (proposal) {
            proposal.status = status;
        }
    }

    public getProposalById(id: number): Proposal | undefined {
        return this.proposals.find(p => p.id === id);
    }
}

export const proposalManager = new ProposalManager();