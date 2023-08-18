#!/usr/bin/env python3
""" Simple Pagination function """

import csv
import math
from typing import List, Tuple


class Server:
    """Server class to paginate a database of popular baby names
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Simple pagination"""
        assert type(page) is int and page > 0
        assert type(page_size) is int and page_size > 0
        idx = index_range(page, page_size)
        try:
            return self.dataset()[idx[0]:idx[1]]
        except IndexError:
            return []


def index_range(page: int, page_size: int) -> Tuple[int]:
    """return a tuple of size two containing
    a start index and an end index corresponding
    to the range of indexes to return in a list
    for those particular pagination parameters"""
    result = ((page - 1) * page_size, page * page_size)
    return (result)
