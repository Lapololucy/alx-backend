#!/usr/bin/python3
""" 2. LIFO Caching """


BaseCaching = __import__("base_caching").BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache that inherits from BaseCaching and is a caching system
    """

    def __init__(self):
        """ Initialize the class """
        super().__init__()
        self.stack = []

    def put(self, key, item):
        """  assign to the dictionary self.cache_data the item value for
        the key key """
        if key and item:
            if key in self.stack:
                self.stack.remove(key)
            if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                discarded = self.stack.pop()
                del self.cache_data[discarded]
                print("DISCARD: {}".format(discarded))
            self.stack.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """ returns the value in self.cache_data linked to key
        """
        return self.cache_data.get(key, None)
