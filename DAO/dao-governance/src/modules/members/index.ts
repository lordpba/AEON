// filepath: /dao-governance/dao-governance/src/modules/members/index.ts

import { Member } from '../../types';

class MemberManagement {
    private members: Member[] = [];

    addMember(member: Member): void {
        this.members.push(member);
    }

    removeMember(memberId: string): void {
        this.members = this.members.filter(member => member.id !== memberId);
    }

    getMembers(): Member[] {
        return this.members;
    }

    verifyMembership(memberId: string): boolean {
        return this.members.some(member => member.id === memberId);
    }

    assignRole(memberId: string, role: string): void {
        const member = this.members.find(member => member.id === memberId);
        if (member) {
            member.role = role;
        }
    }
}

export const memberManagement = new MemberManagement();