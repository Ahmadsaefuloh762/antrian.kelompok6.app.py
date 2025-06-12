import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Fungsi untuk menghitung metrik M/M/1
def mm1_metrics(lam, mu):
    if lam >= mu:
        return None, None  # sistem tidak stabil
    Wq = lam / (mu * (mu - lam))         # waktu tunggu antrian (jam)
    W = 1 / (mu - lam)                   # waktu total dalam sistem (jam)
    return Wq * 60, W * 60               # dikembalikan dalam menit

# Judul aplikasi
st.title("Simulasi Model Antrian M/M/1")

# Input dari pengguna
mu = st.number_input("Laju pelayanan (μ) - orang per jam", min_value=1.0, value=10.0, step=1.0)
lam = st.slider("Laju kedatangan (λ) - orang per jam", min_value=0.1, max_value=mu - 0.1, value=6.0, step=0.1)

# Hitung metrik saat ini
Wq, W = mm1_metrics(lam, mu)

if Wq is None:
    st.error("Sistem tidak stabil: λ harus lebih kecil dari μ.")
else:
    st.write(f"### Hasil untuk λ = {lam} dan μ = {mu}")
    st.write(f"- **Tingkat Utilisasi (ρ)**: {round(lam/mu, 2)}")
    st.write(f"- **Waktu Tunggu dalam Antrian (Wq)**: {Wq:.2f} menit")
    st.write(f"- **Waktu Total dalam Sistem (W)**: {W:.2f} menit")

    # Plot grafik pengaruh λ terhadap waktu
    lam_values = np.linspace(0.1, mu - 0.1, 100)
    Wq_values, W_values = [], []
    for l in lam_values:
        wq, w = mm1_metrics(l, mu)
        Wq_values.append(wq)
        W_values.append(w)

    # Tampilkan grafik
    fig, ax = plt.subplots()
    ax.plot(lam_values, Wq_values, label='Waktu Menunggu (Wq)', color='orange')
    ax.plot(lam_values, W_values, label='Waktu Total (W)', color='blue')
    ax.axvline(x=mu, linestyle='--', color='red', label='μ (Batas Stabilitas)')
    ax.set_title("Pengaruh Laju Kedatangan (λ) terhadap Waktu")
    ax.set_xlabel("Laju Kedatangan (λ) [orang/jam]")
    ax.set_ylabel("Waktu (menit)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
