"""
QR Code Generator with Terminal Display

A command-line tool for generating and displaying QR codes directly in the terminal
using Unicode block characters for high-quality output. 

Author: Madhan Kumar R
Date: 15 October 2025
"""

import os
import shutil
import sys
import time
from typing import Optional
from urllib.parse import urlparse

import qrcode
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner

# Initialize Rich Console for better terminal output
console = Console()

# Available colors for QR code display
AVAILABLE_COLORS = [
    "cyan",
    "green",
    "blue",
    "magenta",
    "yellow",
    "red",
    "white",
    "bright_cyan",
    "bright_green",
    "bright_blue",
    "bright_magenta",
    "bright_yellow",
    "bright_red",
]


def is_valid_url(url: str) -> bool:
    """
    Check if the given string is a valid URL.

    Args:
        url: String to validate as URL

    Returns:
        bool: True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def generate_qr(url: str, filename: str) -> None:
    """
    Generate a QR code for the given URL and save it as an image file.

    Args:
        url: URL to encode in QR code
        filename: Output filename for the QR code image

    Raises:
        Exception: If QR code generation or saving fails
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    console.print(f"[green]QR code saved as {filename}[/green]")


def display_qr_terminal_unicode(url: str) -> None:
    """
    Display QR code directly in terminal using Unicode block characters.

    This provides the best quality terminal display without external tools.
    Uses half-block characters for better resolution.

    Args:
        url: URL to encode and display as QR code
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    matrix = qr.get_matrix()

    console.print("\n[bold green]QR Code (scan with your phone):[/bold green]")

    # Unicode half-block characters for better resolution
    for i in range(0, len(matrix), 2):
        line = ""
        for j in range(len(matrix[0])):
            top = matrix[i][j] if i < len(matrix) else False
            bottom = matrix[i + 1][j] if i + 1 < len(matrix) else False

            if top and bottom:
                line += "█"  # Full block
            elif top and not bottom:
                line += "▀"  # Upper half block
            elif not top and bottom:
                line += "▄"  # Lower half block
            else:
                line += " "  # Empty

        console.print(line)

    console.print()


def display_qr_simple_blocks(url: str) -> None:
    """
    Display QR code using simple full blocks.

    Compatibility mode for terminals that don't support half-blocks well.

    Args:
        url: URL to encode and display as QR code
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    matrix = qr.get_matrix()

    console.print("\n[bold green]QR Code (simple blocks):[/bold green]")

    for row in matrix:
        line = ""
        for cell in row:
            line += "██" if cell else "  "  # Double-width for square appearance
        console.print(line)

    console.print()


def display_qr_colored(url: str, color: str = "cyan") -> None:
    """
    Display QR code with colored blocks for visual appeal.

    Args:
        url: URL to encode and display as QR code
        color: Color name for the QR code (default: cyan)
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    matrix = qr.get_matrix()

    console.print(f"\n[bold green]QR Code ({color}):[/bold green]")

    for i in range(0, len(matrix), 2):
        line = ""
        for j in range(len(matrix[0])):
            top = matrix[i][j] if i < len(matrix) else False
            bottom = matrix[i + 1][j] if i + 1 < len(matrix) else False

            if top and bottom:
                line += "█"
            elif top and not bottom:
                line += "▀"
            elif not top and bottom:
                line += "▄"
            else:
                line += " "

        console.print(line, style=f"bold {color}")

    console.print()


def choose_color() -> str:
    """
    Prompt user to choose a color from available options.

    Returns:
        str: Selected color name
    """
    console.print("\n[bold]Available Colors:[/bold]")
    for i, color in enumerate(AVAILABLE_COLORS, 1):
        console.print(f"  {i}. {color}", style=color)

    while True:
        try:
            choice = console.input(
                f"\nChoose a color (1-{len(AVAILABLE_COLORS)}): "
            ).strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(AVAILABLE_COLORS):
                return AVAILABLE_COLORS[choice_num - 1]
            console.print(
                f"[red]Please enter a number between 1 and {len(AVAILABLE_COLORS)}[/red]"
            )
        except ValueError:
            console.print("[red]Please enter a valid number[/red]")


def save_qr_to_file(generated_filename: str, temp_qr_filename: str) -> Optional[str]:
    """
    Save QR code to a custom filename.

    Args:
        generated_filename: Current filename of the generated QR
        temp_qr_filename: Temporary filename to track

    Returns:
        Optional[str]: New filename if successful, None otherwise
    """
    custom_filename = console.input("Enter desired filename (e.g., my_qr.png): ").strip()
    if not custom_filename.lower().endswith(".png"):
        custom_filename += ".png"

    try:
        if os.path.exists(generated_filename):
            shutil.move(generated_filename, custom_filename)
            console.print(f"[green]QR code successfully saved as {custom_filename}[/green]")
            return custom_filename if generated_filename == temp_qr_filename else generated_filename
        console.print("[red]Temporary QR code file not found for saving.[/red]")
        return None
    except OSError as e:
        console.print(f"[red]Error saving file: {e}[/red]")
        return None


def cleanup_temp_file(filename: str, temp_filename: str) -> None:
    """
    Clean up temporary QR code file if it exists.

    Args:
        filename: Current filename
        temp_filename: Temporary filename to check and remove
    """
    if os.path.exists(temp_filename) and filename == temp_filename:
        os.remove(temp_filename)


def main() -> None:
    """Run the QR code generator program."""
    console.print("[bold green]Welcome to the QR Code Generator![/bold green]")
    console.print("[blue]----------------------------------[/blue]")

    while True:
        url_input = console.input("\nEnter a URL to generate a QR code for: ").strip()

        if not is_valid_url(url_input):
            console.print(
                "[red]Invalid URL. Please enter a valid URL (e.g., https://example.com).[/red]"
            )
            continue

        generated_filename: Optional[str] = None
        temp_qr_filename = "temp_qr_code.png"

        # Animated loading effect
        with Live(
            Spinner("dots", text="[yellow]Generating QR code...[/yellow]"),
            refresh_per_second=8,
            console=console,
        ):
            time.sleep(1)
            try:
                generate_qr(url_input, temp_qr_filename)
                generated_filename = temp_qr_filename
            except Exception as e:
                console.print(f"[red]Error generating QR code: {e}[/red]")

        if not generated_filename:
            console.print("[red]QR code generation failed. Please try again.[/red]")
            cleanup_temp_file(temp_qr_filename, temp_qr_filename)
            continue

        while True:
            console.print("\n[blue]Options:[/blue]")
            console.print("  [cyan]1[/]. View QR (Unicode - Best Quality)")
            console.print("  [cyan]2[/]. View QR (Simple Blocks)")
            console.print("  [cyan]3[/]. View QR (Colored)")
            console.print("  [cyan]4[/]. Save QR code to a custom file")
            console.print("  [cyan]5[/]. Generate another QR code")
            console.print("  [cyan]6[/]. Exit")

            choice = console.input("Enter your choice (1-6): ").strip()

            if choice == "1":
                display_qr_terminal_unicode(url_input)
            elif choice == "2":
                display_qr_simple_blocks(url_input)
            elif choice == "3":
                selected_color = choose_color()
                display_qr_colored(url_input, selected_color)
            elif choice == "4":
                result = save_qr_to_file(generated_filename, temp_qr_filename)
                if result:
                    generated_filename = result
            elif choice == "5":
                cleanup_temp_file(generated_filename, temp_qr_filename)
                break
            elif choice == "6":
                cleanup_temp_file(generated_filename, temp_qr_filename)
                console.print("\n[bold green]Thanks for using the QR Generator![/bold green]")
                for _ in range(3):
                    console.print(".", end="", style="bold yellow")
                    sys.stdout.flush()
                    time.sleep(0.3)
                console.print("\n")
                sys.exit(0)
            else:
                console.print("[red]Invalid choice. Please enter a number from 1 to 6.[/red]")


if __name__ == "__main__":
    main()