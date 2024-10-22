from typing import TypedDict

class Dataset(TypedDict):
    id: str
    name: str

class Embedding(TypedDict):
    id: str
    embedding: any

class Score(TypedDict):
    id: str
    score: str