import unittest
from hashDictionary import HashMap, MonoidHashMap
from hypothesis import given, strategies as st

class TestHashMap(unittest.TestCase):

    def test_add_and_get(self):
        hashmap = HashMap()
        hashmap.add('key1', 'value1')
        self.assertEqual(hashmap.get('key1'), 'value1')
        # 新增：测试重复键的值覆盖
        hashmap.add('key1', 'new_value')
        self.assertEqual(hashmap.get('key1'), 'new_value')  # 确保值被更新

    def test_remove(self):
        hashmap = HashMap()
        hashmap.add('key1', 'value1')
        hashmap.remove('key1')
        self.assertEqual(hashmap.get('key1'), None)
        # 新增：测试删除后重新添加
        hashmap.add('key1', 'value2')
        self.assertEqual(hashmap.get('key1'), 'value2')

    def test_size(self):
        hashmap = HashMap()
        hashmap.add('key1', 'value1')
        hashmap.add('key2', 'value2')
        self.assertEqual(hashmap.size(), 2)
        # 新增：测试重复键不计入size
        hashmap.add('key1', 'value3')
        self.assertEqual(hashmap.size(), 2)  # Size应保持2，不是3

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
        # 新增：测试列表顺序是否保留
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
        hashmap2.add('key1', 'value2')  # 相同键不同值
        hashmap2.add('key2', 'value3')
        
        concated_hashmap = hashmap1.concat(hashmap2)
        # 测试键覆盖
        self.assertEqual(concated_hashmap.get('key1'), 'value2')  # 后者覆盖前者
        self.assertEqual(concated_hashmap.get('key2'), 'value3')
        # 测试顺序：后合并的键应在末尾
        self.assertEqual(concated_hashmap.to_builtin_list()[-1], ('key2', 'value3'))

    def test_map_by_function(self):
        hashmap = MonoidHashMap()
        hashmap.add('key1', 1)
        hashmap.add('key2', 2)
        new_map = hashmap.map_by_function(lambda x: x * 2)
        self.assertEqual(new_map.get('key1'), 2)
        self.assertEqual(new_map.get('key2'), 4)
        # 测试原Map未被修改
        self.assertEqual(hashmap.get('key1'), 1)

    def test_reduce_process_elements(self):
        hashmap = MonoidHashMap()
        hashmap.add('key1', 1)
        hashmap.add('key2', 2)
        result = hashmap.reduce_process_elements(lambda x, y: x + y, initial=0)
        self.assertEqual(result, 3)
        # 测试空Map
        empty_map = MonoidHashMap.empty()
        self.assertEqual(empty_map.reduce_process_elements(lambda x,y: x+y, initial=0), 0)

class TestMonoidHashMapPBT(unittest.TestCase):

    @given(
        st.lists(st.tuples(st.text(), st.integers()), unique_by=lambda x: x[0]),  # 确保键唯一
        st.lists(st.tuples(st.text(), st.integers()), unique_by=lambda x: x[0]),
        st.lists(st.tuples(st.text(), st.integers()), unique_by=lambda x: x[0])
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
        
        # 转换为字典比较，因为列表顺序可能不同但内容应相同
        self.assertEqual(
            dict(left.to_builtin_list()),
            dict(right.to_builtin_list())
        )

    @given(st.lists(st.tuples(st.text(), st.integers())))
    def test_monoid_identity(self, lst):
        hashmap = MonoidHashMap()
        hashmap.from_builtin_list(lst)
        empty_map = MonoidHashMap.empty()
        
        # 合并空Map应不影响原数据
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