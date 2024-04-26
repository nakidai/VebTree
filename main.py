class VebTree:
    def __init__(self, size):
        self.size = size
        if size > 1:
            self.aux = None
            self.tree = [None] * (1 << (size >> 1))
        self.tree_min = self.tree_max = None

    def __getitem__(self, item):
        return self.tree[item]

    def is_empty(self) -> bool:
        return self.tree_min is None

    def __bool__(self) -> bool:
        return self.is_empty()

    def high(self, x: int) -> int:
        return x >> (self.size >> 1)

    def low(self, x: int) -> int:
        return x & ((1 << (self.size >> 1)) - 1)

    def merge(self, high: int, low: int) -> int:
        return (high << (self.size >> 1)) + low

    def insert(self, x: int):
        if self.is_empty():
            self.tree_min = self.tree_max = x
        else:
            if self.tree_min == self.tree_max:
                if self.tree_min < x:
                    self.tree_max = x
                else:
                    self.tree_min = x
            else:
                if self.tree_min > x:
                    self.tree_min, x = x, self.tree_min
                elif self.tree_max < x:
                    self.tree_max, x = x, self.tree_max

                high, low = self.high(x), self.low(x)
                if self[high] is None:
                    self.tree[high] = VebTree(self.size >> 1)
                if self[high].is_empty():
                    if self.aux is None:
                        self.aux = VebTree(self.size >> 1)
                    self.aux.insert(high)
                self.tree[high].insert(low)

    def remove(self, x):
        if self.tree_min == self.tree_max == x:
            self.tree_min = self.tree_max = None
            return
        if self.tree_min == x:
            if self.size == 1 or self.aux is None or self.aux.is_empty():
                self.tree_min = self.tree_max
                return
            x = self.merge(high := self.aux.tree_min, self[high].tree_min)
            self.tree_min = x
        if self.tree_max == x:
            if self.size == 1 or self.aux is None or self.aux.is_empty():
                self.tree_max = self.tree_min
                return
            x = self.merge(high := self.aux.tree_max, self[high].tree_max)
            self.tree_max = x
        high, low = self.high(x), self.low(x)
        self.tree[high].remove(low)
        if self[high].is_empty():
            self.aux.remove(high)
            self.tree[high] = None
        if self.aux.is_empty():
            self.aux = None

    def find_next(self, x: int) -> (int, None):
        if self.is_empty() or x > self.tree_max:
            return None
        elif x <= self.tree_min:
            return self.tree_min
        elif self.aux is None or self.aux.is_empty():
            return self.tree_max

        high, low = self.high(x), self.low(x)
        if self[high] is not None and not self[high].is_empty() and low <= self[high].tree_max:
            return self.merge(high, self[high].find_next(low))
        else:
            high = self.aux.find_next(high + 1)
            if high is not None:
                return self.merge(high, self[high].tree_min)
            else:
                return self.tree_max

    def find_prev(self, x: int) -> (int, None):
        if self.is_empty() or x < self.tree_min:
            return None
        elif x >= self.tree_max:
            return self.tree_max
        elif self.aux is None or self.aux.is_empty():
            return self.tree_min

        high, low = self.high(x), self.low(x)
        if self[high] is not None and not self[high].is_empty() and low >= self[high].tree_min:
            return self.merge(high, self[high].find_prev(low))
        else:
            high = self.aux.find_prev(high - 1)
            if high is not None:
                return self.merge(high, self[high].tree_max)
            else:
                return self.tree_min

    def lookup(self, x) -> bool:
        if x == self.tree_min or x == self.tree_max:
            return True
        else:
            high, low = self.high(x), self.low(x)
            return not self.is_empty() and self[high] is not None and self[high].lookup(low)


if __name__ == "__main__":
    t = VebTree(4)

    t.insert(7)
    t.insert(5)
    t.insert(11)
    t.insert(6)
    t.insert(2)
    t.insert(15)
    t.insert(12)

    print(t.lookup(7),
          t.lookup(5),
          t.lookup(2),
          t.lookup(11),
          t.lookup(6)
          )

    print(t.find_next(2),
          t.find_next(4),
          t.find_next(6),
          t.find_next(7),
          t.find_next(9)
          )

    print(t.lookup(5),
          t.find_next(5)
          )

    y = 16
    while y is not None:
        y = t.find_prev(y - 1)
        print(y, end=' ')
    print()

    t = VebTree(4)

    t.insert(10)
    t.insert(5)
    t.insert(2)
    t.remove(2)
    t.remove(5)
    print(t.find_next(1), t.find_next(3))
    t.insert(6)
    print(t.find_next(3))
