import streamlit as st
from deepface import DeepFace
import os
import shutil
from PIL import Image
import numpy as np

# Simulasi database
database_path = "registered_faces"
os.makedirs(database_path, exist_ok=True)
registered_users = {}  # filename : {nik, name, age, address}

# Simpan data pengguna baru
def save_user_data(image_path, nik, name, age, address):
    new_name = f"{nik}_{name}.jpg"
    new_path = os.path.join(database_path, new_name)
    shutil.copy(image_path, new_path)
    registered_users[new_path] = {
        "nik": nik,
        "name": name,
        "age": age,
        "address": address
    }

# Load data dari folder (persisten)
for file in os.listdir(database_path):
    if file.endswith(".jpg"):
        parts = file.replace(".jpg", "").split("_")
        if len(parts) >= 2:
            nik, name = parts[0], parts[1]
            registered_users[os.path.join(database_path, file)] = {
                "nik": nik,
                "name": name,
                "age": "??",
                "address": "??"
            }

# UI Streamlit
st.title("🔍 Face Recognition Web App (DeepFace)")

uploaded_image = st.file_uploader("📸 Upload foto wajah:", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    img = Image.open(uploaded_image)
    st.image(img, caption="Wajah yang diunggah", width=300)
    temp_path = "temp_uploaded.jpg"
    img.save(temp_path)

    found = False
    for db_img, user_data in registered_users.items():
        try:
            result = DeepFace.verify(img1_path=temp_path, img2_path=db_img, enforce_detection=False)
            if result["verified"]:
                st.success("✅ Wajah dikenali!")
                st.markdown(f"""
                - **NIK:** {user_data['nik']}
                - **Nama:** {user_data['name']}
                - **Usia:** {user_data['age']}
                - **Alamat:** {user_data['address']}
                """)
                found = True
                break
        except Exception as e:
            st.warning(f"Gagal membandingkan: {e}")

    if not found:
        st.warning("🚫 Wajah tidak dikenali. Silakan isi data untuk registrasi.")
        with st.form("form_register"):
            nik = st.text_input("NIK")
            name = st.text_input("Nama")
            age = st.text_input("Usia")
            address = st.text_area("Alamat")
            submitted = st.form_submit_button("Daftarkan Wajah")

            if submitted:
                save_user_data(temp_path, nik, name, age, address)
                st.success("🎉 Wajah berhasil didaftarkan!")
