import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from benchmark_core import run_benchmark

st.set_page_config(page_title="Benchmark Struktur Data", layout="centered", page_icon="📊")

st.title("⚡ Benchmark Pencarian: Array vs BST vs Hash Table vs AVL")
st.caption(":material/database: Dataset: Acak, Terurut, Descending | Ukuran: 100, 1000, 10000 data")

if 'benchmark_done' not in st.session_state:
    st.session_state.benchmark_done = False
if 'df_results' not in st.session_state:
    st.session_state.df_results = None

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button(":material/play_circle: Jalankan Benchmark", type="primary", width='stretch'):
        with st.spinner("Menjalankan benchmark..."):
            sizes = [100, 1000, 10000]
            orders = ['acak', 'terurut', 'descending']
            results = []
            for size in sizes:
                for order in orders:
                    results.append(run_benchmark(size, order))
            st.session_state.df_results = pd.DataFrame(results)
            st.session_state.benchmark_done = True
        st.rerun()

if st.session_state.benchmark_done and st.session_state.df_results is not None:
    df = st.session_state.df_results

    st.subheader(":material/table_chart: Hasil Benchmark (μs)")
    st.dataframe(df, width='stretch')

    st.subheader(":material/show_chart: Grafik Perbandingan")
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='none')
    ax.set_facecolor('#1e1e1e')

    for col in ['Array/List (μs)', 'Hash Table (μs)', 'BST (μs)', 'AVL (μs)']:
        labels = [f"{row['Ukuran']}\n({row['Tipe Data']})" for _, row in df.iterrows()]
        ax.plot(labels, df[col], marker='o', label=col, linewidth=2)

    ax.set_ylabel("Waktu (μs)", color='white')
    ax.set_xlabel("Ukuran Data & Tipe Data", color='white')
    ax.tick_params(colors='white', rotation=45)
    ax.legend(facecolor='#2d2d2d', edgecolor='white', labelcolor='white')
    ax.grid(True, linestyle='--', alpha=0.5, color='gray')
    ax.set_title("Perbandingan Kecepatan Pencarian", color='white', fontsize=14)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

    st.info(
        "**:material/insight: Kesimpulan**  \n"
        "Hash Table (dict) konsisten tercepat. AVL stabil O(log n). "
        "BST memburuk pada data terurut/descending karena menjadi linear.",
        icon=":material/info:"
    )
else:
    st.info(
        "**:material/play_arrow: Klik tombol di atas untuk memulai benchmark.**",
        icon=":material/start:"
    )
