document.addEventListener('DOMContentLoaded', () => {
    // Elementos DOM
    const numberBoard = document.getElementById('number-board');
    const scoreDisplay = document.getElementById('score');
    const highScoreDisplay = document.getElementById('high-score');
    const gameMessage = document.getElementById('game-message');
    const numberInput = document.getElementById('number-input');
    const submitBtn = document.getElementById('submit-btn');
    const newGameBtn = document.getElementById('new-game-btn');
    const resetBtn = document.getElementById('reset-btn');

    // Variáveis do jogo
    let score = 0;
    let highScore = localStorage.getItem('highScore') || 0;
    let currentNumber = 0;
    let gameActive = false;

    // Inicializa o jogo
    function initGame() {
        createNumberBoard();
        highScoreDisplay.textContent = highScore;
        gameActive = true;
        startNewRound();
    }

    // Cria o tabuleiro de números
    function createNumberBoard() {
        numberBoard.innerHTML = '';
        for (let i = 1; i <= 25; i++) {
            const cell = document.createElement('div');
            cell.className = 'number-cell';
            cell.textContent = i;
            cell.dataset.number = i;
            cell.addEventListener('click', () => selectNumber(i));
            numberBoard.appendChild(cell);
        }
    }

    // Inicia uma nova rodada
    function startNewRound() {
        currentNumber = Math.floor(Math.random() * 25) + 1;
        gameMessage.textContent = `Encontre o número: ${currentNumber}`;
        gameMessage.style.color = var(--primary);
        numberInput.value = '';
        numberInput.focus();
    }

    // Seleciona um número do tabuleiro
    function selectNumber(number) {
        if (!gameActive) return;

        if (number === currentNumber) {
            handleCorrectGuess();
        } else {
            handleWrongGuess(number);
        }
    }

    // Lida com chute correto
    function handleCorrectGuess() {
        score++;
        scoreDisplay.textContent = score;

        if (score > highScore) {
            highScore = score;
            highScoreDisplay.textContent = highScore;
            localStorage.setItem('highScore', highScore);
        }

        gameMessage.textContent = "Correto! Próximo número:";
        gameMessage.style.color = var(--success);

        setTimeout(startNewRound, 1500);
    }

    // Lida com chute errado
    function handleWrongGuess(number) {
        const cell = document.querySelector(`.number-cell[data-number="${number}"]`);
        cell.style.backgroundColor = var(--danger);
        cell.style.color = white;

        setTimeout(() => {
            cell.style.backgroundColor = '';
            cell.style.color = '';
        }, 1000);

        gameMessage.textContent = `Errou! Era o número ${currentNumber}. Tente novamente!`;
        gameMessage.style.color = var(--danger);

        setTimeout(startNewRound, 2000);
    }

    // Verifica o número digitado
    function checkNumber() {
        if (!gameActive) return;

        const inputNumber = parseInt(numberInput.value);

        if (isNaN(inputNumber) || inputNumber < 1 || inputNumber > 25) {
            gameMessage.textContent = "Por favor, digite um número entre 1 e 25";
            gameMessage.style.color = var(--danger);
            return;
        }

        if (inputNumber === currentNumber) {
            handleCorrectGuess();
        } else {
            handleWrongGuess(inputNumber);
        }
    }

    // Event Listeners
    submitBtn.addEventListener('click', checkNumber);

    numberInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') checkNumber();
    });

    newGameBtn.addEventListener('click', initGame);

    resetBtn.addEventListener('click', () => {
        score = 0;
        scoreDisplay.textContent = score;
        gameActive = false;
        gameMessage.textContent = "Jogo resetado!";
        setTimeout(initGame, 1500);
    });

    // Inicia o jogo
    initGame();
});
