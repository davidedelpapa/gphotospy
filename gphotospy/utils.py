from typing import Iterator


def batches(lst: list, n: int) -> Iterator[list]:
    """
    split list into chunks in size n
    taken from: https://stackoverflow.com/a/312464/8953378
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
