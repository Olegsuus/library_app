from datetime import date

from .entity import Entity


class Book(Entity):
    MIN_YEAR = 1450

    def __init__(self, title: str, author: str, year: int, genre: str,
                 entity_id: int | None = None) -> None:
        super().__init__(entity_id)
        self._title = ""
        self._author = ""
        self._year = Book.MIN_YEAR
        self._genre = ""
        self._reader_id: int | None = None
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre


    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        value = str(value).strip()
        if not value:
            raise ValueError("Название книги не может быть пустым")
        self._title = value

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value: str) -> None:
        value = str(value).strip()
        if not value:
            raise ValueError("Автор не может быть пустым")
        self._author = value

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, value: int) -> None:
        value = int(value)
        if not Book.MIN_YEAR <= value <= date.today().year:
            raise ValueError(f"Год должен быть от {Book.MIN_YEAR} до {date.today().year}")
        self._year = value

    @property
    def genre(self) -> str:
        return self._genre

    @genre.setter
    def genre(self, value: str) -> None:
        value = str(value).strip()
        if not value:
            raise ValueError("Жанр не может быть пустым")
        self._genre = value

    @property
    def reader_id(self) -> int | None:
        return self._reader_id

    @property
    def is_available(self) -> bool:
        return self._reader_id is None


    def issue_to(self, reader_id: int) -> None:
        if not self.is_available:
            raise ValueError(f"Книга {self} уже выдана")
        self._reader_id = reader_id

    def give_back(self) -> None:
        if self.is_available:
            raise ValueError(f"Книга {self} и так в библиотеке")
        self._reader_id = None

    def matches(self, query: str) -> bool:
        return query in self


    @staticmethod
    def key_title(book: "Book") -> tuple:
        return book.title.lower(), book.author.lower()

    @staticmethod
    def key_author(book: "Book") -> tuple:
        return book.author.lower(), book.title.lower()

    @staticmethod
    def key_year(book: "Book") -> tuple:
        return book.year, book.title.lower()


    @property
    def display_name(self) -> str:
        return f"«{self._title}»"

    def sort_key(self) -> tuple:
        return Book.key_title(self)

    def to_row(self) -> tuple:
        status = "в наличии" if self.is_available else "выдана"
        return str(self.id), self._title, self._author, str(self._year), self._genre, status

    @staticmethod
    def headers() -> tuple:
        return "ID", "Название", "Автор", "Год", "Жанр", "Статус"


    def __contains__(self, query: str) -> bool:
        query = str(query).strip().lower()
        return query in self._title.lower() or query in self._author.lower()

    def __bool__(self) -> bool:
        return self.is_available

    def __str__(self) -> str:
        return f"«{self._title}» — {self._author} ({self._year})"

    def __repr__(self) -> str:
        return (f"Book(id={self.id}, title={self._title!r}, author={self._author!r}, "
                f"year={self._year}, genre={self._genre!r}, reader_id={self._reader_id})")
