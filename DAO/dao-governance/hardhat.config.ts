import { task } from "hardhat/config";
import "@nomiclabs/hardhat-waffle";

const ALCHEMY_API_KEY = "your-alchemy-api-key";
const ROPSTEN_PRIVATE_KEY = "your-ropsten-private-key";

task("accounts", "Prints the list of accounts", async (taskArgs, hre) => {
  const accounts = await hre.ethers.getSigners();
  for (const account of accounts) {
    console.log(account.address);
  }
});

export default {
  solidity: "0.8.4",
  networks: {
    ropsten: {
      url: `https://eth-ropsten.alchemyapi.io/v2/${ALCHEMY_API_KEY}`,
      accounts: [`0x${ROPSTEN_PRIVATE_KEY}`],
    },
  },
};