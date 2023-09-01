from collections import defaultdict

class SortedDict:
    def __init__(self, array, sort_key=None):
        self.array = array
        self.sort_key = sort_key
        self.dict = self._create_dict()
        self.sorted_dict = self._create_sorted_dict()

    def __del__(self):
        print("DICTIONARY DELETED")

    def _create_dict(self):
        result = defaultdict(list)
        for element in sorted(self.array, key=lambda x: type(x).__name__):
            key = type(element).__name__ + "s"
            result[key].append(element)
        return result

    def _create_sorted_dict(self):
        if not self.sort_key:
            return None
        result = defaultdict(list)
        for element in sorted(self.array, key=lambda x: getattr(x, self.sort_key)):
            key = type(element).__name__ + "s"
            result[key].append(element)
        return result

    def append(self, value):
        self.array.append(value)
        self.dict = self._create_dict()
        self.sorted_dict = self._create_sorted_dict()

    def extend(self, values):
        self.array.extend(values)
        self.dict = self._create_dict()
        self.sorted_dict = self._create_sorted_dict()

    def insert(self, index, value):
        self.array.insert(index, value)
        self.dict = self._create_dict()
        self.sorted_dict = self._create_sorted_dict()

    def remove(self, value):
        if value in self.array:
            self.array.remove(value)
            self.dict = self._create_dict()
            self.sorted_dict = self._create_sorted_dict()
        else:
            print(value, "NOT IN THE SORTED DICT ARRAY")

    def pop(self, index=-1):
        value = self.array.pop(index)
        self.dict = self._create_dict()
        self.sorted_dict = self._create_sorted_dict()
        return value

    def __setitem__(self, index, value):
        self.array[index] = value
        self.dict = self._create_dict()
        self.sorted_dict = self._create_sorted_dict()

    def __delitem__(self, index):
        del self.array[index]
        self.dict = self._create_dict()
        self.sorted_dict = self._create_sorted_dict()
