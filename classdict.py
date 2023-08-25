class SortedDict:
    def __init__(self, array, key=None):
        self.array = array
        self.key = key
        self.dict = self._create_dict()

    def _create_dict(self):
        return {i: x for i, x in enumerate(sorted(self.array, key=self.key))}

    def append(self, value):
        self.array.append(value)
        self.dict = self._create_dict()

    def extend(self, values):
        self.array.extend(values)
        self.dict = self._create_dict()

    def insert(self, index, value):
        self.array.insert(index, value)
        self.dict = self._create_dict()

    def remove(self, value):
        self.array.remove(value)
        self.dict = self._create_dict()

    def pop(self, index=-1):
        value = self.array.pop(index)
        self.dict = self._create_dict()
        return value

    def __setitem__(self, index, value):
        self.array[index] = value
        self.dict = self._create_dict()

    def __delitem__(self, index):
        del self.array[index]
        self.dict = self._create_dict()