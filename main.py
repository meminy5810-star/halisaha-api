from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Performans(BaseModel):
    oyuncu_id: int
    reyting: float
    gol: int
    asist: int

# Veritabanı tablosu zaten var, aynen devam ediyoruz.

@app.post("/performanslar")
def performans_ekle(p: Performans):
    conn = sqlite3.connect("halisaha.db")
    cursor = conn.cursor()
    # Herkesin oyu yeni bir satır olarak kaydedilir
    cursor.execute("INSERT INTO performanslar (oyuncu_id, reyting, gol, asist) VALUES (?, ?, ?, ?)", 
                   (p.oyuncu_id, p.reyting, p.gol, p.asist))
    conn.commit()
    conn.close()
    return {"mesaj": "Oyunuz başarıyla kaydedildi!"}

# YENİ: Herkesin oylarının ortalamasını getiren endpoint
@app.get("/istatistikler/{oyuncu_id}")
def istatistik_getir(oyuncu_id: int):
    conn = sqlite3.connect("halisaha.db")
    cursor = conn.cursor()
    # SQL ile ortalama reytingi ve toplam gol/asisti hesaplıyoruz
    cursor.execute("""
        SELECT AVG(reyting), SUM(gol), SUM(asist), COUNT(id) 
        FROM performanslar 
        WHERE oyuncu_id = ?
    """, (oyuncu_id,))
    res = cursor.fetchone()
    conn.close()
    
    return {
        "ortalama_reyting": round(res[0], 1) if res[0] else 0,
        "toplam_gol": res[1] if res[1] else 0,
        "toplam_asist": res[2] if res[2] else 0,
        "toplam_oy": res[3]
    }
