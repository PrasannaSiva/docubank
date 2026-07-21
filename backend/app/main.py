import shutil, uuid
from dotenv import load_dotenv
from fastapi import UploadFile,FastAPI
from app.rag.ingest import ingest_pdf
from pydantic import BaseModel
from app.rag.chain import answer


load_dotenv()

app = FastAPI(title="Docubank API")

class ChatRequest(BaseModel):
    question: str
    doc_id: str

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/chat")
def chat(req:ChatRequest):
    return answer(req.question, req.doc_id)

@app.post("/upload")
async def upload(file: UploadFile):
    doc_id = str(uuid.uuid4())
    tmp_path = f"/tmp/{doc_id}.pdf"
    with open(tmp_path,"wb") as f:
        shutil.copyfileobj(file.file,f)
    chunk_count = ingest_pdf(tmp_path,doc_id)
    return {"doc_id": doc_id, "chunks": chunk_count} 