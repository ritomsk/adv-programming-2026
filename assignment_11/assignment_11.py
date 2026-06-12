from abc import ABC, abstractmethod

class LibraryItem(ABC):
    total_items = 0

    def __init__(self, title: str, year: int):
        self.title = title
        self.year = year
        LibraryItem.total_items += 1

    @abstractmethod
    def display_info(self):
        pass

    @classmethod
    def get_total_items(cls):
        return cls.total_items


class Book(LibraryItem):
    def __init__(self, title: str, year: int, author: str):
        super().__init__(title, year)
        self.author = author

    def display_info(self):
        return f"[Book] '{self.title}' by {self.author} ({self.year})"

class DVD(LibraryItem):
    def __init__(self, title: str, year: int, duration: int, genre: str):
        super().__init__(title, year)
        self.duration = duration
        self.genre = genre

    def display_info(self):
        return f"[DVD] '{self.title}' - {self.genre}, {self.duration} mins ({self.year})"

if __name__ == "__main__":
    catalog = [
        Book("The Hobbit", 1937, "J.R.R. Tolkien"),
        DVD("The Matrix", 1999, 136, "Sci-Fi"),
        Book("1984", 1949, "George Orwell"),
        DVD("Inception", 2010, 148, "Sci-Fi/Action")
    ]

    print("--- Library Inventory ---")
    
    for item in catalog:
        print(item.display_info())

    print("\n--- Library Statistics ---")
    print(f"Total items in library: {LibraryItem.get_total_items()}")