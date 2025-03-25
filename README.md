# BABEL - Lab 1 - Variant 7

This project implements a hash map using separate chaining collision resolution
and extends it with monoid operations. Designed for educational purposes to
demonstrate hash table implementation and algebraic structures.

---

## Project Structure

### Code Files

- `hash.py`  
Contains `HashMap` and `MonoidHashMap` implementations with:  
  - Key-value operations: `add`, `get`, `remove`  
  - Insertion order preservation (`to_builtin_list`)  
  - List serialization (`from_builtin_list`, `to_builtin_list`)  
  - Data transformations (`filter_by_predicate`, `map_by_function`)  
  - Monoid operations (`empty`, `concat`, `reduce_process_elements`)

- `test_hashmap.py`
Comprehensive test suite including:  
  - Unit tests for core functionality  
  - Hypothesis-based property tests (PBT)  
  - Order preservation verification  
  - Collision handling validation  

---

## Core Features

### Hash Map Implementation

- **Separate Chaining**: Dynamic collision resolution using bucket lists  
- **Key Uniqueness**: Ensures unique keys with value overwriting  
- **Order Preservation**: Maintains insertion order for
                          deterministic iteration  

### Monoid Operations

- **Identity Element**: `MonoidHashMap.empty()` returns neutral element  
- **Associative Merge**: `concat()` combines maps with last-write semantics  
- **Data Processing**:  

  ```python
  # Value transformation
  new_map = original.map_by_function(lambda x: x*2)

  # Aggregation
  total = original.reduce_process_elements(lambda a,b: a+b)

---

## Contributors

| Contributor      | Contact               | Contributions                |
|------------------|-----------------------|------------------------------|
| He Jian          | <hj66216084@gmail.com>| Core implementation & testing|
| Aleksandr Penskoi| <penskoi@example.com> | Project template design      |

---

## Changelog

### 2025-3-22

- Complete `HashDictionary` implementation  
- Monoid operations extension  

#### Changed

- Optimized collision handling performance  
- Improved insertion order tracking  

### 2025-3-23

- Property-based testing suite  

### 2025-3-25

- Initial project scaffolding  
- Basic README structure  

---

## Design Notes

### Hash Table Architecture

```python

class HashMap:
    def __init__(self):
        self.bucket_size = 10  # Fixed bucket count
        self.buckets = [None] * self.bucket_size
        self.keys_order = []  # Insertion order tracking

```

### Monoid Implementation

```python

class MonoidHashMap(HashMap):
    @classmethod
    def empty(cls):
        """Identity element for monoid operations"""
        return cls()

    def concat(self, other):
        """Merge operation with last-write semantics"""
        for key in other.keys_order:
            self.add(key, other.get(key))

```

### Implementation Restrictions

#### Mutability Constraints

- **In-place Modification**: Operations modify original dict directly
- **No History**: Cannot revert to previous states

#### Performance Limits

- **Hash Collisions**:
  - Linked lists may become linear
  - Delete ops require O(n) time
- **Memory**:
  - No reuse optimization
  - Fragmentation from frequent changes

#### Functional Limits

- **Keys**: Relies on Python `hash()`
- **Order**: Output order ≠ insertion order
- **Capacity**: Fixed bucket count

### Testing Analysis

#### Unit Tests

| **Pros**          | **Cons**          |
|-------------------|-------------------|
| Precise validation| Hard to cover edges|
| Fast feedback     | Maintenance grows |
| Readable cases    | Depends on dev data|

#### Property Tests

| **Pros**          | **Cons**          |
|-------------------|-------------------|
| Auto-generates cases| Hard to debug fails|
| Checks math props  | Needs careful setup|
| Finds threading bugs| Slower execution |

#### Test Types

| **Type**  | **Purpose**       | **Used For**       |
|-----------|-------------------|--------------------|
| Unit      | Core functionality| API validation     |
| PBT       | Robustness        | Filter invariants  |
| Integration| Module interaction| (Not used)         |

### Improvements

1. **Thread Safety**: Add modification locks
2. **Resizing**: Dynamic bucket expansion
3. **Memory**: Pooled node allocation
4. **Metrics**: Add performance benchmarks
