import unittest
from hashDictionary import HashMap, MonoidHashMap
from hypothesis import given, strategies as st


class TestHashMap(unittest.TestCase):

    def test_add_and_get(self):
        hashmap = HashMap()
        hashmap.add('key1', 'value1')
        self.assertEqual(hashmap.get('key1'), 'value1')
        # Additional: Test value overwrite for duplicate keys
        hashmap.add('key1', 'new_value')
        self.assertEqual(hashmap.get('key1'), 'new_value')
        # Ensure value is updated

    def test_remove(self):
        hashmap = HashMap()
        hashmap.add('key1', 'value1')
        hashmap.remove('key1')
        self.assertEqual(hashmap.get('key1'), None)
        # Additional: Test re-adding after removal
        hashmap.add('key1', 'value2')
        self.assertEqual(hashmap.get('key1'), 'value2')

    def test_size(self):
        hashmap = HashMap()
        hashmap.add('key1', 'value1')
        hashmap.add('key2', 'value2')
        self.assertEqual(hashmap.size(), 2)
        # Additional: Test duplicate keys don't increase size
        hashmap.add('key1', 'value3')
        self.assertEqual(hashmap.size(), 2)  # Size should remain 2, not 3

    def test_is_member(self):
        hashmap = HashMap()
        hashmap.add('key1', 'value1')
        self.assertTrue(hashmap.is_member('key1'))
        self.assertFalse(hashmap.is_member('key2'))

    def test_from_to_builtin_list(self):
        hashmap = HashMap()
        initial_list = [('key1', 'value1'), ('key2', 'value2')]
        hashmap.from_builtin_list(initial_list)
        self.assertEqual(hashmap.to_builtin_list(), initial_list)
        # Additional: Test if list order is preserved
        hashmap.add('key3', 'value3')
        self.assertEqual(hashmap.to_builtin_list()[-1], ('key3', 'value3'))


class TestMonoidHashMap(unittest.TestCase):

    def test_empty(self):
        empty_hashmap = MonoidHashMap.empty()
        self.assertEqual(empty_hashmap.size(), 0)

    def test_concat(self):
        hashmap1 = MonoidHashMap()
        hashmap2 = MonoidHashMap()
        hashmap1.add('key1', 'value1')
        hashmap2.add('key1', 'value2')  # Same key with different value
        hashmap2.add('key2', 'value3')

        concated_hashmap = hashmap1.concat(hashmap2)
        # Test key overwriting
        self.assertEqual(concated_hashmap.get('key1'), 'value2')
        # Later value overwrites
        self.assertEqual(concated_hashmap.get('key2'), 'value3')
        # Test order: keys from latter map should be at the end
        self.assertEqual(concated_hashmap.to_builtin_list()[-1],
                         ('key2', 'value3'))

    def test_map_by_function(self):
        hashmap = MonoidHashMap()
        hashmap.add('key1', 1)
        hashmap.add('key2', 2)
        new_map = hashmap.map_by_function(lambda x: x * 2)
        self.assertEqual(new_map.get('key1'), 2)
        self.assertEqual(new_map.get('key2'), 4)
        # Test original map is not modified
        self.assertEqual(hashmap.get('key1'), 1)

    def test_reduce_process_elements(self):
        hashmap = MonoidHashMap()
        hashmap.add('key1', 1)
        hashmap.add('key2', 2)
        result = hashmap.reduce_process_elements(lambda x, y: x + y, initial=0)
        self.assertEqual(result, 3)
        # Test empty map
        empty_map = MonoidHashMap.empty()
        self.assertEqual(empty_map.reduce_process_elements(
            lambda x, y: x+y, initial=0), 0)


class TestMonoidHashMapPBT(unittest.TestCase):

    @given(
        st.lists(st.tuples(st.text(), st.integers()),
                 unique_by=lambda x: x[0]),  # Ensure keys are unique
        st.lists(st.tuples(st.text(), st.integers()),
                 unique_by=lambda x: x[0]),
        st.lists(st.tuples(st.text(), st.integers()),
                 unique_by=lambda x: x[0])
    )
    def test_monoid_associativity(self, lst1, lst2, lst3):
        hashmap1 = MonoidHashMap()
        hashmap1.from_builtin_list(lst1)
        hashmap2 = MonoidHashMap()
        hashmap2.from_builtin_list(lst2)
        hashmap3 = MonoidHashMap()
        hashmap3.from_builtin_list(lst3)

        left = hashmap1.concat(hashmap2).concat(hashmap3)
        right = hashmap1.concat(hashmap2.concat(hashmap3))

        # Compare as dictionaries since list order might differ
        # but content should be same
        self.assertEqual(
            dict(left.to_builtin_list()),
            dict(right.to_builtin_list())
        )

    @given(st.lists(st.tuples(st.text(), st.integers())))
    def test_monoid_identity(self, lst):
        hashmap = MonoidHashMap()
        hashmap.from_builtin_list(lst)
        empty_map = MonoidHashMap.empty()

        # Concatenating with empty map shouldn't change the original
        self.assertEqual(
            dict(hashmap.concat(empty_map).to_builtin_list()),
            dict(hashmap.to_builtin_list())
        )
        self.assertEqual(
            dict(empty_map.concat(hashmap).to_builtin_list()),
            dict(hashmap.to_builtin_list())
        )


if __name__ == '__main__':
    unittest.main()
