
import streamlit as st
import requests
import base64
from pathlib import Path
from config import config

from src.rag_logic import get_relevant_context, generate_llm_answer


def get_answer_from_api(question: str):
    try:
         context = get_relevant_context(soru)
         final_answer = generate_llm_answer(soru, context)
         return final_answer

    except Exception as e:
        return f"Beklenmedik bir hata oluştu: {e}"
   
@st.cache_data
def get_image_as_base64(file):
    try:
        path = Path(file)
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

st.set_page_config(layout="wide", page_title="TRT Dijital Destek Asistanı", page_icon="📺")

IMG_PATH = "asistan.png"
img_base64 = get_image_as_base64(IMG_PATH)

if img_base64:
    st.markdown(f"""
        <div style='background-color: #002147; padding: 20px 30px; border-radius: 12px; margin-bottom: 30px; max-width: 1000px; margin-left: auto; margin-right: auto; display: flex; align-items: center;'>
            <div style='display: flex; align-items: center;'>
                <img src="data:image/png;base64,{img_base64}" style="width: 60px; height: 60px; margin-right: 20px;">
                <div>
                    <h1 style='color: white; margin: 0;'>TRT Dijital Destek Asistanı</h1>
                    <p style='color: #e0e0e0; margin: 0;'>TRT hakkında sorunu yaz, sana en uygun cevabı getireyim!</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div style='background-color: #002147; padding: 25px 30px; border-radius: 12px; margin-bottom: 30px; max-width: 1000px; margin-left: auto; margin-right: auto; display: flex; align-items: center;'>
            <div style='display: flex; align-items: center;'>
                <h1 style='color: white; margin: 0;'> TRT Dijital Destek Asistanı</h1>
                <p style='color: #e0e0e0; margin: 0;'>TRT hakkında sorunu yaz, sana en uygun cevabı getireyim!</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

if "gecmis" not in st.session_state:
    karsilama_mesaji = "Selam! Ben TRT Dijital Destek Asistanı. 🚀 Sana TRT'nin tarihi, kanalları, dijital uygulamaları ve güncel projeleri gibi birçok konu hakkında anında bilgi verebilirim. Merak ettiğin ne varsa, sorman yeterli!"
    st.session_state.gecmis = [("BOT_ACILIS", karsilama_mesaji)]

for soru, cevap in st.session_state.gecmis:
    if soru == "BOT_ACILIS":
        st.markdown(f"""
            <div style="max-width:1000px; margin:auto; margin-bottom:20px;">
                <div style="text-align:left;">
                    <div class="bot-message">
                        {cevap}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="max-width:1000px; margin:auto; margin-bottom:20px;">
                <div style="text-align:right;">
                    <div style="display:inline-block; background-color:#e1e5ea; color:#002147;
                                padding:14px 20px; border-radius:18px 18px 0px 18px; max-width:80%;
                                font-size:18px; line-height:1.6;">
                        {soru}
                    </div>
                </div>
                <br>
                <div style="text-align:left;">
                    <div class="bot-message">
                        {cevap}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] > .main {
            padding-bottom: 9rem; 
        }
        [data-testid="stForm"] {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            width: 100%;
            padding: 1rem 0;
            background: white;
            border-top: 1px solid #ddd;
            z-index: 100;
        }
        [data-testid="stForm"] > div:first-child {
            max-width: 1000px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        [data-testid="stHorizontalBlock"] {
            align-items: center;
        }
        .bot-message {
            display: inline-block; background-color: #ffffff; color: #222; padding: 16px 22px;
            border-radius: 18px 18px 18px 0px; max-width: 85%; font-size: 18px;
            line-height: 1.7; border: 1px solid #ddd;
        }
        .bot-message p {
            font-size: 18px; margin-bottom: 0;
        }
        [data-testid="stTextInput"] > div:first-child {
            height: 90px;
            display: flex;
            align-items: center;
        }
        [data-testid="stTextInput"] input {
            font-size: 24px;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        [data-testid="stFormSubmitButton"] button {
            background-color: #002147 !important;
            color: white !important;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

with st.form("soru_form", clear_on_submit=True):
    col1, col2 = st.columns([8, 1])
    with col1:
        soru = st.text_input("Soru", placeholder="TRT hakkında merak ettiğini yaz...", label_visibility="collapsed", key="soru_alani")
    with col2:
        gonder = st.form_submit_button("➤")

if gonder and soru.strip():
    with st.spinner("Cevabınız hazırlanıyor... ✨"):
        final_answer = get_answer_from_api(soru)
        
        st.session_state.gecmis.append((soru, final_answer))

        st.rerun()


