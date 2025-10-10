import random
import string
import secrets
import re
from typing import List, Optional
import pyperclip  # You may need to install: pip install pyperclip

class PasswordGenerator:
    def __init__(self, length: int = 12):
        self.length = max(4, length)  # Minimum length of 4
        self.uppercase = True
        self.lowercase = True
        self.digits = True
        self.symbols = True
        self.exclude_ambiguous = False
        self.ambiguous_chars = '0O1lI|`'
        
    def set_length(self, length: int) -> None:
        """Set the desired password length with validation."""
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        if length > 256:
            raise ValueError("Password length cannot exceed 256 characters")
        self.length = length
    
    def configure_character_sets(self, uppercase: bool = True, lowercase: bool = True,
                                 digits: bool = True, symbols: bool = True,
                                 exclude_ambiguous: bool = False) -> None:
        """Configure which character sets to include in the password."""
        if not any([uppercase, lowercase, digits, symbols]):
            raise ValueError("At least one character set must be enabled")
        
        self.uppercase = uppercase
        self.lowercase = lowercase
        self.digits = digits
        self.symbols = symbols
        self.exclude_ambiguous = exclude_ambiguous
    
    def _get_character_pool(self) -> str:
        """Build the character pool based on configuration."""
        pool = ''
        
        if self.uppercase:
            pool += string.ascii_uppercase
        if self.lowercase:
            pool += string.ascii_lowercase
        if self.digits:
            pool += string.digits
        if self.symbols:
            pool += string.punctuation
        
        # Remove ambiguous characters if requested
        if self.exclude_ambiguous:
            pool = ''.join(char for char in pool if char not in self.ambiguous_chars)
        
        return pool
    
    def generate_password(self, ensure_all_types: bool = True) -> str:
        """
        Generate and return a random password.
        
        Args:
            ensure_all_types: If True, ensures at least one character from each enabled set
        """
        pool = self._get_character_pool()
        
        if not pool:
            raise ValueError("No characters available for password generation")
        
        if ensure_all_types and self.length >= 4:
            # Ensure at least one character from each enabled set
            password_chars = []
            
            if self.uppercase:
                chars = string.ascii_uppercase
                if self.exclude_ambiguous:
                    chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
                password_chars.append(secrets.choice(chars))
            
            if self.lowercase:
                chars = string.ascii_lowercase
                if self.exclude_ambiguous:
                    chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
                password_chars.append(secrets.choice(chars))
            
            if self.digits:
                chars = string.digits
                if self.exclude_ambiguous:
                    chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
                password_chars.append(secrets.choice(chars))
            
            if self.symbols:
                chars = string.punctuation
                if self.exclude_ambiguous:
                    chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
                password_chars.append(secrets.choice(chars))
            
            # Fill the rest with random characters from the pool
            remaining_length = self.length - len(password_chars)
            password_chars.extend(secrets.choice(pool) for _ in range(remaining_length))
            
            # Shuffle to avoid predictable patterns
            random.shuffle(password_chars)
            return ''.join(password_chars)
        else:
            # Use secrets for cryptographically secure randomness
            return ''.join(secrets.choice(pool) for _ in range(self.length))
    
    def generate_multiple(self, count: int) -> List[str]:
        """Generate multiple passwords."""
        return [self.generate_password() for _ in range(count)]
    
    def check_password_strength(self, password: str) -> dict:
        """
        Check the strength of a password.
        
        Returns a dictionary with strength score and feedback.
        """
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        
        # Character diversity
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'[0-9]', password):
            score += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        
        # Determine strength level
        if score < 3:
            strength = "Weak 😟"
            feedback.append("Consider using a longer password with more character types")
        elif score < 5:
            strength = "Moderate 😐"
            feedback.append("Good, but could be stronger with more complexity")
        elif score < 7:
            strength = "Strong 😊"
            feedback.append("This is a strong password")
        else:
            strength = "Very Strong 💪"
            feedback.append("Excellent password strength!")
        
        return {
            'score': score,
            'strength': strength,
            'feedback': feedback,
            'length': len(password),
            'has_uppercase': bool(re.search(r'[A-Z]', password)),
            'has_lowercase': bool(re.search(r'[a-z]', password)),
            'has_digits': bool(re.search(r'[0-9]', password)),
            'has_symbols': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        }


def print_password_with_strength(password: str, generator: PasswordGenerator) -> None:
    """Print password with strength indicator."""
    strength = generator.check_password_strength(password)
    
    print(f"\n{'='*50}")
    print(f"🔑 Generated Password: {password}")
    print(f"📊 Strength: {strength['strength']} (Score: {strength['score']}/7)")
    print(f"📏 Length: {strength['length']} characters")
    
    features = []
    if strength['has_uppercase']:
        features.append("Uppercase")
    if strength['has_lowercase']:
        features.append("Lowercase")
    if strength['has_digits']:
        features.append("Numbers")
    if strength['has_symbols']:
        features.append("Symbols")
    
    print(f"✅ Contains: {', '.join(features)}")
    print(f"💡 {strength['feedback'][0]}")
    print('='*50)


def get_user_preferences() -> dict:
    """Get user preferences for password generation."""
    print("\n📋 Password Configuration:")
    
    # Get length
    while True:
        try:
            length = int(input("Enter password length (4-256, default=12): ") or "12")
            if 4 <= length <= 256:
                break
            print("❌ Length must be between 4 and 256")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Get character set preferences
    print("\nCharacter sets to include:")
    uppercase = input("Include uppercase letters? (Y/n): ").lower() != 'n'
    lowercase = input("Include lowercase letters? (Y/n): ").lower() != 'n'
    digits = input("Include numbers? (Y/n): ").lower() != 'n'
    symbols = input("Include symbols? (Y/n): ").lower() != 'n'
    exclude_ambiguous = input("Exclude ambiguous characters (0O1lI|`)? (y/N): ").lower() == 'y'
    
    # Validate at least one character set is selected
    if not any([uppercase, lowercase, digits, symbols]):
        print("⚠️ No character sets selected. Using default (all types).")
        uppercase = lowercase = digits = symbols = True
    
    return {
        'length': length,
        'uppercase': uppercase,
        'lowercase': lowercase,
        'digits': digits,
        'symbols': symbols,
        'exclude_ambiguous': exclude_ambiguous
    }


def save_passwords_to_file(passwords: List[str], filename: str = "passwords.txt") -> None:
    """Save generated passwords to a file."""
    try:
        with open(filename, 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Passwords generated on {__import__('datetime').datetime.now()}\n")
            f.write('='*50 + '\n')
            for i, password in enumerate(passwords, 1):
                f.write(f"{i}. {password}\n")
        print(f"✅ Passwords saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving passwords: {e}")


def main():
    print("\n" + "="*50)
    print("🔐 Advanced Password Generator 🔐".center(50))
    print("="*50)
    
    generator = PasswordGenerator()
    
    while True:
        print("\n📌 Main Menu:")
        print("1. Quick generate (default settings)")
        print("2. Custom generate (choose settings)")
        print("3. Generate multiple passwords")
        print("4. Check password strength")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            # Quick generate with default settings
            password = generator.generate_password()
            print_password_with_strength(password, generator)
            
            # Copy to clipboard option
            if input("\n📋 Copy to clipboard? (y/N): ").lower() == 'y':
                try:
                    pyperclip.copy(password)
                    print("✅ Password copied to clipboard!")
                except:
                    print("⚠️ Clipboard not available. Please copy manually.")
        
        elif choice == '2':
            # Custom generate
            prefs = get_user_preferences()
            generator.set_length(prefs['length'])
            generator.configure_character_sets(
                uppercase=prefs['uppercase'],
                lowercase=prefs['lowercase'],
                digits=prefs['digits'],
                symbols=prefs['symbols'],
                exclude_ambiguous=prefs['exclude_ambiguous']
            )
            
            password = generator.generate_password()
            print_password_with_strength(password, generator)
            
            # Copy to clipboard option
            if input("\n📋 Copy to clipboard? (y/N): ").lower() == 'y':
                try:
                    pyperclip.copy(password)
                    print("✅ Password copied to clipboard!")
                except:
                    print("⚠️ Clipboard not available. Please copy manually.")
        
        elif choice == '3':
            # Generate multiple passwords
            prefs = get_user_preferences()
            
            while True:
                try:
                    count = int(input("How many passwords to generate? (1-20): "))
                    if 1 <= count <= 20:
                        break
                    print("❌ Please enter a number between 1 and 20")
                except ValueError:
                    print("❌ Please enter a valid number")
            
            generator.set_length(prefs['length'])
            generator.configure_character_sets(
                uppercase=prefs['uppercase'],
                lowercase=prefs['lowercase'],
                digits=prefs['digits'],
                symbols=prefs['symbols'],
                exclude_ambiguous=prefs['exclude_ambiguous']
            )
            
            passwords = generator.generate_multiple(count)
            
            print(f"\n🎯 Generated {count} passwords:")
            print("="*50)
            for i, pwd in enumerate(passwords, 1):
                print(f"{i:2}. {pwd}")
            print("="*50)
            
            # Save to file option
            if input("\n💾 Save to file? (y/N): ").lower() == 'y':
                save_passwords_to_file(passwords)
        
        elif choice == '4':
            # Check password strength
            password = input("\nEnter password to check: ")
            if password:
                strength = generator.check_password_strength(password)
                print(f"\n📊 Strength: {strength['strength']} (Score: {strength['score']}/7)")
                print(f"💡 {strength['feedback'][0]}")
        
        elif choice == '5':
            print("\n👋 Thank you for using Password Generator!")
            print("Stay secure! 🔒")
            break
        
        else:
            print("❌ Invalid option. Please try again.")


if __name__ == "__main__":
    main()
