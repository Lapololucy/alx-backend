#!/usr/bin/python3
""" 5. LFU Caching """

BaseCaching = __import__("base_caching").BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache that inherits from BaseCaching and is a caching system
    """

    def __init__(self):
        """ Initialize the class """
        super().__init__()
        self.obj = {}

    def put(self, key, item):
        """  assign to the dictionary self.cache_data the item value
        for the key key
        """
        if key and item:
            if (len(self.cache_data) == self.MAX_ITEMS
                    and key not in self.cache_data):
                discarded = min(self.obj, key=self.obj.get)
                del self.cache_data[discarded]
                del self.obj[discarded]
                print("DISCARD: {}".format(discarded))

            if key in self.cache_data:
                self.obj[key] += 1
            else:
                self.obj[key] = 1
            self.cache_data[key] = item

    def get(self, key):
        """ returns the value in self.cache_data linked to key
        """
        if key in self.cache_data:
            self.obj[key] += 1
            return self.cache_data.get(key)
