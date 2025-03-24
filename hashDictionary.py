class HashMap:
    def __init__(self):
        self.bucket_size = 10
        self.buckets = [None] * self.bucket_size
        self.keys_order = []  # Maintains insertion order of unique keys

    def _hash_function(self, key):
        # Compute bucket index for a given key using hash modulo.
        return hash(key) % self.bucket_size

    def add(self, key, value):
        # Insert or update a key-value pair while preserving insertion order.
        index = self._hash_function(key)
        if self.buckets[index] is None:
            self.buckets[index] = []
        #  Check if key exists in bucket
        for i, (existing_key, _) in enumerate(self.buckets[index]):
            if existing_key == key:
                #  Update existing value without changing insertion order
                self.buckets[index][i] = (key, value)
                return
        #  Add new key-value pair
        self.buckets[index].append((key, value))
        #  Track insertion order for new keys
        if key not in self.keys_order:
            self.keys_order.append(key)
        else:
            pass

    def set_element(self, key, value):
        #  Alias for add() to match dictionary-like API.
        self.add(key, value)

    def get(self, key):
        # Retrieve value for a key, returns None if not found.
        index = self._hash_function(key)
        if self.buckets[index] is not None:
            for existing_key, value in self.buckets[index]:
                if existing_key == key:
                    return value
        return None

    def remove(self, key):
        # Delete a key-value pair and its insertion order tracking.
        index = self._hash_function(key)
        if self.buckets[index] is not None:
            for i, (existing_key, _) in enumerate(self.buckets[index]):
                if existing_key == key:
                    del self.buckets[index][i]
                    if key in self.keys_order:
                        self.keys_order.remove(key)
                    return

    def size(self):
        # Return count of unique keys using insertion order tracking.
        return len(self.keys_order)

    def is_member(self, key):
        # Check if key exists using efficient order tracking.
        return key in self.keys_order

    def from_builtin_list(self, lst):
        # Populate from Python list of (key, value) tuples.
        for key, value in lst:
            self.add(key, value)

    def to_builtin_list(self):
        # Convert to Python list preserving insertion order.
        return [(key, self.get(key)) for key in self.keys_order
                if self.get(key) is not None]

    def filter_by_predicate(self, predicate):
        # Create new map containing entries that satisfy predicate(key, value).
        filtered_map = self.__class__()
        for key in self.keys_order:
            value = self.get(key)
            if value is not None and predicate(key, value):
                filtered_map.add(key, value)
        return filtered_map


class MonoidHashMap(HashMap):
    # Monoid implementation supporting empty identity
    # and associative concatenation.
    @classmethod
    def empty(cls):
        # Identity element for monoid (empty map)
        return cls()

    def concat(self, other):
        # Associative operation: merge another map into this one.
        for key in other.keys_order:
            value = other.get(key)
            #  Update insertion order for conflicts
            if key in self.keys_order:
                self.keys_order.remove(key)
            self.keys_order.append(key)
            self.add(key, value)
        return self

    def map_by_function(self, func):
        # Apply function to values and return new transformed map.
        new_map = self.__class__()
        for key in self.keys_order:
            new_map.add(key, func(self.get(key)))
        return new_map

    def reduce_process_elements(self, func, initial=None):
        # Reduce values using binary function, optionally with initial value.
        result = initial
        for key in self.keys_order:
            value = self.get(key)
            result = func(result, value) if result is not None else value
        return result
