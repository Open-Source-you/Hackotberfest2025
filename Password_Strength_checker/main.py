
"""
A modular CLI tool that evaluates password strength and provides
detailed feedback with improvement recommendations.

Author:Madhan Kumar R
Date: 15 October 2025

"""

import getpass
import re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def check_length(password: str) -> tuple[bool, int]:
    """
    Check password length and return status with points.
    
    Args:
        password: The password to check
        
    Returns:
        Tuple of (meets_requirement, points_awarded)
    """
    length = len(password)
    if length >= 12:
        return True, 3
    elif length >= 8:
        return True, 2
    elif length >= 6:
        return True, 1
    else:
        return False, 0


def check_lowercase(password: str) -> tuple[bool, int]:
    """
    Check for lowercase letters.
    
    Args:
        password: The password to check
        
    Returns:
        Tuple of (has_lowercase, points_awarded)
    """
    has_lower = bool(re.search(r'[a-z]', password))
    return has_lower, 1 if has_lower else 0


def check_uppercase(password: str) -> tuple[bool, int]:
    """
    Check for uppercase letters.
    
    Args:
        password: The password to check
        
    Returns:
        Tuple of (has_uppercase, points_awarded)
    """
    has_upper = bool(re.search(r'[A-Z]', password))
    return has_upper, 2 if has_upper else 0


def check_digits(password: str) -> tuple[bool, int]:
    """
    Check for numeric digits.
    
    Args:
        password: The password to check
        
    Returns:
        Tuple of (has_digits, points_awarded)
    """
    has_digit = bool(re.search(r'\d', password))
    return has_digit, 2 if has_digit else 0


def check_symbols(password: str) -> tuple[bool, int]:
    """
    Check for special symbols.
    
    Args:
        password: The password to check
        
    Returns:
        Tuple of (has_symbols, points_awarded)
    """
    has_symbol = bool(re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;~`]', password))
    return has_symbol, 2 if has_symbol else 0


def evaluate_strength(password: str) -> int:
    """
    Evaluate password strength on a 0-10 scale.
    
    Args:
        password: The password to evaluate
        
    Returns:
        Integer score from 0 to 10
    """
    if not password:
        return 0
    
    # Check all criteria and sum points
    _, length_points = check_length(password)
    _, lower_points = check_lowercase(password)
    _, upper_points = check_uppercase(password)
    _, digit_points = check_digits(password)
    _, symbol_points = check_symbols(password)
    
    total_points = length_points + lower_points + upper_points + digit_points + symbol_points
    
    # Max possible points is 10 (3+1+2+2+2)
    return min(total_points, 10)


def get_feedback(score: int) -> str:
    """
    Provide feedback message based on password score.
    
    Args:
        score: Password strength score (0-10)
        
    Returns:
        Feedback string with assessment
    """
    if score >= 9:
        return "Excellent! Your password is very strong."
    elif score >= 7:
        return "Good! Your password is strong, but could be improved slightly."
    elif score >= 5:
        return "Fair. Your password is moderate but could use improvement."
    elif score >= 3:
        return "Weak. Your password needs significant improvement."
    else:
        return "Very weak. Your password is vulnerable and should be strengthened."


def get_improvement_tips(password: str, score: int) -> list[str]:
    """
    Generate specific improvement tips based on password weaknesses.
    
    Args:
        password: The password to analyze
        score: Current password score
        
    Returns:
        List of improvement tip strings
    """
    tips = []
    
    # Check each criterion
    has_length, _ = check_length(password)
    has_lower, _ = check_lowercase(password)
    has_upper, _ = check_uppercase(password)
    has_digit, _ = check_digits(password)
    has_symbol, _ = check_symbols(password)
    
    if not has_length or len(password) < 12:
        tips.append("Increase length to at least 12 characters for better security")
    
    if not has_lower:
        tips.append("Add lowercase letters (a-z)")
    
    if not has_upper:
        tips.append("Add uppercase letters (A-Z)")
    
    if not has_digit:
        tips.append("Include numeric digits (0-9)")
    
    if not has_symbol:
        tips.append("Include special symbols (!@#$%^&* etc.)")
    
    if score < 7 and len(tips) == 0:
        tips.append("Consider making your password even longer for maximum security")
    
    return tips


def display_report(password: str, score: int):
    """
    Display a detailed strength report using rich formatting.
    
    Args:
        password: The password that was evaluated
        score: The strength score
    """
    # Create criteria table
    table = Table(title="Password Analysis", show_header=True, header_style="bold cyan")
    table.add_column("Criterion", style="white", width=20)
    table.add_column("Status", style="white", width=10)
    table.add_column("Details", style="white")
    
    # Check all criteria
    has_length, length_points = check_length(password)
    has_lower, _ = check_lowercase(password)
    has_upper, _ = check_uppercase(password)
    has_digit, _ = check_digits(password)
    has_symbol, _ = check_symbols(password)
    
    # Add rows with color-coded status
    length_status = "[green]Pass[/green]" if has_length else "[red]Fail[/red]"
    table.add_row("Length", length_status, f"{len(password)} characters")
    
    lower_status = "[green]Pass[/green]" if has_lower else "[red]Fail[/red]"
    table.add_row("Lowercase Letters", lower_status, "Contains a-z" if has_lower else "Missing")
    
    upper_status = "[green]Pass[/green]" if has_upper else "[red]Fail[/red]"
    table.add_row("Uppercase Letters", upper_status, "Contains A-Z" if has_upper else "Missing")
    
    digit_status = "[green]Pass[/green]" if has_digit else "[red]Fail[/red]"
    table.add_row("Digits", digit_status, "Contains 0-9" if has_digit else "Missing")
    
    symbol_status = "[green]Pass[/green]" if has_symbol else "[red]Fail[/red]"
    table.add_row("Special Symbols", symbol_status, "Contains symbols" if has_symbol else "Missing")
    
    console.print()
    console.print(table)
    
    # Display score with color
    console.print()
    if score >= 7:
        score_color = "green"
    elif score >= 5:
        score_color = "yellow"
    else:
        score_color = "red"
    
    console.print(f"[bold]Strength Score:[/bold] [{score_color}]{score}/10[/{score_color}]")
    
    # Display feedback
    feedback = get_feedback(score)
    console.print(f"[bold]Assessment:[/bold] {feedback}")
    
    # Display improvement tips if needed
    if score < 9:
        tips = get_improvement_tips(password, score)
        if tips:
            console.print()
            console.print("[bold yellow]Improvement Tips:[/bold yellow]")
            for tip in tips:
                console.print(f"  - {tip}")


def main():
    """
    Main program entry point.
    """
    # Welcome message
    console.print()
    console.print(Panel.fit(
        "[bold cyan]Password Strength Checker[/bold cyan]\n"
        "Evaluate your password security and get improvement tips",
        border_style="cyan"
    ))
    console.print()
    
    try:
        # Get password input without echo
        password = getpass.getpass("Enter password to check ( No worries others cannot see them ): ")
        
        if not password:
            console.print("[red]Error: Password cannot be empty[/red]")
            return
        
        # Evaluate password
        score = evaluate_strength(password)
        
        # Display report
        display_report(password, score)
        
        # Exit message
        console.print()
        console.print("[dim]Thank you for using Password Strength Checker[/dim]")
        console.print()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"[red]An error occurred: {e}[/red]")


if __name__ == "__main__":
    main()