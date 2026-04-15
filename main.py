from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Güneyin Dantelleri - API (Final)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Oyuncu(BaseModel):
    isim: str
    numara: int
    pozisyon: str

class Performans(BaseModel):
    oyuncu_id: int
    reyting: float
    gol: int
    asist: int

def veritabanini_hazirla():
    conn = sqlite3.connect("halisaha.db")
    cursor = conn.cursor()
    # Oyuncular Tablosu
    cursor.execute('''CREATE TABLE IF NOT EXISTS oyuncular (
            id INTEGER PRIMARY KEY AUTOINCREMENT, isim TEXT, numara INTEGER, pozisyon TEXT)''')
    # Performanslar (Maç Sonu) Tablosu
    cursor.execute('''CREATE TABLE IF NOT EXISTS performanslar (
            id INTEGER PRIMARY KEY AUTOINCREMENT, oyuncu_id INTEGER, reyting REAL, gol INTEGER, asist INTEGER)''')
    conn.commit()
    conn.close()

veritabanini_hazirla()

@app.get("/oyuncular")
def oyunculari_getir():
    conn = sqlite3.connect("halisaha.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM oyuncular")
    satirlar = cursor.fetchall()
    conn.close()
    
    oyuncular_listesi = [{"id": s[0], "isim": s[1], "numara": s[2], "pozisyon": s[3]} for s in satirlar]
    return oyuncular_listesi

@app.post("/oyuncular")
def oyuncu_ekle(yeni_oyuncu: Oyuncu):
    conn = sqlite3.connect("halisaha.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO oyuncular (isim, numara, pozisyon) VALUES (?, ?, ?)", 
                   (yeni_oyuncu.isim, yeni_oyuncu.numara, yeni_oyuncu.pozisyon))
    conn.commit()
    conn.close()
    return {"mesaj": "Oyuncu eklendi!"}

@app.post("/performanslar")
def performans_ekle(p: Performans):
    conn = sqlite3.connect("halisaha.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO performanslar (oyuncu_id, reyting, gol, asist) VALUES (?, ?, ?, ?)", 
                   (p.oyuncu_id, p.reyting, p.gol, p.asist))
    conn.commit()
    conn.close()
    return {"mesaj": "Performans kaydedildi!"}