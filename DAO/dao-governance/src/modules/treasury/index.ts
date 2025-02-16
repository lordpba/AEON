// filepath: /dao-governance/dao-governance/src/modules/treasury/index.ts

class Treasury {
    private funds: number;

    constructor() {
        this.funds = 0;
    }

    public allocateFunds(amount: number): boolean {
        if (amount <= this.funds) {
            this.funds -= amount;
            console.log(`Allocated ${amount} funds.`);
            return true;
        }
        console.log(`Insufficient funds to allocate ${amount}.`);
        return false;
    }

    public addFunds(amount: number): void {
        this.funds += amount;
        console.log(`Added ${amount} funds.`);
    }

    public getFunds(): number {
        return this.funds;
    }

    public report(): string {
        return `Current treasury funds: ${this.funds}`;
    }
}

export default Treasury;