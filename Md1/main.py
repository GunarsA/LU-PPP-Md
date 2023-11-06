import os
import json

from rich.console import Console
from rich.prompt import Prompt, IntPrompt, FloatPrompt
from rich.table import Table


class Warehouse:
    def __init__(self, inventory):
        self._inventory = inventory

    def _create_book(self, book):
        if book["ISBN"] in self._inventory:
            return False
        else:
            self._inventory[book["ISBN"]] = book
            return True

    def _read_book(self, ISBN):
        if ISBN in self._inventory:
            return self._inventory[ISBN]
        else:
            return None

    def _read_books(self, title="", author=""):
        if title and author:
            return [book for book in self._inventory.values() if title in book["title"] and author in book["author"]]
        elif title:
            return [book for book in self._inventory.values() if title in book["title"]]
        elif author:
            return [book for book in self._inventory.values() if author in book["author"]]
        else:
            return self._inventory.values()

    def _update_book(self, book):
        if book["ISBN"] in self._inventory:
            self._inventory[book["ISBN"]] = book
            return True
        else:
            return False

    def _delete_book(self, ISBN):
        if ISBN in self._inventory:
            del self._inventory[ISBN]
            return True
        else:
            return False

    def add_book(self):
        book = {}
        book["title"] = Prompt.ask(
            "Enter book title: ", default="Pride and Prejudice")
        book["author"] = Prompt.ask(
            "Enter book author: ", default="Jane Austen")
        book["ISBN"] = IntPrompt.ask("Enter book ISBN: ", default="0684801221")
        book["price"] = FloatPrompt.ask("Enter book price: ", default="5.99")
        book["quantity"] = IntPrompt.ask(
            "Enter book quantity: ", default="100")

        if self._create_book(book):
            console.print(f"Book [bold green] {
                          book['title']} [/bold green] added to inventory")
        else:
            console.print(f"Book [bold red] {
                          book['title']} [/bold red] already exists in inventory")
            choice = Prompt.ask(
                "Do you want to update the book? (y/n): ", choices=["y", "n"])
            if choice == "y":
                self._update_book(book)
                console.print(f"Book [bold green] {
                              book['title']} [/bold green] updated in inventory")
            else:
                console.print(f"Book [bold red] {
                              book['title']} [/bold red] not updated in inventory")

    def remove_book(self):
        ISBN = IntPrompt.ask("Enter book ISBN: ", default="0684801221")
        if self._delete_book(ISBN):
            console.print(f"Book with ISBN [bold green] {
                          ISBN} [/bold green] removed from inventory")
        else:
            console.print(f"Book with ISBN [bold red] {
                          ISBN} [/bold red] does not exist in inventory")

    def search_book(self):
        ISBN = IntPrompt.ask("Enter book ISBN: ", default="0684801221")
        book = self._read_book(ISBN)
        if book:
            console.print(book)
        else:
            console.print(f"Book with ISBN [bold red] {
                          ISBN} [/bold red] does not exist in inventory")

    def search_books(self):
        title = Prompt.ask("Enter book title: ", default="")
        author = Prompt.ask("Enter book author: ", default="")
        books = self._read_books(title, author)
        if books:
            for book in books:
                console.print(book)
        else:
            console.print(f"Book with title [bold red] {
                          title} [/bold red] and author [bold red] {author} [/bold red] does not exist in inventory")

    def print_inventory(self):
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

    file_path = os.path.join(os.path.dirname(__file__), "data.json")
    with open(file_path, "r") as f:
        inventory = json.load(f)

    warehouse = Warehouse(inventory)

    while True:
        # Clear screen
        console.clear()

        # make pretty menu using rich
        console.print("Book Warehouse", style="bold underline green")

        menu = Table(title="Menu")
        menu.add_column("Option", justify="right", style="cyan", no_wrap=True)
        menu.add_column("Description", style="magenta")

        menu.add_row("1", "Add book")
        menu.add_row("2", "Remove book")
        menu.add_row("3", "Search book by ISBN")
        menu.add_row("4", "Search books by title and/or author")
        menu.add_row("5", "Print inventory")
        menu.add_row("6", "Exit")

        console.print(menu)

        choice = input("Enter your choice: ")

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
        "Do you want to save the inventory? (y/n): ", choices=["y", "n"])
    if choice == "y":
        with open("data.json", "w") as f:
            json.dump(inventory, f)
        console.print("[bold green]Inventory saved![/bold green]")
    else:
        console.print("[bold red]Inventory not saved![/bold red]")
