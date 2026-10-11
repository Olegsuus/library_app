from typing import Iterator

from app.core.custom_map import CustomMap
from app.models import Book, Reader


class Library:
    SORT_MODES = (
        ("По названию", Book.key_title),
        ("По автору", Book.key_author),
        ("По году", Book.key_year),
    )
    ALL_GENRES = "Все жанры"

    def __init__(self) -> None:
        self._books: list[Book] = []
        self._readers: list[Reader] = []
        self._genres: set[str] = set()
        self._book_index = CustomMap()     # id -> Book
        self._reader_index = CustomMap()   # id -> Reader

    @property
    def books(self) -> tuple:
        return tuple(self._books)

    @property
    def readers(self) -> tuple:
        return tuple(sorted(self._readers))

    @property
    def genres(self) -> tuple:
        return tuple(sorted(self._genres))

    def add_book(self, book: Book) -> Book:
        if book in self._books:
            raise ValueError(f"Книга {book} уже есть в каталоге")
        self._books.append(book)
        self._book_index[book.id] = book
        self._genres.add(book.genre)
        return book

    def update_book(self, book_id: int, title: str, author: str, year: int, genre: str) -> Book:
        book = self.get_book(book_id)
        book.title, book.author, book.year, book.genre = title, author, year, genre
        self._rebuild_genres()
        return book

    def remove_book(self, book_id: int) -> Book:
        book = self.get_book(book_id)
        if not book.is_available:
            raise ValueError("Нельзя удалить выданную книгу — сначала верните её")
        self._books.remove(book)
        del self._book_index[book_id]
        self._rebuild_genres()
        return book

    def get_book(self, book_id: int) -> Book:
        if book_id not in self._book_index:
            raise ValueError(f"Книга с id={book_id} не найдена")
        return self._book_index[book_id]

    def filter_books(self, query: str = "", genre: str = ALL_GENRES,
                     only_available: bool = False, sort_index: int = 0) -> list[Book]:
        result = [
            book for book in self._books
            if (not query or book.matches(query))
            and (genre == Library.ALL_GENRES or book.genre == genre)
            and (not only_available or book)
        ]
        key = Library.SORT_MODES[sort_index][1]
        return sorted(result, key=key)

    def _rebuild_genres(self) -> None:
        self._genres = {book.genre for book in self._books}

    def add_reader(self, reader: Reader) -> Reader:
        if any(r.name.lower() == reader.name.lower() for r in self._readers):
            raise ValueError(f"Читатель «{reader.name}» уже зарегистрирован")
        self._readers.append(reader)
        self._reader_index[reader.id] = reader
        return reader

    def remove_reader(self, reader_id: int) -> Reader:
        reader = self.get_reader(reader_id)
        if len(reader):
            raise ValueError("У читателя есть книги на руках")
        self._readers.remove(reader)
        del self._reader_index[reader_id]
        return reader

    def get_reader(self, reader_id: int) -> Reader:
        if reader_id not in self._reader_index:
            raise ValueError(f"Читатель с id={reader_id} не найден")
        return self._reader_index[reader_id]

    def books_of(self, reader: Reader) -> list[Book]:
        return sorted(self.get_book(book_id) for book_id in reader)


    def issue(self, book_id: int, reader_id: int) -> None:
        book, reader = self.get_book(book_id), self.get_reader(reader_id)
        book.issue_to(reader.id)
        reader.take(book.id)

    def give_back(self, book_id: int) -> Reader:
        book = self.get_book(book_id)
        if book.reader_id is None:
            raise ValueError(f"Книга {book.display_name} уже в библиотеке")
        reader = self.get_reader(book.reader_id)
        book.give_back()
        reader.release(book.id)
        return reader

    def stats(self) -> tuple:
        issued = sum(1 for book in self._books if not book)
        return len(self._books), issued, len(self._readers)


    def __len__(self) -> int:
        return len(self._books)

    def __iter__(self) -> Iterator[Book]:
        return iter(tuple(self._books))

    def __contains__(self, item: object) -> bool:
        return item in self._books or item in self._readers

    def __repr__(self) -> str:
        return f"Library(books={len(self._books)}, readers={len(self._readers)})"

    def __str__(self) -> str:
        total, issued, readers = self.stats()
        return f"Книг: {total} (выдано {issued}) · Читателей: {readers}"
