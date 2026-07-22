import sqlite3
from datetime import datetime

DB_PATH = "docubank.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
         CREATE TABLE IF NOT EXISTS documents(
                 doc_id TEXT PRIMARY KEY,
                 filename TEXT NOT NULL,
                 chunk_count INTEGER,
                 uploaded_at TEXT
                 )"""
                 )
    conn.commit()
    conn.close()


def add_document(doc_id:str,filename:str,chunk_count:int):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO documents values (?,?,?,?)",
                 (doc_id,filename,chunk_count,datetime.now().isoformat())
                 )
    conn.commit()
    conn.close()


def list_documents():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT doc_id, filename, chunk_count,uploaded_at from documents ORDER BY uploaded_at desc"
    ).fetchall()
    conn.close()
    return [
        {"doc_id":r[0],"filename":r[1],"chunk_count":r[2],"uploaded_at":r[3]}
        for r in rows
    ]

    
def delete_document(doc_id:str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "DELETE FROM documents where doc_id = ?",
        (doc_id,),
    )
    conn.commit()
    conn.close()