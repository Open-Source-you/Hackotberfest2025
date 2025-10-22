```javascript
const screen = document.getElementById('screen');
const buttons = document.querySelectorAll('button');
let screenValue = '';

buttons.forEach(item => {
  item.addEventListener('click', (e) => {
    let buttonText = e.target.innerText;
    buttonText = (buttonText === 'X') ? '*' : buttonText;

    if (buttonText === 'C') {
      screenValue = "";
    } else if (buttonText === '=') {
      try {
        screenValue = eval(screenValue);
      } catch (error) {
        screenValue = "Error";
      }
    } else {
      screenValue += buttonText;
    }

    screen.value = screenValue;
  });
});
```
