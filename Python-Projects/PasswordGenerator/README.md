# 🔐 Password Generator & Strength Checker

A Python tool for generating secure passwords and analyzing their strength with detailed feedback.

---

## ✨ Features

### 🧩 Password Generation
- 🎲 Customizable length (minimum 4 characters)
- ✅ Toggle uppercase letters
- ✅ Toggle digits (0–9)
- ✅ Toggle special symbols
- 🔀 Random shuffle for unpredictability
- 📋 Batch generation mode

### 🧠 Password Strength Analysis
- 📏 Length evaluation
- 🔤 Character variety checking (lowercase, uppercase, digits, symbols)
- ⚠️ Common pattern detection
- 📊 Scoring system (0–7 points)
- 💡 Detailed feedback and recommendations
- 🎯 Strength classification (Weak / Medium / Strong)

### 🛠️ Additional Features
- 🛡️ Password security tips and best practices
- 🎨 User-friendly menu interface
- ✅ Input validation and error handling

---

## 🚀 How to Run

### Prerequisites
- Python 3.x installed

### Installation & Usage
```bash
git clone https://github.com/Open-Source-you/Hackotberfest2025.git
cd Hackotberfest2025/Python-Projects/PasswordGenerator
python password_generator.py
```

---

## 💻 Usage Examples

### 🔹 Example 1: Generate a Password
```
Enter your choice (1-5): 1

📝 Password Generation Options
Enter password length (default 12): 16
Include uppercase letters? (y/n, default y): y
Include digits? (y/n, default y): y
Include symbols? (y/n, default y): y

🎉 Generated Password: K9@mP#xL2$qR7&Vn

🔍 Password Strength: 🟢 STRONG (Score: 7/7)
```

---

### 🔹 Example 2: Check Password Strength
```
Enter your choice (1-5): 2

🔑 Enter password to check: MyPassword123!

============================================================
🔍 Password Strength Analysis
Password: ****
Strength: 🟡 MEDIUM
Score: 5/7

📊 Detailed Feedback:
✅ Good length (12+ characters)
✅ Contains lowercase letters
✅ Contains uppercase letters
✅ Contains digits
✅ Contains special symbols
```

---

### 🔹 Example 3: Batch Generation
```
Enter your choice (1-5): 3

🔢 How many passwords to generate? (default 5): 3
Password length (default 12): 14

🎲 Generated 3 Passwords:
aB8#kL@mP9$xR2
qW5&rT#yU7^iO3
zX6*cV!bN8@mK4
============================================================
```

---

## 🎯 Password Strength Scoring

| Score | Strength | Criteria |
|:------:|:----------:|:----------|
| 0–3 | 🔴 WEAK | Missing multiple character types or too short |
| 4–5 | 🟡 MEDIUM | Good length with some character variety |
| 6–7 | 🟢 STRONG | 12+ characters with full character variety |

### Scoring Breakdown
- **Length**: 2 points (12+ chars) or 1 point (8–11 chars)
- **Lowercase letters**: 1 point  
- **Uppercase letters**: 1 point  
- **Digits**: 1 point  
- **Special symbols**: 2 points  
- **Common patterns**: −2 points (penalty)

---

## 🛡️ Security Best Practices

✅ **DO:**
- Use at least 12 characters  
- Mix character types (uppercase, lowercase, digits, symbols)  
- Use unique passwords for each account  
- Store passwords in a password manager  
- Enable two-factor authentication  

❌ **DON’T:**
- Use personal information (names, birthdays)  
- Reuse passwords across sites  
- Share passwords via email or text  
- Use common patterns (123456, password, qwerty)

---

## 🧩 Technical Details

**Language:** Python 3.x  

**Libraries Used:**
- `random` — Random character selection  
- `string` — Character sets (letters, digits, punctuation)  
- `re` — Regular expressions for pattern matching  

**Concepts Demonstrated:**
- Object-oriented programming (classes and methods)  
- Regular expressions  
- User input handling  
- String manipulation  
- Control flow and loops  
- Error handling  

---

## 🤝 Contributing

Contributions are welcome! Ideas for improvement:
- Add password export functionality (save to file)
- Implement password history tracking
- Add pronounceable password generation
- Create GUI version using Tkinter
- Add unit tests
- Estimate password cracking time

---

## 👨‍💻 Author

**[Your Name]**  
GitHub: [@YourUsername](https://github.com/YourUsername)

---

## 📝 License

This project follows the repository’s license terms.

---

## 🎃 Hacktoberfest 2025

This contribution is part of **Hacktoberfest 2025**!  
Made with ❤️ and ☕  

---

⭐ **If you find this project useful, please star the repository!**
