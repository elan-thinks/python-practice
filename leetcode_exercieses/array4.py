class DynamicArray:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self.capacity = capacity
        self.array = [None] * capacity
        self.size = 0

    def get(self, i: int) -> int:
        if not (0 <= i < self.size):
            raise IndexError("index out of range")
        return self.array[i]

    def set(self, i: int, n: int) -> None:
        if not (0 <= i < self.size):
            raise IndexError("index out of range")
        self.array[i] = n

    def pushback(self, n: int) -> None:
        if self.size == self.capacity:
            self.resize()
        self.array[self.size] = n
        self.size += 1

    def popback(self) -> int:
        if self.size == 0:
            raise IndexError("pop from empty array")
        self.size -= 1
        return self.array[self.size]

    def resize(self) -> None:
        new_capacity = self.capacity * 2
        new_data = [None] * new_capacity

        for i in range(self.size):
            new_data[i] = self.array[i]
        self.array = new_data
        self.capacity = new_capacity

    def getSize(self) -> int:
        return self.size

    def getCapacity(self) -> int:
        return self.capacity

da = DynamicArray(1)
print([da.getSize(), da.getCapacity()])   # [0, 1]

da.pushback(1)
print([da.getSize(), da.getCapacity()])   # [1, 1]

da.pushback(2)                            # triggers resize
print([da.getSize(), da.getCapacity()])   # [2, 2]

print(da.popback())                       # 2
print([da.getSize(), da.getCapacity()])   # [1, 2]

da.set(0, 99)
print(da.get(0))                          # 99
print(da)

# ["Array", 1, "pushback", 1, "getCapacity", "pushback", 2, "getCapacity"]

