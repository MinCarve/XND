import TonWeb from "tonweb";

const tonweb = new TonWeb(); // Use TonWeb to connect to TON
const contractAddress = "YOUR_CONTRACT_ADDRESS";
const walletAddress = "YOUR_WALLET_ADDRESS";

const playButton = document.getElementById("play-btn");
const pickWinnerButton = document.getElementById("pick-winner-btn");
const status = document.getElementById("status");

playButton.addEventListener("click", async () => {
    try {
        status.innerText = "Sending TON to participate...";
        
        const tx = await tonweb.sendTransaction({
            to: contractAddress,
            value: TonWeb.utils.toNano(1), // 1 TON entry fee
            from: walletAddress,
        });

        status.innerText = "Transaction sent! Waiting for confirmation...";
        await tx.wait();
        status.innerText = "You are now in the game!";
    } catch (err) {
        console.error(err);
        status.innerText = "Error: " + err.message;
    }
});

pickWinnerButton.addEventListener("click", async () => {
    try {
        status.innerText = "Picking a winner...";
        const tx = await tonweb.runMethod({
            method: "pick_winner",
            from: walletAddress,
        });
        status.innerText = "Winner selected!";
    } catch (err) {
        console.error(err);
        status.innerText = "Error: " + err.message;
    }
});