import wikipedia as wiki
import textwrap
import sys
from colorama import init, Fore, Style
import time

# Initialize colorama for colored output
init(autoreset=True)

class WikipediaBot:
    def __init__(self):
        self.language = 'en'
        wiki.set_lang(self.language)
        self.search_history = []
        
    def print_header(self):
        """Display application header"""
        print("\n" + "="*60)
        print(Fore.CYAN + "WIKIPEDIA KNOWLEDGE BOT".center(60))
        print("="*60 + "\n")
    
    def print_separator(self):
        """Print a visual separator"""
        print(Fore.YELLOW + "-"*60)
    
    def search_topic(self):
        """Search for Wikipedia articles"""
        while True:
            # Get search query
            print(Fore.GREEN + "\n[OPTIONS] Enter topic, 'random' for random article, or 'quit' to exit")
            topic = input(Fore.CYAN + "Search Topic: " + Style.RESET_ALL).strip()
            
            # Handle special commands
            if topic.lower() == 'quit':
                self.exit_program()
            elif topic.lower() == 'random':
                return [wiki.random()]
            elif topic.lower() == 'history':
                self.show_history()
                continue
            elif not topic:
                print(Fore.RED + "Please enter a valid topic!")
                continue
            
            # Search Wikipedia
            print(Fore.YELLOW + "\nSearching Wikipedia...")
            try:
                results = wiki.search(topic, results=20)
                
                if not results:
                    print(Fore.RED + f"No results found for '{topic}'")
                    retry = input("Try another search? (y/n): ").lower()
                    if retry != 'y':
                        return None
                    continue
                
                return results
                
            except Exception as e:
                print(Fore.RED + f"Search error: {e}")
                return None
    
    def display_results(self, results):
        """Display search results in a formatted way"""
        print(Fore.GREEN + f"\n[+] Found {len(results)} articles:\n")
        
        # Display in two columns for better readability
        for i in range(0, len(results), 2):
            left = f"{i+1:2}. {results[i][:35]:<35}"
            print(Fore.CYAN + left, end="")
            
            if i+1 < len(results):
                right = f"{i+2:2}. {results[i+1][:35]}"
                print(Fore.CYAN + "  " + right)
            else:
                print()
        
        print()
    
    def get_user_choice(self, max_options):
        """Get and validate user's article selection"""
        while True:
            try:
                print(Fore.YELLOW + "Enter article number (or 0 to search again)")
                choice = input(Fore.CYAN + "Select: " + Style.RESET_ALL).strip()
                
                if choice == '0':
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= max_options:
                    return choice_num - 1
                else:
                    print(Fore.RED + f"Please enter a number between 1 and {max_options}")
                    
            except ValueError:
                print(Fore.RED + "Invalid input! Please enter a number.")
    
    def display_article(self, article_title):
        """Display article information with better error handling"""
        try:
            print(Fore.YELLOW + "\nLoading article...")
            page = wiki.page(article_title, auto_suggest=False)
            
            # Add to history
            self.search_history.append(page.title)
            
            # Display article header
            self.print_separator()
            print(Fore.GREEN + f"\n📖 {page.title}\n")
            print(Fore.CYAN + f"🔗 URL: {page.url}")
            
            # Display categories if available
            if page.categories:
                categories = ', '.join(page.categories[:5])
                print(Fore.MAGENTA + f"📂 Categories: {categories}")
            
            # Display summary with proper formatting
            print(Fore.YELLOW + "\n📝 SUMMARY:")
            self.print_separator()
            
            summary = wiki.summary(article_title, sentences=4)
            wrapped_summary = textwrap.fill(summary, width=60)
            print(Style.RESET_ALL + wrapped_summary)
            
            # Show article options
            self.article_options(page)
            
        except wiki.exceptions.DisambiguationError as e:
            self.handle_disambiguation(e)
            
        except wiki.exceptions.PageError:
            print(Fore.RED + f"\n[-] Error: Page '{article_title}' does not exist!")
            self.suggest_alternatives(article_title)
            
        except Exception as e:
            print(Fore.RED + f"\n[-] Unexpected error: {e}")
            # Provide direct Wikipedia link as fallback
            fallback_url = f"https://en.wikipedia.org/wiki/{article_title.replace(' ', '_')}"
            print(Fore.YELLOW + f"Try this link: {fallback_url}")
    
    def handle_disambiguation(self, disambiguation_error):
        """Handle disambiguation pages properly"""
        print(Fore.YELLOW + "\n⚠️  Multiple articles found. Did you mean:")
        options = disambiguation_error.options[:15]
        
        for i, option in enumerate(options, 1):
            print(Fore.CYAN + f"  {i:2}. {option}")
        
        choice = self.get_user_choice(len(options))
        if choice is not None:
            self.display_article(options[choice])
    
    def suggest_alternatives(self, original_title):
        """Suggest alternative articles when page not found"""
        print(Fore.YELLOW + "\nSearching for similar articles...")
        suggestions = wiki.search(original_title, results=5)
        
        if suggestions:
            print(Fore.GREEN + "Perhaps you meant one of these:")
            for i, suggestion in enumerate(suggestions, 1):
                print(Fore.CYAN + f"  {i}. {suggestion}")
            
            choice = self.get_user_choice(len(suggestions))
            if choice is not None:
                self.display_article(suggestions[choice])
    
    def article_options(self, page):
        """Provide additional options for the current article"""
        while True:
            print(Fore.YELLOW + "\n" + "-"*60)
            print(Fore.GREEN + "OPTIONS:")
            print("  1. Read more content")
            print("  2. View images")
            print("  3. See related articles")
            print("  4. Translate to another language")
            print("  5. Get article in different format")
            print("  6. New search")
            print("  0. Exit")
            
            choice = input(Fore.CYAN + "\nSelect option: " + Style.RESET_ALL).strip()
            
            if choice == '1':
                self.show_more_content(page)
            elif choice == '2':
                self.show_images(page)
            elif choice == '3':
                self.show_related_links(page)
            elif choice == '4':
                self.translate_article(page.title)
            elif choice == '5':
                self.show_different_format(page)
            elif choice == '6':
                return
            elif choice == '0':
                self.exit_program()
            else:
                print(Fore.RED + "Invalid option!")
    
    def show_more_content(self, page):
        """Display more article content"""
        print(Fore.YELLOW + "\n📄 EXTENDED CONTENT:")
        self.print_separator()
        
        # Get first 2000 characters
        content = page.content[:2000]
        
        # Split into paragraphs for better readability
        paragraphs = content.split('\n\n')[:3]
        for para in paragraphs:
            if para.strip():
                wrapped = textwrap.fill(para, width=60)
                print(wrapped)
                print()
        
        print(Fore.YELLOW + "[...Content truncated...]")
    
    def show_images(self, page):
        """Display image URLs from the article"""
        images = page.images[:10]
        
        if images:
            print(Fore.YELLOW + "\n🖼️  IMAGES IN THIS ARTICLE:")
            self.print_separator()
            for i, img_url in enumerate(images, 1):
                # Show only filename for readability
                filename = img_url.split('/')[-1][:60]
                print(Fore.CYAN + f"  {i}. {filename}")
        else:
            print(Fore.RED + "No images found in this article.")
    
    def show_related_links(self, page):
        """Show related Wikipedia articles"""
        links = page.links[:15]
        
        if links:
            print(Fore.YELLOW + "\n🔗 RELATED ARTICLES:")
            self.print_separator()
            for i, link in enumerate(links, 1):
                print(Fore.CYAN + f"  {i:2}. {link}")
            
            # Option to read a related article
            print(Fore.GREEN + "\nEnter number to read related article (or 0 to go back)")
            choice = self.get_user_choice(len(links))
            if choice is not None:
                self.display_article(links[choice])
        else:
            print(Fore.RED + "No related links found.")
    
    def translate_article(self, title):
        """Change language for article"""
        print(Fore.YELLOW + "\nAvailable languages: en, es, fr, de, it, pt, ru, ja, zh")
        lang = input(Fore.CYAN + "Enter language code: ").strip().lower()
        
        try:
            wiki.set_lang(lang)
            self.language = lang
            print(Fore.GREEN + f"Language changed to: {lang}")
            
            # Try to load article in new language
            self.display_article(title)
            
            # Reset to English
            wiki.set_lang('en')
            self.language = 'en'
            
        except Exception as e:
            print(Fore.RED + f"Error changing language: {e}")
            wiki.set_lang('en')
    
    def show_different_format(self, page):
        """Show article in different formats"""
        print(Fore.YELLOW + "\n📋 ARTICLE FORMATS:")
        print("1. Brief (1 sentence)")
        print("2. Short (3 sentences)")
        print("3. Medium (5 sentences)")
        print("4. Section headers only")
        
        choice = input(Fore.CYAN + "Select format: ").strip()
        
        try:
            if choice == '1':
                summary = wiki.summary(page.title, sentences=1)
            elif choice == '2':
                summary = wiki.summary(page.title, sentences=3)
            elif choice == '3':
                summary = wiki.summary(page.title, sentences=5)
            elif choice == '4':
                # Show section headers
                content = page.content
                headers = [line for line in content.split('\n') if line.startswith('==')]
                print(Fore.GREEN + "\nSection Headers:")
                for header in headers[:10]:
                    print(Fore.CYAN + f"  • {header.replace('=', '').strip()}")
                return
            else:
                print(Fore.RED + "Invalid choice!")
                return
            
            print(Fore.GREEN + f"\n{page.title} - Summary:")
            print(textwrap.fill(summary, width=60))
            
        except Exception as e:
            print(Fore.RED + f"Error: {e}")
    
    def show_history(self):
        """Display search history"""
        if self.search_history:
            print(Fore.YELLOW + "\n📚 SEARCH HISTORY:")
            self.print_separator()
            for i, title in enumerate(self.search_history[-10:], 1):
                print(Fore.CYAN + f"  {i}. {title}")
        else:
            print(Fore.RED + "No search history yet!")
    
    def exit_program(self):
        """Exit the program gracefully"""
        print(Fore.GREEN + "\n" + "="*60)
        print("Thank you for using Wikipedia Bot!")
        print("Happy learning! 📚")
        print("="*60 + "\n")
        sys.exit(0)
    
    def run(self):
        """Main program loop"""
        self.print_header()
        print(Fore.GREEN + "Welcome to Wikipedia Bot! Your gateway to knowledge.")
        print(Fore.YELLOW + "Commands: 'random' for random article, 'history' to view history, 'quit' to exit")
        
        while True:
            # Search for topic
            results = self.search_topic()
            if results is None:
                continue
            
            # Display results
            self.display_results(results)
            
            # Get user choice
            choice = self.get_user_choice(len(results))
            if choice is None:
                continue
            
            # Display selected article
            self.display_article(results[choice])


def main():
    # Check dependencies
    try:
        import colorama
    except ImportError:
        print("Installing required package: colorama")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
        print("Please restart the program.")
        return
    
    # Run the bot
    bot = WikipediaBot()
    try:
        bot.run()
    except KeyboardInterrupt:
        bot.exit_program()
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please report this issue for improvement.")

if __name__ == "__main__":
    main()
