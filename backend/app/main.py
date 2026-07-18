from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
app = FastAPI(title="Docubank API")

@app.get("/health")
def health():
    return {"status":"ok"}