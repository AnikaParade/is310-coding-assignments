"""
Fairy-Tale Retellings Data Entry CLI
Collects and saves cultural data about fairy-tale adaptations.
"""

import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()
DATA_FILE = Path(__file__).with_name("fairy_tale_data.json")

EXAMPLE_RECORDS = [
    {
        "title": "Cinderella",
        "original_tale": "Cinderella",
        "creator": "Charles Perrault",
        "year": "1697",
        "medium": "Literary fairy tale",
        "protagonist_agency": "Limited",
        "gender_representation": "Rewards beauty and patience",
        "setting_change": "Royal court",
        "moral_message": "Good behavior is rewarded",
        "adaptation_notes": "A literary version that emphasizes manners and virtue."
    },
    {
        "title": "The Bloody Chamber",
        "original_tale": "Bluebeard",
        "creator": "Angela Carter",
        "year": "1979",
        "medium": "Short story",
        "protagonist_agency": "Growing agency",
        "gender_representation": "Questions patriarchal power",
        "setting_change": "Gothic, wealthy household",
        "moral_message": "Suspicion and independence can be protective",
        "adaptation_notes": "A feminist retelling that revises the original power dynamics."
    }
]

FIELDS = [
    ("title", "Title of the retelling"),
    ("original_tale", "Original fairy tale"),
    ("creator", "Author/creator"),
    ("year", "Publication/release year"),
    ("medium", "Medium (book, film, comic, game, etc.)"),
    ("protagonist_agency", "Protagonist agency (how much control do they have?)"),
    ("gender_representation", "How are gender roles represented?"),
    ("setting_change", "How has the setting changed?"),
    ("moral_message", "What moral/message does the retelling convey?"),
    ("adaptation_notes", "Your interpretation/notes"),
]


def load_records():
    """Load previously saved records, if the JSON file exists."""
    if DATA_FILE.exists():
        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, list):
                return data
            console.print("[yellow]Existing data file was not a list; starting with examples.[/yellow]")
        except (json.JSONDecodeError, OSError) as error:
            console.print(f"[yellow]Could not read saved data ({error}); starting with examples.[/yellow]")
    return [record.copy() for record in EXAMPLE_RECORDS]


def display_records(records, heading="Current fairy-tale data"):
    """Display records in a formatted Rich table."""
    table = Table(title=heading, show_lines=True)
    table.add_column("Title", style="magenta")
    table.add_column("Original tale", style="cyan")
    table.add_column("Creator")
    table.add_column("Year", justify="right")
    table.add_column("Medium")
    for record in records:
        table.add_row(
            record.get("title", ""),
            record.get("original_tale", ""),
            record.get("creator", ""),
            record.get("year", ""),
            record.get("medium", ""),
        )
    console.print(table)


def collect_record():
    """Ask the user to enter one complete record."""
    record = {}
    console.print("\n[bold cyan]Enter a fairy-tale retelling record.[/bold cyan]")
    for field, prompt in FIELDS:
        while True:
            answer = console.input(f"[bold]{prompt}:[/bold] ").strip()
            if answer:
                record[field] = answer
                break
            console.print("[red]This field is required. Please enter a value.[/red]")
    return record


def confirm_record(record):
    """Show all entered fields and ask the user to confirm or retry."""
    while True:
        table = Table(title="Review your entry", show_lines=True)
        table.add_column("Field", style="cyan")
        table.add_column("Your entry", style="white")
        for field, _ in FIELDS:
            table.add_row(field.replace("_", " ").title(), record[field])
        console.print(table)
        choice = console.input("Is this correct? [y]es / [n]o, re-enter: ").strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        console.print("[yellow]Please type y or n.[/yellow]")


def save_records(records):
    """Save records as readable JSON."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2, ensure_ascii=False)


def main():
    console.print("[bold green]Fairy-Tale Retellings Data Curator[/bold green]")
    records = load_records()
    display_records(records)

    while True:
        record = collect_record()
        if confirm_record(record):
            records.append(record)
            save_records(records)
            console.print(f"[green]Confirmed record saved.[/green] Total records: {len(records)}")
        else:
            console.print("[yellow]Let's enter that record again.[/yellow]")
            continue

        more = console.input("Would you like to add another record? [y/n]: ").strip().lower()
        if more not in ("y", "yes"):
            break

    console.print("\n[bold green]Finished![/bold green]")
    console.print(f"Data file location: [underline]{DATA_FILE.resolve()}[/underline]")
    console.print(f"Total records in file: {len(records)}")


if __name__ == "__main__":
    main()
