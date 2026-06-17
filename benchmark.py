import time
import random


def buat_dataset(ukuran, jenis):
    """Buat dataset angka acak sesuai ukuran dan jenis."""
    data = random.sample(range(ukuran * 10), ukuran)
    if jenis == "terurut":
        data.sort()
    elif jenis == "descending":
        data.sort(reverse=True)
    return data


# ── ARRAY / LIST ─────────────────────────────────────

def array_insert(daftar, nilai):
    daftar.append(nilai)

def array_search(daftar, target):
    return target in daftar

def array_delete(daftar, target):
    if target in daftar:
        daftar.remove(target)


# ── BINARY SEARCH TREE (BST) ─────────────────────────

class NodeBST:
    def __init__(self, nilai):
        self.nilai = nilai
        self.kiri  = None
        self.kanan = None

class BST:
    def __init__(self):
        self.akar = None

    def insert(self, nilai):
        if self.akar is None:
            self.akar = NodeBST(nilai)
            return
        sekarang = self.akar
        while True:
            if nilai < sekarang.nilai:
                if sekarang.kiri is None:
                    sekarang.kiri = NodeBST(nilai)
                    return
                sekarang = sekarang.kiri
            elif nilai > sekarang.nilai:
                if sekarang.kanan is None:
                    sekarang.kanan = NodeBST(nilai)
                    return
                sekarang = sekarang.kanan
            else:
                return  # duplikat diabaikan

    def search(self, nilai):
        sekarang = self.akar
        while sekarang:
            if nilai == sekarang.nilai:
                return True
            sekarang = sekarang.kiri if nilai < sekarang.nilai else sekarang.kanan
        return False

    def delete(self, nilai):
        """Hapus nilai dari BST secara iteratif untuk menghindari RecursionError."""
        induk = None
        sekarang = self.akar

        # Langkah 1: Cari node yang ingin dihapus dan induknya
        while sekarang and sekarang.nilai != nilai:
            induk = sekarang
            if nilai < sekarang.nilai:
                sekarang = Thermal = sekarang.kiri
            else:
                sekarang = sekarang.kanan

        # Jika nilai tidak ditemukan di dalam pohon
        if sekarang is None:
            return

        # Langkah 2: Kasus 1 & 2 - Node memiliki 0 atau 1 anak
        if sekarang.kiri is None or sekarang.kanan is None:
            if sekarang.kiri is not None:
                anak = sekarang.kiri
            else:
                anak = sekarang.kanan

            if induk is None:
                self.akar = anak
            elif sekarang == induk.kiri:
                induk.kiri = anak
            else:
                induk.kanan = anak

        # Langkah 3: Kasus 3 - Node memiliki 2 anak
        else:
            induk_penerus = sekarang
            penerus = sekarang.kanan
            while penerus.kiri is not None:
                induk_penerus = penerus
                penerus = penerus.kiri

            sekarang.nilai = penerus.nilai

            if induk_penerus.kiri == penerus:
                induk_penerus.kiri = penerus.kanan
            else:
                induk_penerus.kanan = penerus.kanan

    @classmethod
    def dari_list(cls, data):
        pohon = cls()
        for nilai in data:
            pohon.insert(nilai)
        return pohon

# ── HASH TABLE ───────────────────────────────────────

class HashTable:
    def __init__(self, data=None):
        self._tabel = {}
        if data:
            for nilai in data:
                self._tabel[nilai] = nilai

    def insert(self, nilai):
        self._tabel[nilai] = nilai

    def search(self, nilai):
        return nilai in self._tabel

    def delete(self, nilai):
        self._tabel.pop(nilai, None)


# ── AVL TREE ─────────────────────────────────────────

class NodeAVL:
    def __init__(self, nilai):
        self.nilai  = nilai
        self.kiri   = None
        self.kanan  = None
        self.tinggi = 1

class AVLTree:
    def __init__(self):
        self.akar = None

    def _tinggi(self, s):
        return s.tinggi if s else 0

    def _fk(self, s):
        return self._tinggi(s.kiri) - self._tinggi(s.kanan)

    def _update(self, s):
        s.tinggi = 1 + max(self._tinggi(s.kiri), self._tinggi(s.kanan))

    def _rot_kanan(self, y):
        x = y.kiri
        y.kiri  = x.kanan
        x.kanan = y
        self._update(y)
        self._update(x)
        return x

    def _rot_kiri(self, x):
        y       = x.kanan
        x.kanan = y.kiri
        y.kiri  = x
        self._update(x)
        self._update(y)
        return y

    def _seimbangkan(self, s):
        self._update(s)
        fk = self._fk(s)
        if fk > 1 and self._fk(s.kiri) >= 0:
            return self._rot_kanan(s)
        if fk > 1 and self._fk(s.kiri) < 0:
            s.kiri = self._rot_kiri(s.kiri)
            return self._rot_kanan(s)
        if fk < -1 and self._fk(s.kanan) <= 0:
            return self._rot_kiri(s)
        if fk < -1 and self._fk(s.kanan) > 0:
            s.kanan = self._rot_kanan(s.kanan)
            return self._rot_kiri(s)
        return s

    def insert(self, nilai):
        self.akar = self._insert(self.akar, nilai)

    def _insert(self, s, nilai):
        if s is None:
            return NodeAVL(nilai)
        if nilai < s.nilai:
            s.kiri  = self._insert(s.kiri, nilai)
        elif nilai > s.nilai:
            s.kanan = self._insert(s.kanan, nilai)
        return self._seimbangkan(s)

    def search(self, nilai):
        s = self.akar
        while s:
            if nilai == s.nilai:
                return True
            s = s.kiri if nilai < s.nilai else s.kanan
        return False

    def delete(self, nilai):
        self.akar = self._hapus(self.akar, nilai)

    def _hapus(self, s, nilai):
        if s is None:
            return None
        if nilai < s.nilai:
            s.kiri  = self._hapus(s.kiri, nilai)
        elif nilai > s.nilai:
            s.kanan = self._hapus(s.kanan, nilai)
        else:
            if s.kiri is None:
                return s.kanan
            if s.kanan is None:
                return s.kiri
            penerus = s.kanan
            while penerus.kiri:
                penerus = penerus.kiri
            s.nilai = penerus.nilai
            s.kanan = self._hapus(s.kanan, penerus.nilai)
        return self._seimbangkan(s)

    @classmethod
    def dari_list(cls, data):
        pohon = cls()
        for nilai in data:
            pohon.insert(nilai)
        return pohon


# ── FUNGSI BENCHMARK ─────────────────────────────────

def jalankan_benchmark(ukuran, jenis_dataset, operasi, ulangan=5):
    """Ukur waktu keempat struktur data, kembalikan dict hasil rata-rata (µs)."""
    kumpulan = {}

    for _ in range(ulangan):
        data      = buat_dataset(ukuran, jenis_dataset)
        target    = random.choice(data)
        nilai_baru = max(data) + random.randint(1, 100)

        daftar_strukt = {
            "Array/List": data.copy(),
            "BST":        BST.dari_list(data),
            "Hash Table": HashTable(data),
            "AVL Tree":   AVLTree.dari_list(data),
        }

        for nama, strukt in daftar_strukt.items():
            awal = time.perf_counter()

            if operasi == "insert":
                if nama == "Array/List":
                    array_insert(strukt, nilai_baru)
                else:
                    strukt.insert(nilai_baru)

            elif operasi == "search":
                if nama == "Array/List":
                    array_search(strukt, target)
                else:
                    strukt.search(target)

            else:  # delete
                if nama == "Array/List":
                    array_delete(strukt, target)
                else:
                    strukt.delete(target)

            waktu_us = (time.perf_counter() - awal) * 1_000_000
            kumpulan.setdefault(nama, []).append(waktu_us)

    return {nama: round(sum(w) / len(w), 4) for nama, w in kumpulan.items()}
