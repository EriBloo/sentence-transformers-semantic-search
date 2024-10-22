from typing import TypeVar

T = TypeVar('T')

def pluck(lst: list[dict[str, T]], key: str) -> list[T]:
  return [x.get(key) for x in lst]