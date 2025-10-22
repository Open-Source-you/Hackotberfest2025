import wikipedia as wiki
import textwrap
import webbrowser
from datetime import datetime

class WikiSearch:
    def __init__(self):
        wiki.set_lang("en")
        self.history = []
    
    def search_articles(self):
        # Get search query
        topic = input("\n📚 Enter topic (or 'random' for random article): ").strip()
        
        if topic.lower() == 'random':
            return self.random_article()
        
        # Search with limit
        print("\n🔍 Searching...")
        results = wiki.search(topic, results=15)
        
        if not results:
            print("❌ No results found!")
            return None
        
        # Display results in columns
        print(f"\n✅ Found {len(results)} articles:\n")
        for i, title in enumerate(results, 1):
            print(f"{i:2}. {title[:50]:<50}", end="")
            if i % 2 == 0:
                print()
        print("\n")
        
        # Get selection
        try:
            choice = input("Select article (number) or 's' to search again: ").strip()
            if choice.lower() == 's':
                return self.search_articles()
            
            article_num = int(choice) - 1
            if 0 <= article_num < len(results):
                return results[article_num]
            else:
                print("Invalid selection!")
                return None
        except ValueError:
            print("Invalid input!")
            return None
    
    def display_article(self, article_title):
        try:
            # Get page
            page = wiki.page(article_title)
            self.history.append((datetime.now().strftime("%H:%M"), page.title))
            
            # Display header
            print("\n" + "="*70)
            print(f"📖 {page.title}".center(70))
            print("="*70)
            
            # Basic info
            print(f"\n🔗 URL: {page.url}")
            print(f"📝 Categories: {', '.join(page.categories[:3])}")
            
            # Summary with word wrap
            print("\n📄 SUMMARY:")
            print("-"*70)
            summary = wiki.summary(article_title, sentences=3)
            wrapped = textwrap.fill(summary, width=70)
            print(wrapped)
            
            # Options menu
            self.article_menu(page)
            
        except wiki.DisambiguationError as e:
            
