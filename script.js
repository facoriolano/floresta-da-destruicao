// Estado do Jogo
const gameState = {
    currentSection: 1,
    character: {
        skill: 0,
        stamina: 0,
        maxStamina: 0,
        luck: 0,
        maxLuck: 0,
        inventory: []
    },
    story: {},
    inCombat: false,
    currentEnemy: null,
    combatLog: []
};

// Elementos do DOM
const titleScreen = document.getElementById('title-screen');
const characterScreen = document.getElementById('character-screen');
const gameScreen = document.getElementById('game-screen');
const startButton = document.getElementById('start-button');
const rollStatsButton = document.getElementById('roll-stats-button');
const confirmCharacterButton = document.getElementById('confirm-character-button');
const skillValue = document.getElementById('skill-value');
const staminaValue = document.getElementById('stamina-value');
const luckValue = document.getElementById('luck-value');
const storyText = document.getElementById('story-text');
const storyImage = document.getElementById('story-image');
const choicesContainer = document.getElementById('choices-container');
const combatContainer = document.getElementById('combat-container');
const luckTestContainer = document.getElementById('luck-test-container');
const gameSkill = document.getElementById('game-skill');
const gameStamina = document.getElementById('game-stamina');
const gameLuck = document.getElementById('game-luck');
const sectionNumber = document.getElementById('section-number');
const attackButton = document.getElementById('attack-button');
const luckTestButton = document.getElementById('luck-test-button');
const rollLuckButton = document.getElementById('roll-luck-button');
const combatLog = document.getElementById('combat-log');
const restartButton = document.getElementById('restart-button');

// Funções Auxiliares
function rollDice(sides = 6) {
    return Math.floor(Math.random() * sides) + 1;
}

function roll2d6() {
    return rollDice(6) + rollDice(6);
}

function showScreen(screen) {
    titleScreen.classList.remove('active');
    characterScreen.classList.remove('active');
    gameScreen.classList.remove('active');
    screen.classList.add('active');
}

// Carregar a história
async function loadStory() {
    try {
        const response = await fetch('data/story.json');
        gameState.story = await response.json();
    } catch (error) {
        console.error('Erro ao carregar a história:', error);
        // Fallback para uma história simples se o arquivo não carregar
        gameState.story = {
            "1": {
                "text": "Bem-vindo à Floresta da Sombra Negra!",
                "image": "forest_entrance.png",
                "choices": [
                    {"text": "Continuar", "goto": 15}
                ],
                "event": null
            },
            "15": {
                "text": "Fim de Jogo",
                "image": "gargoyle_eye.png",
                "choices": [
                    {"text": "Jogar novamente", "goto": "restart"}
                ],
                "event": {"type": "end", "ending": "victory"}
            }
        };
    }
}

// Criar Personagem
function rollStats() {
    const skill = rollDice(6) + rollDice(6) + 6;
    const stamina = rollDice(6) + rollDice(6) + 6;
    const luck = rollDice(6) + rollDice(6) + 6;

    skillValue.textContent = skill;
    staminaValue.textContent = stamina;
    luckValue.textContent = luck;

    gameState.character.skill = skill;
    gameState.character.stamina = stamina;
    gameState.character.maxStamina = stamina;
    gameState.character.luck = luck;
    gameState.character.maxLuck = luck;

    confirmCharacterButton.disabled = false;
}

function confirmCharacter() {
    updateGameStats();
    gameState.currentSection = 1;
    showScreen(gameScreen);
    displaySection(1);
}

// Atualizar Estatísticas na Tela
function updateGameStats() {
    gameSkill.textContent = gameState.character.skill;
    gameStamina.textContent = gameState.character.stamina;
    gameLuck.textContent = gameState.character.luck;
}

// Exibir Seção da História
function displaySection(sectionId) {
    const section = gameState.story[sectionId];
    if (!section) {
        console.error('Seção não encontrada:', sectionId);
        return;
    }

    gameState.currentSection = sectionId;
    sectionNumber.textContent = `Seção ${sectionId}`;
    storyText.textContent = section.text;

    // Exibir imagem
    if (section.image) {
        storyImage.src = `assets/images/${section.image}`;
        storyImage.style.display = 'block';
    } else {
        storyImage.style.display = 'none';
    }

    // Limpar containers
    choicesContainer.innerHTML = '';
    combatContainer.style.display = 'none';
    luckTestContainer.style.display = 'none';
    restartButton.style.display = 'none';

    // Processar eventos
    if (section.event) {
        handleEvent(section.event);
    } else {
        // Exibir opções de escolha
        displayChoices(section.choices);
    }

    updateGameStats();
}

// Exibir Opções de Escolha
function displayChoices(choices) {
    choicesContainer.innerHTML = '';
    choices.forEach((choice, index) => {
        const button = document.createElement('button');
        button.className = 'choice-button';
        button.textContent = choice.text;
        button.addEventListener('click', () => {
            if (choice.goto === 'restart') {
                restartGame();
            } else {
                displaySection(choice.goto);
            }
        });
        choicesContainer.appendChild(button);
    });
}

// Processar Eventos
function handleEvent(event) {
    if (event.type === 'combat') {
        startCombat(event.enemy);
    } else if (event.type === 'luck_test') {
        startLuckTest(event);
    } else if (event.type === 'skill_test') {
        startSkillTest(event);
    } else if (event.type === 'item') {
        applyItemEffect(event);
    } else if (event.type === 'damage') {
        takeDamage(event.damage);
    } else if (event.type === 'end') {
        displayEndGame(event.ending);
    }
}

// COMBATE
function startCombat(enemy) {
    gameState.inCombat = true;
    gameState.currentEnemy = {
        name: enemy.name,
        skill: enemy.skill,
        stamina: enemy.stamina,
        maxStamina: enemy.stamina
    };

    combatLog.innerHTML = '';
    updateCombatDisplay();
    combatContainer.style.display = 'block';
    choicesContainer.innerHTML = '';
}

function updateCombatDisplay() {
    document.getElementById('enemy-name').textContent = gameState.currentEnemy.name;
    document.getElementById('player-combat-skill').textContent = gameState.character.skill;
    document.getElementById('player-combat-stamina').textContent = gameState.character.stamina;
    document.getElementById('enemy-combat-skill').textContent = gameState.currentEnemy.skill;
    document.getElementById('enemy-combat-stamina').textContent = gameState.currentEnemy.stamina;
}

function performAttack() {
    const playerRoll = roll2d6();
    const playerAttack = playerRoll + gameState.character.skill;

    const enemyRoll = roll2d6();
    const enemyAttack = enemyRoll + gameState.currentEnemy.skill;

    let logEntry = `<p>Você rolou: ${playerRoll} + ${gameState.character.skill} = ${playerAttack}</p>`;
    logEntry += `<p>${gameState.currentEnemy.name} rolou: ${enemyRoll} + ${gameState.currentEnemy.skill} = ${enemyAttack}</p>`;

    if (playerAttack > enemyAttack) {
        gameState.currentEnemy.stamina -= 2;
        logEntry += `<p style="color: #00ff00;">Você acertou! ${gameState.currentEnemy.name} perde 2 de Energia!</p>`;
    } else if (enemyAttack > playerAttack) {
        gameState.character.stamina -= 2;
        logEntry += `<p style="color: #ff0000;">${gameState.currentEnemy.name} acertou! Você perde 2 de Energia!</p>`;
    } else {
        logEntry += `<p>Empate! Nada acontece.</p>`;
    }

    combatLog.innerHTML += logEntry;
    combatLog.scrollTop = combatLog.scrollHeight;
    updateCombatDisplay();

    // Verificar fim do combate
    if (gameState.currentEnemy.stamina <= 0) {
        endCombat(true);
    } else if (gameState.character.stamina <= 0) {
        endCombat(false);
    }
}

function endCombat(playerWon) {
    gameState.inCombat = false;
    attackButton.disabled = true;
    luckTestButton.disabled = true;

    if (playerWon) {
        combatLog.innerHTML += `<p style="color: #00ff00; font-weight: bold;">Você venceu!</p>`;
        const nextSection = gameState.currentSection + 1;
        setTimeout(() => {
            displaySection(nextSection);
        }, 2000);
    } else {
        combatLog.innerHTML += `<p style="color: #ff0000; font-weight: bold;">Você foi derrotado!</p>`;
        setTimeout(() => {
            restartGame();
        }, 2000);
    }
}

// TESTE DE SORTE
function startLuckTest(event) {
    luckTestContainer.style.display = 'block';
    document.getElementById('luck-test-text').textContent = event.text;
    rollLuckButton.onclick = () => performLuckTest(event);
}

function performLuckTest(event) {
    const roll = roll2d6();
    const currentLuck = gameState.character.luck;

    let result = `<p>Você rolou: ${roll}</p>`;
    result += `<p>Sua Sorte: ${currentLuck}</p>`;

    gameState.character.luck -= 1;

    if (roll <= currentLuck) {
        result += `<p style="color: #00ff00; font-weight: bold;">Sucesso! Você teve sorte!</p>`;
        const nextSection = event.success;
        setTimeout(() => {
            displaySection(nextSection);
        }, 1500);
    } else {
        result += `<p style="color: #ff0000; font-weight: bold;">Fracasso! Azar!</p>`;
        const nextSection = event.failure;
        setTimeout(() => {
            displaySection(nextSection);
        }, 1500);
    }

    document.getElementById('luck-result').innerHTML = result;
    rollLuckButton.disabled = true;
    updateGameStats();
}

// TESTE DE HABILIDADE
function startSkillTest(event) {
    const roll = roll2d6();
    const playerSkill = gameState.character.skill;
    const difficulty = event.success;

    let result = `<p>Você rolou: ${roll}</p>`;
    result += `<p>Sua Habilidade: ${playerSkill}</p>`;

    if (roll + playerSkill >= difficulty) {
        result += `<p style="color: #00ff00; font-weight: bold;">Sucesso!</p>`;
        const nextSection = event.success;
        setTimeout(() => {
            displaySection(nextSection);
        }, 1500);
    } else {
        result += `<p style="color: #ff0000; font-weight: bold;">Fracasso!</p>`;
        const nextSection = event.failure;
        setTimeout(() => {
            displaySection(nextSection);
        }, 1500);
    }

    luckTestContainer.style.display = 'block';
    document.getElementById('luck-test-text').textContent = event.text;
    document.getElementById('luck-result').innerHTML = result;
    rollLuckButton.style.display = 'none';
}

// EFEITOS DE ITEM
function applyItemEffect(event) {
    if (event.effect.stamina) {
        gameState.character.stamina += event.effect.stamina;
        if (gameState.character.stamina > gameState.character.maxStamina) {
            gameState.character.stamina = gameState.character.maxStamina;
        }
    }
    if (event.effect.skill) {
        gameState.character.skill += event.effect.skill;
    }
    if (event.effect.luck) {
        gameState.character.luck += event.effect.luck;
        gameState.character.maxLuck += event.effect.luck;
    }

    gameState.character.inventory.push(event.item);
    updateGameStats();

    // Exibir opções após obter item
    const section = gameState.story[gameState.currentSection];
    displayChoices(section.choices);
}

// DANO
function takeDamage(damage) {
    gameState.character.stamina -= damage;
    if (gameState.character.stamina < 0) {
        gameState.character.stamina = 0;
    }
    updateGameStats();

    // Exibir opções após dano
    const section = gameState.story[gameState.currentSection];
    displayChoices(section.choices);
}

// FIM DE JOGO
function displayEndGame(ending) {
    if (ending === 'victory') {
        choicesContainer.innerHTML = '<p style="color: #00ff00; font-weight: bold; text-align: center;">VOCÊ VENCEU!</p>';
    } else {
        choicesContainer.innerHTML = '<p style="color: #ff0000; font-weight: bold; text-align: center;">GAME OVER</p>';
    }

    const section = gameState.story[gameState.currentSection];
    displayChoices(section.choices);
}

// REINICIAR JOGO
function restartGame() {
    gameState.currentSection = 1;
    gameState.character = {
        skill: 0,
        stamina: 0,
        maxStamina: 0,
        luck: 0,
        maxLuck: 0,
        inventory: []
    };
    gameState.inCombat = false;
    gameState.currentEnemy = null;
    gameState.combatLog = [];

    skillValue.textContent = '-';
    staminaValue.textContent = '-';
    luckValue.textContent = '-';
    confirmCharacterButton.disabled = true;

    showScreen(characterScreen);
}

// Event Listeners
startButton.addEventListener('click', () => {
    showScreen(characterScreen);
});

rollStatsButton.addEventListener('click', rollStats);
confirmCharacterButton.addEventListener('click', confirmCharacter);
attackButton.addEventListener('click', performAttack);

// Inicializar
async function init() {
    await loadStory();
    showScreen(titleScreen);
}

init();

