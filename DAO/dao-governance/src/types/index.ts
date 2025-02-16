// src/types/index.ts

export interface Proposal {
    id: string;
    title: string;
    description: string;
    creator: string;
    votesFor: number;
    votesAgainst: number;
    status: ProposalStatus;
    createdAt: Date;
    votingEnd: Date;
}

export enum ProposalStatus {
    Pending = "Pending",
    Active = "Active",
    Executed = "Executed",
    Rejected = "Rejected"
}

export interface Member {
    address: string;
    role: MemberRole;
    joinedAt: Date;
}

export enum MemberRole {
    Admin = "Admin",
    Member = "Member",
    Guest = "Guest"
}

export interface Vote {
    proposalId: string;
    voter: string;
    choice: VoteChoice;
}

export enum VoteChoice {
    For = "For",
    Against = "Against"
}

export interface Treasury {
    totalFunds: number;
    allocatedFunds: number;
    availableFunds: number;
}