"""
Spam Email Classifier
A CLI tool to detect spam emails using machine learning
"""

import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import box
import time

console = Console()


class SpamClassifier:
    """Machine learning classifier for spam detection"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=3000, stop_words='english')
        self.model = MultinomialNB()
        self.is_trained = False
    
    def train(self, emails, labels):
        """Train the classifier with email data"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]Training model..."),
            console=console
        ) as progress:
            progress.add_task("train", total=None)
            
            X = self.vectorizer.fit_transform(emails)
            self.model.fit(X, labels)
            self.is_trained = True
            
            time.sleep(0.5)
        
        console.print("[green]Model trained successfully[/]")
    
    def predict(self, email):
        """Predict if an email is spam or not"""
        if not self.is_trained:
            raise Exception("Model not trained yet")
        
        X = self.vectorizer.transform([email])
        prediction = self.model.predict(X)[0]
        probability = self.model.predict_proba(X)[0]
        
        return prediction, probability
    
    def save_model(self, path='model'):
        """Save trained model to disk"""
        os.makedirs(path, exist_ok=True)
        
        with open(f'{path}/vectorizer.pkl', 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        with open(f'{path}/classifier.pkl', 'wb') as f:
            pickle.dump(self.model, f)
        
        console.print(f"[green]Model saved to {path}/[/]")
    
    def load_model(self, path='model'):
        """Load trained model from disk"""
        try:
            with open(f'{path}/vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            with open(f'{path}/classifier.pkl', 'rb') as f:
                self.model = pickle.load(f)
            
            self.is_trained = True
            console.print("[green]Model loaded successfully[/]")
            return True
        except FileNotFoundError:
            console.print("[yellow]No saved model found[/]")
            return False


def create_sample_dataset():
    """Create a sample dataset for demonstration"""
    spam_emails = [
        "Congratulations! You've won $1000. Click here to claim your prize now!",
        "URGENT: Your account will be closed. Verify your information immediately.",
        "Get rich quick! Make $5000 per week working from home.",
        "You have been selected for a free iPhone. Click now!",
        "Lose weight fast with this miracle pill. Order now!",
        "Your package is waiting. Pay shipping fee to receive it.",
        "Hot singles in your area want to meet you tonight!",
        "You've inherited millions. Send your bank details to claim.",
        "Earn money online. No experience needed. Start today!",
        "Limited time offer! Buy now and save 90 percent!",
        "Your computer has a virus. Download our software immediately.",
        "Claim your lottery winnings now. Send processing fee.",
        "Work from home and earn thousands. No skills required.",
        "Free vacation to Bahamas. Just pay taxes and fees.",
        "Your credit card has been compromised. Update details now."
    ]
    
    ham_emails = [
        "Hi, can we schedule a meeting for tomorrow at 3 PM?",
        "The project report is attached. Please review and send feedback.",
        "Reminder: Team standup is at 10 AM today.",
        "Thanks for your help with the presentation yesterday.",
        "Could you please send me the latest version of the document?",
        "The client meeting went well. Here are the key takeaways.",
        "Your order has been shipped. Expected delivery in 3-5 days.",
        "Happy birthday! Hope you have a wonderful day.",
        "Can you review this code before I submit the pull request?",
        "The conference call has been rescheduled to next week.",
        "Please find attached the invoice for this month.",
        "Great work on the project! The client is very happy.",
        "Lunch tomorrow at the usual place? Let me know.",
        "The meeting notes from yesterday are now available.",
        "Thanks for attending the workshop. Here are the resources."
    ]
    
    emails = spam_emails + ham_emails
    labels = [1] * len(spam_emails) + [0] * len(ham_emails)
    
    return emails, labels


def display_header():
    """Display application header"""
    console.clear()
    
    header = """
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║          SPAM EMAIL CLASSIFIER v1.0                  ║
    ║          Machine Learning Powered Detection          ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
    """
    
    console.print(header, style="bold cyan")
    time.sleep(0.3)


def display_result(email, prediction, probability):
    """Display classification results"""
    is_spam = prediction == 1
    spam_prob = probability[1] * 100
    ham_prob = probability[0] * 100
    
    result_color = "red" if is_spam else "green"
    result_text = "SPAM" if is_spam else "LEGITIMATE"
    confidence = spam_prob if is_spam else ham_prob
    
    console.print()
    console.print(Panel(
        f"[bold]Email Text:[/]\n{email[:200]}{'...' if len(email) > 200 else ''}",
        title="Input",
        border_style="blue"
    ))
    
    console.print()
    
    result_panel = f"""
[bold]Classification:[/] [{result_color}]{result_text}[/]
[bold]Confidence:[/] {confidence:.2f}%

[dim]Probability Breakdown:[/]
  Spam: {spam_prob:.2f}%
  Legitimate: {ham_prob:.2f}%
    """
    
    console.print(Panel(
        result_panel.strip(),
        title="Analysis Result",
        border_style=result_color,
        box=box.DOUBLE
    ))
    
    console.print()


def display_menu():
    """Display main menu options"""
    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
    table.add_column("Option", style="cyan")
    table.add_column("Description", style="white")
    
    table.add_row("1", "Classify an email")
    table.add_row("2", "Train new model")
    table.add_row("3", "About this tool")
    table.add_row("4", "Exit")
    
    console.print()
    console.print(table)
    console.print()


def show_about():
    """Display information about the tool"""
    about_text = """
[bold cyan]Spam Email Classifier[/]

This tool uses machine learning to detect spam emails with high accuracy.

[bold]How it works:[/]
1. Emails are converted to numerical features using TF-IDF
2. A Naive Bayes classifier analyzes these features
3. The model outputs spam probability and classification

[bold]Features:[/]
- Real-time email classification
- Confidence scores for predictions
- Pre-trained model included
- Option to train custom models

[bold]Tech Stack:[/]
- scikit-learn for ML algorithms
- TF-IDF for text vectorization
- Naive Bayes for classification
- Rich library for CLI interface

[dim]Developed for educational purposes[/]
    """
    
    console.print(Panel(
        about_text.strip(),
        title="About",
        border_style="magenta"
    ))
    console.print()


def main():
    """Main application loop"""
    display_header()
    
    classifier = SpamClassifier()
    
    console.print(Panel(
        "[cyan]Welcome to Spam Email Classifier[/]\n\n"
        "This tool helps you identify spam emails using machine learning.\n"
        "Loading pre-trained model...",
        border_style="blue"
    ))
    console.print()
    
    # Try to load existing model, otherwise train a new one
    if not classifier.load_model():
        console.print("[yellow]Training new model with sample data...[/]")
        emails, labels = create_sample_dataset()
        classifier.train(emails, labels)
        classifier.save_model()
    
    console.print()
    
    while True:
        display_menu()
        
        choice = Prompt.ask(
            "[bold cyan]Select an option[/]",
            choices=["1", "2", "3", "4"],
            default="1"
        )
        
        if choice == "1":
            console.print()
            email_text = Prompt.ask("[bold green]Enter email text to classify[/]")
            
            if not email_text.strip():
                console.print("[red]Please enter valid email text[/]")
                continue
            
            try:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[cyan]Analyzing email..."),
                    console=console
                ) as progress:
                    progress.add_task("analyze", total=None)
                    time.sleep(0.8)
                    prediction, probability = classifier.predict(email_text)
                
                display_result(email_text, prediction, probability)
                
            except Exception as e:
                console.print(f"[red]Error: {str(e)}[/]")
            
            console.print()
            Prompt.ask("[dim]Press Enter to continue[/]", default="")
        
        elif choice == "2":
            console.print()
            console.print("[yellow]Training with sample dataset...[/]")
            emails, labels = create_sample_dataset()
            classifier.train(emails, labels)
            classifier.save_model()
            console.print()
            Prompt.ask("[dim]Press Enter to continue[/]", default="")
        
        elif choice == "3":
            console.print()
            show_about()
            Prompt.ask("[dim]Press Enter to continue[/]", default="")
        
        elif choice == "4":
            console.print()
            console.print("[cyan]Thank you for using Spam Email Classifier. Developed by Madhan Kumar R[/]")
            console.print()
            break
        
        console.clear()
        display_header()


if __name__ == "__main__":
    main()