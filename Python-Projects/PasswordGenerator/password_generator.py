#!/usr/bin/env python3
"""
Password Generator & Strength Checker
Author: [Your Name]
Description: Generate secure passwords and check password strength
Hacktoberfest 2025 Contribution
"""

import random
import string
import re

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate_password(self, length=12, use_uppercase=True, use_digits=True, use_symbols=True):
        """Generate a random password based on specified criteria"""
        if length < 4:
            return "❌ Password length must be at least 4 characters!"
        
        # Build character pool
        char_pool = self.lowercase
        password_chars = [random.choice(self.lowercase)]  # Ensure at least one lowercase
        
        if use_uppercase:
            char_pool += self.uppercase
            password_chars.append(random.choice(self.uppercase))
        
        if use_digits:
            char_pool += self.digits
            password_chars.append(random.choice(self.digits))
        
        if use_symbols:
            char_pool += self.symbols
            password_chars.append(random.choice(self.symbols))
        
        # Fill remaining length
        remaining_length = length - len(password_chars)
        password_chars.extend(random.choice(char_pool) for _ in range(remaining_length))
        
        # Shuffle to avoid predictable patterns
        random.shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def check_strength(self, password):
        """Check password strength and return score with feedback"""
        score = 0
        feedback = []
        
        # Length check
        length = len(password)
        if length >= 12:
            score += 2
            feedback.append("✅ Good length (12+ characters)")
        elif length >= 8:
            score += 1
            feedback.append("⚠️ Acceptable length (8-11 characters)")
        else:
            feedback.append("❌ Too short (less than 8 characters)")
        
        # Character variety checks
        if re.search(r'[a-z]', password):
            score += 1
            feedback.append("✅ Contains lowercase letters")
        else:
            feedback.append("❌ Missing lowercase letters")
        
        if re.search(r'[A-Z]', password):
            score += 1
            feedback.append("✅ Contains uppercase letters")
        else:
            feedback.append("⚠️ Missing uppercase letters")
        
        if re.search(r'\d', password):
            score += 1
            feedback.append("✅ Contains digits")
        else:
            feedback.append("⚠️ Missing digits")
        
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 2
            feedback.append("✅ Contains special symbols")
        else:
            feedback.append("⚠️ Missing special symbols")
        
        # Common patterns check
        common_patterns = ['123', '456', '789', 'abc', 'password', 'qwerty', '000', '111']
        if any(pattern in password.lower() for pattern in common_patterns):
            score -= 2
            feedback.append("❌ Contains common patterns")
        
        # Determine strength level
        if score >= 6:
            strength = "🟢 STRONG"
        elif score >= 4:
            strength = "🟡 MEDIUM"
        else:
            strength = "🔴 WEAK"
        
        return {
            'score': max(0, score),
            'strength': strength,
            'feedback': feedback
        }

def display_menu():
    """Display main menu"""
    print("\n" + "="*60)
    print("       🔐 PASSWORD GENERATOR & STRENGTH CHECKER 🔐")
    print("="*60)
    print("1. 🎲 Generate Password")
    print("2. 🔍 Check Password Strength")
    print("3. 📋 Generate Multiple Passwords")
    print("4. ℹ️ Password Security Tips")
    print("5. 🚪 Exit")
    print("="*60)

def display_security_tips():
    """Display password security tips"""
    print("\n" + "="*60)
    print("           🛡️ PASSWORD SECURITY TIPS 🛡️")
    print("="*60)
    print("""
1. ✅ Use at least 12 characters
2. ✅ Mix uppercase, lowercase, numbers, and symbols
3. ✅ Avoid common words and patterns
4. ✅ Use unique passwords for each account
5. ✅ Consider using a password manager
6. ❌ Don't share passwords via email or text
7. ❌ Don't reuse passwords across sites
8. ❌ Don't use personal information (birthdays, names)
9. 🔄 Change passwords if a breach occurs
10. 🔐 Enable two-factor authentication when possible
    """)
    print("="*60)

def main():
    """Main program loop"""
    generator = PasswordGenerator()
    
    print("\n🎉 Welcome to Password Generator & Strength Checker! 🎉")
    print("💚 Hacktoberfest 2025 Contribution 💚")
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            # Generate password
            print("\n📝 Password Generation Options")
            try:
                length = int(input("Enter password length (default 12): ") or "12")
                use_upper = input("Include uppercase letters? (y/n, default y): ").lower() != 'n'
                use_digits = input("Include digits? (y/n, default y): ").lower() != 'n'
                use_symbols = input("Include symbols? (y/n, default y): ").lower() != 'n'
                
                password = generator.generate_password(length, use_upper, use_digits, use_symbols)
                
                if password.startswith("❌"):
                    print(f"\n{password}")
                else:
                    print(f"\n🎉 Generated Password: {password}")
                    
                    # Auto-check strength
                    result = generator.check_strength(password)
                    print(f"\n🔍 Password Strength: {result['strength']} (Score: {result['score']}/7)")
                    
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
        
        elif choice == '2':
            # Check password strength
            password = input("\n🔑 Enter password to check: ")
            if password:
                result = generator.check_strength(password)
                print(f"\n{'='*60}")
                print(f"🔍 Password Strength Analysis")
                print(f"{'='*60}")
                print(f"Password: {'*' * len(password)}")
                print(f"Strength: {result['strength']}")
                print(f"Score: {result['score']}/7")
                print(f"\n📊 Detailed Feedback:")
                for item in result['feedback']:
                    print(f"  {item}")
                print(f"{'='*60}")
            else:
                print("❌ Password cannot be empty!")
        
        elif choice == '3':
            # Generate multiple passwords
            try:
                count = int(input("\n🔢 How many passwords to generate? (default 5): ") or "5")
                length = int(input("Password length (default 12): ") or "12")
                
                print(f"\n🎲 Generated {count} Passwords:")
                print("="*60)
                for i in range(count):
                    pwd = generator.generate_password(length)
                    print(f"{i+1}. {pwd}")
                print("="*60)
                
            except ValueError:
                print("❌ Invalid input! Please enter valid numbers.")
        
        elif choice == '4':
            # Display security tips
            display_security_tips()
        
        elif choice == '5':
            # Exit
            print("\n👋 Thank you for using Password Generator!")
            print("🔒 Stay secure! 🔒")
            print("💚 Happy Hacktoberfest 2025! 💚\n")
            break
        
        else:
            print("\n❌ Invalid choice! Please select 1-5.")

if __name__ == "__main__":
    main()
