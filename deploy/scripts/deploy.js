const { ethers, Wallet, JsonRpcProvider } = require("ethers");
require("dotenv").config();

async function main() {
  console.log("========================================");
  console.log("  AgeVerificationContract Deployment");
  console.log("========================================");
  console.log("");

  // Get RPC URL
  const rpcUrl = process.env.SEPOLIA_RPC_URL;
  if (!rpcUrl) {
    console.error("Error: SEPOLIA_RPC_URL not set");
    console.error("Please set it in .env file or as environment variable");
    console.error("Example: SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY");
    process.exit(1);
  }

  // Get private key
  const privateKey = process.env.PRIVATE_KEY;
  if (!privateKey) {
    console.error("Error: PRIVATE_KEY not set");
    console.error("Please set it in .env file or as environment variable");
    console.error("Example: PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE");
    process.exit(1);
  }

  // Create provider and wallet
  const provider = new JsonRpcProvider(rpcUrl);
  const wallet = new Wallet(privateKey, provider);
  
  console.log("Deploying with account:", wallet.address);

  // Check balance
  const balance = await provider.getBalance(wallet.address);
  console.log("Account balance:", ethers.formatEther(balance), "ETH");
  console.log("");

  // Read compiled contract ABI
  const artifact = require("../artifacts/contracts/AgeVerificationContract.sol/AgeVerificationContract.json");
  const bytecode = artifact.bytecode;
  const abi = artifact.abi;

  // Initial government public key (dummy value for testing)
  // In production, replace with actual government public key
  const initialPublicKey = "0x" + "00".repeat(64);

  console.log("Contract constructor argument:");
  console.log("  governmentPublicKey:", initialPublicKey);
  console.log("");

  // Deploy the contract
  console.log("Deploying AgeVerificationContract...");
  const factory = new ethers.ContractFactory(abi, bytecode, wallet);
  const contract = await factory.deploy(initialPublicKey);
  
  console.log("Waiting for deployment transaction...");
  await contract.deploymentTransaction().wait();

  const contractAddress = contract.target;
  console.log("");
  console.log("========================================");
  console.log("  Deployment Successful!");
  console.log("========================================");
  console.log("");
  console.log("Contract Address:", contractAddress);
  console.log("");
  console.log("Admin Address:", wallet.address);
  console.log("");
  console.log("Next steps:");
  console.log("1. Verify on Etherscan:");
  console.log(`   npx hardhat verify --network sepolia ${contractAddress} "${initialPublicKey}"`);
  console.log("");
  console.log("2. View on Sepolia Etherscan:");
  console.log(`   https://sepolia.etherscan.io/address/${contractAddress}`);
  console.log("");
  console.log("3. Call contract functions:");
  console.log(`   Provider: ${rpcUrl}`);
  console.log("");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Error:", error);
    process.exit(1);
  });
