const colors = [
  { name: "Red", hex: "#FF0000" },
  { name: "Green", hex: "#00FF00" },
  { name: "Blue", hex: "#0000FF" },
  { name: "Yellow", hex: "#FFFF00" },
  { name: "Purple", hex: "#800080" },
  { name: "Orange", hex: "#FFA500" },
  { name: "Pink", hex: "#FFC0CB" },
  { name: "Teal", hex: "#008080" },
  { name: "Coral", hex: "#FF7F50" },
  { name: "Indigo", hex: "#4B0082" }
];

const btn = document.getElementById("btn");
const colorDisplay = document.querySelector(".color");

btn.addEventListener("click", function() {
  // Get random color from array
  const randomIndex = Math.floor(Math.random() * colors.length);
  const randomColor = colors[randomIndex];
  
  // Update background and text
  document.body.style.backgroundColor = randomColor.hex;
  colorDisplay.textContent = `${randomColor.name} (${randomColor.hex})`;
});
