import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from openai import AzureOpenAI
from fastapi import HTTPException
from config import config
from src import prompts
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent 
DATA_PATH = ROOT_DIR / "TRTData_final.csv"


def load_model_and_index():
    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
    
    df = pd.read_csv(DATA_PATH)
    
    sorular = df["soru"].tolist()
    cevaplar = df["metin"].tolist()
    soru_embeddings = model.encode(sorular, convert_to_numpy=True)
    index = faiss.IndexFlatL2(soru_embeddings.shape[1])
    index.add(soru_embeddings)
    return model, index, cevaplar

embedding_model, faiss_index, cevaplar_listesi = load_model_and_index()

client = AzureOpenAI(
    api_version=config.AZURE_API_VERSION,
    azure_endpoint=config.AZURE_ENDPOINT,
    api_key=config.AZURE_API_KEY,
)

def get_relevant_context(user_question, top_k=1):
    embed = embedding_model.encode([user_question])
    _, indices = faiss_index.search(embed, top_k)
    return [cevaplar_listesi[i] for i in indices[0]][0]

def generate_llm_answer(user_question, context):
    if not client:
        raise HTTPException(status_code=503, detail="LLM istemcisi (client) başlatılamadı.")

    system_prompt = prompts.SYSTEM_PROMPT
    
    user_prompt = f'Kullanıcının Sorusu: "{user_question}"\n\nCevabında Kullanacağın Bağlam: "{context}"'

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model=config.AZURE_DEPLOYMENT_NAME,
            temperature=0.7,
            max_tokens=800,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cevap üretilirken bir hata oluştu: {e}")