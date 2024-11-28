const spinner = document.getElementById('spinner');
        const resultDisplay = document.getElementById('result');
        const betAmountInput = document.getElementById('bet-amount');

        // Predefined colors for numbers 1 to 30
        const colors = {
            1: 'red', 2: 'black', 3: 'red', 4: 'black', 5: 'red',
            6: 'black', 7: 'red', 8: 'black', 9: 'red', 10: 'black',
            11: 'red', 12: 'black', 13: 'red', 14: 'black', 15: 'red',
            16: 'black', 17: 'red', 18: 'black', 19: 'red', 20: 'black',
            21: 'red', 22: 'black', 23: 'red', 24: 'black', 25: 'red',
            26: 'black', 27: 'red', 28: 'black', 29: 'red', 30: 'black',
        };

        // Function to simulate the game
        function placeBet(selectedColor) {
            const betAmount = parseFloat(betAmountInput.value);

            if (!betAmount || betAmount <= 0) {
                alert("Please enter a valid bet amount!");
                return;
            }

            resultDisplay.textContent = ""; // Clear previous result
            let currentNumber = 1;
            const totalNumbers = 30;

            const spinInterval = setInterval(() => {
                currentNumber = Math.floor(Math.random() * totalNumbers) + 1;
                spinner.textContent = currentNumber;
                spinner.style.color = colors[currentNumber]; // Update spinner color
            }, 100);

            setTimeout(() => {
                clearInterval(spinInterval);
                const finalNumber = Math.floor(Math.random() * totalNumbers) + 1;
                const finalColor = colors[finalNumber];

                spinner.textContent = finalNumber;
                spinner.style.color = finalColor;

                if (selectedColor === finalColor) {
                    resultDisplay.textContent = `You win ${betAmount * 2} credits!`;
                    resultDisplay.style.color = 'green';
                } else {
                    resultDisplay.textContent = `You lost ${betAmount} credits.`;
                    resultDisplay.style.color = 'red';
                }
            }, 3000);
        }