// filepath: /dao-governance/dao-governance/src/core/autonomousDAO.ts
import { ResourceManager } from './resourceManager';
import { ProposalHandler } from './proposalHandler';
import { VotingSystem } from './votingSystem';

class AutonomousDAO {
    private resourceManager: ResourceManager;
    private proposalHandler: ProposalHandler;
    private votingSystem: VotingSystem;

    constructor() {
        this.resourceManager = new ResourceManager();
        this.proposalHandler = new ProposalHandler();
        this.votingSystem = new VotingSystem();
    }

    public initialize() {
        // Initialize the DAO components
        this.resourceManager.initialize();
        this.proposalHandler.initialize();
        this.votingSystem.initialize();
    }

    public run() {
        // Start the DAO operations
        this.initialize();
        console.log("Autonomous DAO is running...");
    }
}

const dao = new AutonomousDAO();
dao.run();