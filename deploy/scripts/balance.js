const { Wallet, JsonRpcProvider } = require("ethers");
require("dotenv").config();

async function main() {
  const rpcUrl = process.env.SEPOLIA_RPC_URL || "https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY";
  const privateKey = process.env.PRIVATE_KEY;
  
  if (!privateKey) {
    console.error("Error: PRIVATE_KEY not set");
    process.exit(1);
  }

  const provider = new JsonRpcProvider(rpcUrl);
  const wallet = new Wallet(privateKey, provider);
  
  console.log("Account:", wallet.address);

  const balance = await provider.getBalance(wallet.address);
  console.log("Balance:", ethers.formatEther(balance), "ETH");

  console.log("");
  console.log("Sepolia Faucets:");
  console.log("- https://sepoliafaucet.com/");
  console.log("- https://www.alchemy.com/faucets/ethereum-sepolia");
  console.log("- https://cloud.google.com/application/web3/faucet/ethereum/sepolia");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
