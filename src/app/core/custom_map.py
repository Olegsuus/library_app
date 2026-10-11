from typing import Any, Iterator


class CustomMap:


    def __init__(self) -> None:
        self._keys: list = []
        self._values: list = []

    def _index_of(self, key: Any) -> int:
        for index, existing in enumerate(self._keys):
            if existing == key:
                return index
        return -1

    def get(self, key: Any, default: Any = None) -> Any:
        index = self._index_of(key)
        return self._values[index] if index >= 0 else default

    def keys(self) -> list:
        return list(self._keys)

    def values(self) -> list:
        return list(self._values)

    def items(self) -> list:
        return list(zip(self._keys, self._values))

    def clear(self) -> None:
        self._keys.clear()
        self._values.clear()


    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._index_of(key)
        if index >= 0:
            self._values[index] = value
        else:
            self._keys.append(key)
            self._values.append(value)

    def __getitem__(self, key: Any) -> Any:
        index = self._index_of(key)
        if index < 0:
            raise KeyError(key)
        return self._values[index]

    def __delitem__(self, key: Any) -> None:
        index = self._index_of(key)
        if index < 0:
            raise KeyError(key)
        del self._keys[index]
        del self._values[index]

    def __contains__(self, key: Any) -> bool:
        return self._index_of(key) >= 0

    def __len__(self) -> int:
        return len(self._keys)

    def __iter__(self) -> Iterator:
        return iter(list(self._keys))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CustomMap):
            return NotImplemented
        return len(self) == len(other) and all(
            key in other and other[key] == value for key, value in self.items()
        )

    def __repr__(self) -> str:
        pairs = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"CustomMap({pairs})"

    def __str__(self) -> str:
        return f"CustomMap с {len(self)} элементами"
