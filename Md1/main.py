import os
import json
from time import sleep

from rich.console import Console
from rich.prompt import Prompt, IntPrompt, FloatPrompt
from rich.progress import track
from rich.table import Table


class Warehouse:
    def __init__(self, file_name="data.json"):
        """
        Initializes an instance of Warehouse with the given file name.

        Args: 
            file_name (str): The name of the file to use for storing inventory data.
        """
        self._file_path = os.path.join(os.path.dirname(__file__), file_name)

        if os.path.exists(self._file_path):
            with open(self._file_path, "r") as f:
                self._inventory = json.load(f)
        else:
            self._inventory = {}

    def save(self) -> None:
        """
        Saves the current inventory to a JSON file at the specified file path.
        """
        with open(self._file_path, "w") as f:
            json.dump(self._inventory, f)

    def _create_book(self, book) -> bool:
        """
        Adds a new book to the inventory.

        Args:
            book (dict): A dictionary containing the book's information, including its ISBN.

        Returns:
            bool: True if the book was successfully added to the inventory, False otherwise.
        """
        if book["ISBN"] in self._inventory:
            return False
        else:
            self._inventory[book["ISBN"]] = book
            return True

    def _read_book(self, ISBN) -> dict:
        """
        Returns the book information for a given ISBN.

        Args:
            ISBN (str): The ISBN of the book to retrieve.

        Returns:
            dict: A dictionary containing the book information, or None if the book is not found.
        """
        if ISBN in self._inventory:
            return self._inventory[ISBN]
        else:
            return None

    def _read_books(self, title="", author="") -> list:
        """
        Returns a list of books from the inventory that match the given title and/or author.

        Args:
            title (str): The title of the book to search for (optional).
            author (str): The author of the book to search for (optional).

        Returns:
            list: A list of books that match the given title and/or author.
        """
        if title and author:
            return [book for book in self._inventory.values() if title.lower() in book["title"].lower() and author.lower() in book["author"].lower()]
        elif title:
            return [book for book in self._inventory.values() if title.lower() in book["title"].lower()]
        elif author:
            return [book for book in self._inventory.values() if author.lower() in book["author"].lower()]
        else:
            return list(self._inventory.values())

    def _update_book(self, book) -> bool:
        """
        Updates the inventory with the given book information.

        Args:
            book (dict): A dictionary containing the book information.

        Returns:
            bool: True if the book was successfully updated, False otherwise.
        """
        if book["ISBN"] in self._inventory:
            self._inventory[book["ISBN"]] = book
            return True
        else:
            return False

    def _delete_book(self, ISBN) -> bool:
        """
        Deletes a book from the inventory.

        Args:
            ISBN (str): The ISBN of the book to delete.

        Returns:
            bool: True if the book was deleted, False otherwise.
        """
        if ISBN in self._inventory:
            del self._inventory[ISBN]
            return True
        else:
            return False

    def add_book(self) -> None:
        """
        Prompts the user to enter the book's title, author, ISBN, price, and quantity.
        If the book already exists in the inventory, prompts the user to update the book.
        """
        book = {}

        book["title"] = Prompt.ask(
            "Enter book title", default="Pride and Prejudice")

        book["author"] = Prompt.ask("Enter book author", default="Jane Austen")

        book["ISBN"] = Prompt.ask("Enter book ISBN", default="0684801221")
        while not book["ISBN"].isdigit():
            console.print("[red]ISBN must contain only digits[/red]")
            book["ISBN"] = Prompt.ask("Enter book ISBN", default="0684801221")

        book["price"] = FloatPrompt.ask("Enter book price", default=5.99)
        while book["price"] < 0:
            console.print("[red]Price cannot be negative[/red]")
            book["price"] = FloatPrompt.ask("Enter book price", default="5.99")

        book["quantity"] = IntPrompt.ask("Enter book quantity", default=100)
        while book["quantity"] < 1:
            console.print("[red]Quantity has to be positive[/red]")
            book["quantity"] = IntPrompt.ask(
                "Enter book quantity", default="100")

        if self._create_book(book):
            console.print(f"Book [bold green] {
                          book["title"]} [/bold green] added to inventory")
        else:
            console.print(f"Book with ISBN [bold red] {
                          book['title']} [/bold red] already exists in inventory")

            choice = Prompt.ask(
                "Do you want to update the book?", choices=["y", "n"])

            if choice == "y":
                self._update_book(book)
                console.print(f"Book [bold green] {
                              book['title']} [/bold green] updated in inventory")
            else:
                console.print(f"Book [bold red] {
                              book['title']} [/bold red] not updated in inventory")

    def remove_book(self) -> None:
        """
        Prompts the user to enter the book's ISBN. If the book exists in the inventory,
        it is removed.
        """
        ISBN = Prompt.ask("Enter book ISBN", default="0684801221")
        while not ISBN.isdigit():
            console.print("[red]ISBN must contain only digits[/red]")
            ISBN = Prompt.ask("Enter book ISBN", default="0684801221")

        if self._delete_book(ISBN):
            console.print(f"Book with ISBN [bold green] {
                          ISBN} [/bold green] removed from inventory")
        else:
            console.print(f"Book with ISBN [bold red] {
                          ISBN} [/bold red] does not exist in inventory")

    def search_book(self) -> None:
        """
        Prompts the user to enter a book ISBN and searches for the book in the inventory.
        If the book is found, it is displayed. Otherwise, an error message is displayed.
        """
        ISBN = IntPrompt.ask("Enter book ISBN", default="0684801221")
        while ISBN < 0:
            console.print("[red]ISBN cannot be negative[/red]")
            ISBN = IntPrompt.ask("Enter book ISBN", default="0684801221")

        book = self._read_book(ISBN)
        if book:
            console.print(book)
        else:
            console.print(f"Book with ISBN [bold red] {
                          ISBN} [/bold red] does not exist in inventory")

    def search_books(self) -> None:
        """
        Searches for books in the inventory based on user input for title and author.
        Displays the search results in a formatted table.
        """
        title = Prompt.ask("Enter book title", default="")
        author = Prompt.ask("Enter book author", default="")

        books = self._read_books(title, author)
        # Sort the books by author and title
        books.sort(key=lambda book: (book["author"], book["title"]))

        table = Table(title=f"Search results ({len(books)})")
        table.add_column("ISBN", justify="right", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Author", style="green")
        table.add_column("Price", justify="right", style="yellow")
        table.add_column("Quantity", justify="right", style="red")

        for book in books:
            table.add_row(str(book["ISBN"]), book["title"], book["author"], str(
                book["price"]), str(book["quantity"]))

        # Simulate a long-running search 
        for _ in track(range(100), description="Searching..."):
            sleep(0.01)

        console.print(table)

    def print_inventory(self) -> None:
        """
        Prints the inventory of books in a formatted table.
        """
        table = Table(title="Inventory")
        table.add_column("ISBN", justify="right", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Author", style="green")
        table.add_column("Price", justify="right", style="yellow")
        table.add_column("Quantity", justify="right", style="red")

        for book in self._read_books():
            table.add_row(str(book["ISBN"]), book["title"], book["author"], str(
                book["price"]), str(book["quantity"]))

        console.print(table)


if __name__ == "__main__":
    console = Console()

    warehouse = Warehouse()

    while True:
        console.clear()

        menu = Table(title="Book Warehouse Menu")
        menu.add_column("Option", justify="right", style="cyan", no_wrap=True)
        menu.add_column("Description", style="magenta")

        menu.add_row("1", "Add book")
        menu.add_row("2", "Remove book")
        menu.add_row("3", "Search book by exact ISBN")
        menu.add_row("4", "Search books by title or author")
        menu.add_row("5", "Print inventory")
        menu.add_row("6", "Exit")

        console.print(menu)

        choice = Prompt.ask("Enter option", choices=[
                            "1", "2", "3", "4", "5", "6"])

        if choice == "1":
            warehouse.add_book()
        elif choice == "2":
            warehouse.remove_book()
        elif choice == "3":
            warehouse.search_book()
        elif choice == "4":
            warehouse.search_books()
        elif choice == "5":
            warehouse.print_inventory()
        elif choice == "6":
            break

        Prompt.ask("Press Enter to continue...")

    choice = Prompt.ask(
        "Do you want to save the inventory changes in file?", choices=["y", "n"])
    if choice == "y":
        warehouse.save()
        console.print("[bold green]Inventory saved![/bold green]")
    else:
        console.print("[bold red]Inventory not saved![/bold red]")
