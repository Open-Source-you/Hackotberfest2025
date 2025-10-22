// Main calculate function (Caln)
// Calculates BMI and updates #bmi-output and #bmi-status
function Caln() {
  const hInput = document.getElementById('h-input');
  const wInput = document.getElementById('w-input');
  const bmiOut = document.getElementById('bmi-output');
  const statusOut = document.getElementById('bmi-status');
  const tip = document.getElementById('tip');

  const hCm = Number(hInput.value);
  const wKg = Number(wInput.value);

  // Basic validation
  if (!hCm || !wKg || hCm <= 0 || wKg <= 0) {
    bmiOut.textContent = '';
    statusOut.textContent = '';
    tip.textContent = 'Please enter valid height (cm) and weight (kg).';
    return;
  }

  // Convert height to meters
  const hM = hCm / 100;
  const bmi = wKg / (hM * hM);

  // Round to one decimal place
  const bmiRounded = Math.round(bmi * 10) / 10;

  // Determine status
  let status = '';
  if (bmiRounded < 18.5) {
    status = 'Underweight';
  } else if (bmiRounded < 25) {
    status = 'Normal weight';
  } else if (bmiRounded < 30) {
    status = 'Overweight';
  } else {
    status = 'Obesity';
  }

  // Update UI
  bmiOut.textContent = bmiRounded;
  statusOut.textContent = status;
  tip.textContent = `Calculated for ${hCm} cm and ${wKg} kg. BMI = ${bmiRounded}.`;
}

// Reset everything (inputs + outputs)
function resetAll() {
  document.getElementById('h-input').value = '';
  document.getElementById('w-input').value = '';
  document.getElementById('bmi-output').textContent = '';
  document.getElementById('bmi-status').textContent = '';
  document.getElementById('tip').textContent = '';
}

// Clear outputs only
function clearOutputs() {
  document.getElementById('bmi-output').textContent = '';
  document.getElementById('bmi-status').textContent = '';
  document.getElementById('tip').textContent = '';
}

// Copy BMI value to clipboard
function copyBMI() {
  const bmiValue = document.getElementById('bmi-output').textContent.trim();
  if (!bmiValue) {
    alert('No BMI value to copy. Please calculate first.');
    return;
  }

  // Use Clipboard API with fallback
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(bmiValue)
      .then(() => {
        alert('BMI copied to clipboard: ' + bmiValue);
      })
      .catch(() => {
        fallbackCopyTextToClipboard(bmiValue);
      });
  } else {
    fallbackCopyTextToClipboard(bmiValue);
  }
}

// Fallback copy method
function fallbackCopyTextToClipboard(text) {
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.style.position = 'fixed';
  textarea.style.left = '-9999px';
  document.body.appendChild(textarea);
  textarea.select();
  try {
    document.execCommand('copy');
    alert('BMI copied to clipboard: ' + text);
  } catch (err) {
    alert('Failed to copy BMI.');
  }
  document.body.removeChild(textarea);
}

// Save entry to localStorage
function saveEntry() {
  const h = document.getElementById('h-input').value;
  const w = document.getElementById('w-input').value;
  const bmi = document.getElementById('bmi-output').textContent.trim();
  const status = document.getElementById('bmi-status').textContent.trim();

  if (!h || !w) {
    alert('Please enter height and weight before saving.');
    return;
  }

  const entry = {
    height_cm: Number(h),
    weight_kg: Number(w),
    bmi: bmi || null,
    status: status || null,
    timestamp: new Date().toISOString()
  };

  // Save as last entry (single)
  localStorage.setItem('bmi_last_entry', JSON.stringify(entry));
  alert('Entry saved.');
}

// Load last entry from localStorage
function loadLastEntry() {
  const raw = localStorage.getItem('bmi_last_entry');
  if (!raw) {
    alert('No saved entry found.');
    return;
  }
  try {
    const entry = JSON.parse(raw);
    document.getElementById('h-input').value = entry.height_cm ?? '';
    document.getElementById('w-input').value = entry.weight_kg ?? '';
    document.getElementById('bmi-output').textContent = entry.bmi ?? '';
    document.getElementById('bmi-status').textContent = entry.status ?? '';
    document.getElementById('tip').textContent =
      'Loaded saved entry from ' + (entry.timestamp ?? 'unknown time') + '.';
  } catch (err) {
    alert('Failed to load saved entry.');
  }
}

// Show help tips
function showHelp() {
  const tips = [
    'Enter height in centimeters and weight in kilograms.',
    'BMI formula: (weight(kg)) / (height(m))².',
    'Normal BMI is between 18.5 and 24.9.',
    'Use Save Entry to keep the last result. Load Last Entry will restore it.'
  ];
  alert(tips.join('\n'));
  document.getElementById('tip').textContent = tips.join(' • ');
}

// Optional: run Caln() when pressing Enter in inputs
document.addEventListener('DOMContentLoaded', function () {
  const inputs = document.querySelectorAll('.values');
  inputs.forEach((el) => {
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        Caln();
      }
    });
  });
});

