import csv
from typing import Any


def csvToDict(fileName: str) -> list[dict[str, Any]]:
    data: list[dict[str, Any]]
    with open(fileName) as csvFile:
        reader = csv.DictReader(csvFile)
        data = [x for x in reader]
        return data
