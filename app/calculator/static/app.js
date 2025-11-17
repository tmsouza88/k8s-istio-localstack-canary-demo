let display = document.getElementById('display');
let currentValue = '0';

function updateDisplay() {
  display.textContent = currentValue;
}

function appendToDisplay(value) {
  if (currentValue === '0' && value !== '.') {
    currentValue = value;
  } else {
    currentValue += value;
  }
  updateDisplay();
}

function clearDisplay() {
  currentValue = '0';
  updateDisplay();
}

function backspace() {
  if (currentValue.length > 1) {
    currentValue = currentValue.slice(0, -1);
  } else {
    currentValue = '0';
  }
  updateDisplay();
}

function calculate() {
  try {
    // Substitui × por * para avaliação
    let expression = currentValue.replace(/×/g, '*');
    let result = eval(expression);
    currentValue = result.toString();
    updateDisplay();
  } catch (error) {
    currentValue = 'Erro';
    updateDisplay();
    setTimeout(() => {
      currentValue = '0';
      updateDisplay();
    }, 1500);
  }
}

// Suporte para teclado
document.addEventListener('keydown', function(event) {
  if (event.key >= '0' && event.key <= '9') {
    appendToDisplay(event.key);
  } else if (event.key === '.') {
    appendToDisplay('.');
  } else if (event.key === '+' || event.key === '-' || event.key === '*' || event.key === '/') {
    appendToDisplay(event.key);
  } else if (event.key === 'Enter') {
    calculate();
  } else if (event.key === 'Escape') {
    clearDisplay();
  } else if (event.key === 'Backspace') {
    backspace();
  }
});