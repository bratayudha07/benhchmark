import streamlit as st
import pandas as pd
from benchmark import buat_dataset, jalankan_benchmark

st.set_page_config(page_title="Benchmarking Struktur Data", page_icon="⚡")

st.title("⚡ Benchmarking Performa Struktur Data")
st.caption("Membandingkan Array/List, BST, Hash Table, dan AVL Tree.")

st.markdown("---")

# ── LANGKAH 1 – GENERATE DATASET ────────────────────

st.header("1. Generate Dataset")

ukuran = st.selectbox(
    "Ukuran Dataset", [100, 1_000, 10_000], format_func=lambda x: f"{x:,} data"
)
jenis = st.selectbox(
    "Jenis Dataset", ["acak", "terurut", "descending"], format_func=str.capitalize
)

if st.button("Generate Dataset"):
    contoh = buat_dataset(ukuran, jenis)
    st.success(f"Dataset berhasil dibuat: {ukuran:,} data ({jenis})")
    st.write("Contoh 10 data pertama:", contoh[:10])

st.markdown("---")

# ── LANGKAH 2 & 3 – PILIH STRUKTUR DATA & OPERASI ───

st.header("2. Pilih Operasi")

operasi = st.selectbox(
    "Operasi", ["search", "insert", "delete"], format_func=str.capitalize
)
ulangan = st.slider("Jumlah Pengulangan", 1, 20, 5)

st.markdown("---")

# ── LANGKAH 4 – LAKUKAN BENCHMARK ───────────────────

st.header("3. Lakukan Benchmark")

if st.button("▶ Jalankan Benchmark"):
    with st.spinner("Sedang mengukur performa …"):
        hasil = jalankan_benchmark(ukuran, jenis, operasi, ulangan)

    st.success("✅ Benchmark selesai!")

    # ── LANGKAH 5 – TAMPILKAN GRAFIK DAN ANALISIS ───

    st.header("4. Hasil & Analisis")

    # Tabel hasil
    df = pd.DataFrame(
        list(hasil.items()), columns=["Struktur Data", "Waktu Rata-rata (µs)"]
    )
    df = df.sort_values("Waktu Rata-rata (µs)").reset_index(drop=True)
    st.dataframe(df, width="stretch")  # ← perbaikan di sini

    # Grafik batang bawaan Streamlit
    st.bar_chart(df.set_index("Struktur Data"))

    # Analisis sederhana
    st.subheader("Analisis")

    tercepat = df.iloc[0]
    terlambat = df.iloc[-1]

    st.write(
        f"✅ **Tercepat**: {tercepat['Struktur Data']} "
        f"({tercepat['Waktu Rata-rata (µs)']:.4f} µs)"
    )
    st.write(
        f"🐢 **Terlambat**: {terlambat['Struktur Data']} "
        f"({terlambat['Waktu Rata-rata (µs)']:.4f} µs)"
    )

    selisih = terlambat["Waktu Rata-rata (µs)"] - tercepat["Waktu Rata-rata (µs)"]
    st.write(f"📊 Selisih waktu: **{selisih:.4f} µs**")

    # Catatan khusus dataset terurut
    if jenis in ["terurut", "descending"]:
        st.warning(
            "⚠️ Dataset terurut/descending adalah kasus terburuk BST. "
            "Pohon BST bisa menjadi tidak seimbang sehingga performanya menurun. "
            "AVL Tree tetap stabil karena melakukan rotasi otomatis."
        )

st.markdown("---")

# ── TABEL KOMPLEKSITAS ───────────────────────────────

st.header("📐 Kompleksitas Algoritma")

df_kompleksitas = pd.DataFrame(
    {
        "Struktur Data": ["Array/List", "BST", "Hash Table", "AVL Tree"],
        "Search": ["O(n)", "O(log n)*", "O(1)", "O(log n)"],
        "Insert": ["O(1)", "O(log n)*", "O(1)", "O(log n)"],
        "Delete": ["O(n)", "O(log n)*", "O(1)", "O(log n)"],
    }
)
st.dataframe(
    df_kompleksitas.set_index("Struktur Data"), width="stretch"
)  # ← perbaikan di sini
st.caption("* BST tidak self-balancing → bisa O(n) pada data terurut.")
