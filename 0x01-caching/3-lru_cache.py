#!/usr/bin/python3
""" 3. LRU Caching """

from collections import deque

BaseCaching = __import__("base_caching").BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache that inherits from BaseCaching and is a caching system
    """

    def __init__(self):
        """ Initialize the class """
        super().__init__()
        self.queue = deque()

    def put(self, key, item):
        """  assign to the dictionary self.cache_data the item value
        for the key key
        """
        if key and item:
            if key in self.cache_data:
                self.queue.remove(key)
            if len(self.cache_data) == self.MAX_ITEMS:
                discarded = self.queue.popleft()
                del self.cache_data[discarded]
                print("DISCARD: {}".format(discarded))
            self.queue.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """ returns the value in self.cache_data linked to key
        """
        if key in self.cache_data:
            self.queue.remove(key)
            self.queue.append(key)
            return self.cache_data.get(key)
