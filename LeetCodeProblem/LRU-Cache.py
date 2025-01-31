from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache.keys():
            return -1
        value = self.cache[key]
        self.cache.move_to_end(key)
        return value

    def put(self, key: int, value: int) -> None:

        if key in self.cache.keys():
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value


if __name__ == '__main__':
    lRUCache = LRUCache(2);
    lRUCache.put(1, 1)
    lRUCache.put(2, 2)
    print('get ', lRUCache.get(1))  # renvoie 1
    lRUCache.put(3, 3)  # La clé LRU était 2, supprime la clé 2, le cache est {1=1, 3=3}
    print('get ', lRUCache.get(2))  # renvoie -1 (non trouvé)
    lRUCache.put(4, 4)  # La clé LRU était 1, supprime la clé 1, le cache est {4=4, 3=3}
    print('get ', lRUCache.get(1))  # renvoie -1 (non trouvé)
    print('get ', lRUCache.get(3))  # renvoie 3
    print('get ', lRUCache.get(4))  # renvoie 4
