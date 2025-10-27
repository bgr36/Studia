const words = ["JAVASCRIPT", "TEST", "WISIELEC"];
let selectedWord = "";
let guessedLetters = [];
let mistakes = 0;
const maxMistakes = 10;

const canvas = document.getElementById("hangman-canvas");
const ctx = canvas.getContext("2d");

// function resizeCanvas() {
//     const canvas = document.getElementById('hangman');
//     const containerWidth = canvas.parentElement.clientWidth;
//     canvas.width = containerWidth;
//     canvas.height = containerWidth;
//     drawHangman(mistakes); // <-- dodane: odtworzenie aktualnego stanu rysunku
// }

function drawHangman(step) {
  switch (step) {
    case 1: ctx.moveTo(50, 250); ctx.lineTo(250, 250); ctx.stroke(); break;
    case 2: ctx.moveTo(100, 250); ctx.lineTo(100, 50); ctx.stroke(); break;
    case 3: ctx.lineTo(200, 50); ctx.stroke(); break;
    case 4: ctx.lineTo(200, 80); ctx.stroke(); break;
    case 5: ctx.beginPath(); ctx.arc(200, 100, 20, 0, Math.PI * 2); ctx.stroke(); break;
    case 6: ctx.moveTo(200, 120); ctx.lineTo(200, 180); ctx.stroke(); break;
    case 7: ctx.moveTo(200, 140); ctx.lineTo(180, 160); ctx.stroke(); break;
    case 8: ctx.moveTo(200, 140); ctx.lineTo(220, 160); ctx.stroke(); break;
    case 9: ctx.moveTo(200, 180); ctx.lineTo(180, 220); ctx.stroke(); break;
    case 10: ctx.moveTo(200, 180); ctx.lineTo(220, 220); ctx.stroke(); break;
  }
}

function saveGameState() {
  const gameState = {
    selectedWord,
    guessedLetters,
    mistakes
  };
  localStorage.setItem("hangmanState", JSON.stringify(gameState));
}

function loadGameState() {
  const saved = localStorage.getItem("hangmanState");
  if (saved) {
    const state = JSON.parse(saved);
    selectedWord = state.selectedWord;
    guessedLetters = state.guessedLetters;
    mistakes = state.mistakes;
    document.getElementById("message").textContent = "";
    canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
    ctx.lineWidth = 4;
    ctx.beginPath();
    drawHangmanSteps(mistakes);
    updateWord();
    createAlphabet();
    updateUsedButtons();
    if (mistakes >= maxMistakes) endGame(false);
    if (checkWin()) endGame(true);
    return true;
  }
  return false;
}

function clearGameState() {
  localStorage.removeItem("hangmanState");
}

function drawHangmanSteps(m) {
  for (let i = 1; i <= m; i++) drawHangman(i);
}

function initGame() {
  clearGameState();
  selectedWord = words[Math.floor(Math.random() * words.length)];
  guessedLetters = [];
  mistakes = 0;
  document.getElementById("word-container").innerHTML = selectedWord.split('').map(() => "_").join(" ");
  document.getElementById("message").textContent = "";
  canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
  ctx.lineWidth = 4;
  ctx.beginPath();
  createAlphabet();
  loadGameState();
//   saveGameState();
}

function createAlphabet() {
  const alphabet = "ABCDEFGHIJKLMNOPRSTUVWXYZ";
  const container = document.getElementById("alphabet");
  container.innerHTML = "";
  for (let letter of alphabet) {
    const btn = document.createElement("button");
    btn.textContent = letter;
    btn.value = letter;
    btn.onclick = () => handleGuess(letter, btn);
    container.appendChild(btn);
  }
}

function updateUsedButtons() {
  document.querySelectorAll("#alphabet button").forEach(btn => {
    if (guessedLetters.includes(btn.value)) {
      btn.classList.add("used");
      btn.disabled = true;
    }
  });
}

function handleGuess(letter, button) {
  button.classList.add("used");
  button.disabled = true;

  if (!guessedLetters.includes(letter)) {
    guessedLetters.push(letter);
    if (selectedWord.includes(letter)) {
      updateWord();
    } else {
      mistakes++;
      drawHangman(mistakes);
    }

    saveGameState();

    if (mistakes >= maxMistakes) endGame(false);
    else if (checkWin()) endGame(true);
  }
}

function updateWord() {
  document.getElementById("word-container").innerHTML = selectedWord
    .split('')
    .map(l => guessedLetters.includes(l) ? l : "_")
    .join(" ");
}

function checkWin() {
  return selectedWord.split('').every(l => guessedLetters.includes(l));
}

function endGame(won) {
  document.getElementById("message").textContent = won ? "Wygrałeś!" : `Przegrałeś! Słowo to: ${selectedWord}`;
  document.querySelectorAll("#alphabet button").forEach(btn => btn.disabled = true);
  clearGameState(); 
}

document.getElementById("new-game").onclick = initGame;
// window.addEventListener('resize', resizeCanvas);
window.addEventListener('DOMContentLoaded', () => {
//   resizeCanvas();
  if (!loadGameState()) initGame();
});
