import random
import time

# ==================== BST ====================
class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = {'key': key, 'left': None, 'right': None}
            return
        cur = self.root
        while True:
            if key < cur['key']:
                if cur['left'] is None:
                    cur['left'] = {'key': key, 'left': None, 'right': None}
                    break
                cur = cur['left']
            elif key > cur['key']:
                if cur['right'] is None:
                    cur['right'] = {'key': key, 'left': None, 'right': None}
                    break
                cur = cur['right']
            else:
                break

    def search(self, key):
        cur = self.root
        while cur:
            if key == cur['key']:
                return True
            cur = cur['left'] if key < cur['key'] else cur['right']
        return False

# ==================== AVL ====================
class AVLNode:
    __slots__ = ('key', 'height', 'left', 'right')
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

class AVL:
    def __init__(self):
        self.root = None

    def _height(self, n):
        return n.height if n else 0

    def _update(self, n):
        n.height = 1 + max(self._height(n.left), self._height(n.right))

    def _bf(self, n):
        return self._height(n.left) - self._height(n.right)

    def _rotate_right(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        self._update(y)
        self._update(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        self._update(x)
        self._update(y)
        return y

    def _balance(self, n):
        bf = self._bf(n)
        if bf > 1:
            if self._bf(n.left) < 0:
                n.left = self._rotate_left(n.left)
            return self._rotate_right(n)
        if bf < -1:
            if self._bf(n.right) > 0:
                n.right = self._rotate_right(n.right)
            return self._rotate_left(n)
        return n

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, n, key):
        if n is None:
            return AVLNode(key)
        if key < n.key:
            n.left = self._insert(n.left, key)
        elif key > n.key:
            n.right = self._insert(n.right, key)
        else:
            return n
        self._update(n)
        return self._balance(n)

    def search(self, key):
        cur = self.root
        while cur:
            if key == cur.key:
                return True
            cur = cur.left if key < cur.key else cur.right
        return False

# ==================== Generator dataset ====================
def generate_data(size, order):
    data = list(range(size))
    if order == 'acak':
        random.shuffle(data)
    elif order == 'terurut':
        data.sort()
    elif order == 'descending':
        data.sort(reverse=True)
    return data

# ==================== Benchmark helper ====================
def bench_structure(structure, struct_type, queries):
    start = time.perf_counter()
    for q in queries:
        if struct_type == 'list':
            _ = q in structure
        elif struct_type == 'dict':
            _ = q in structure
        elif struct_type == 'bst':
            _ = structure.search(q)
        elif struct_type == 'avl':
            _ = structure.search(q)
    elapsed = time.perf_counter() - start
    return (elapsed / len(queries)) * 1_000_000

def run_benchmark(size, order):
    data = generate_data(size, order)
    queries = random.sample(data, min(100, len(data)))

    lst = data
    d = {x: x for x in data}
    bst = BST()
    avl = AVL()
    for v in data:
        bst.insert(v)
        avl.insert(v)

    t_list = bench_structure(lst, 'list', queries)
    t_dict = bench_structure(d, 'dict', queries)
    t_bst = bench_structure(bst, 'bst', queries)
    t_avl = bench_structure(avl, 'avl', queries)

    return {
        'Ukuran': size,
        'Tipe Data': order,
        'Array/List (μs)': t_list,
        'Hash Table (μs)': t_dict,
        'BST (μs)': t_bst,
        'AVL (μs)': t_avl,
    }
