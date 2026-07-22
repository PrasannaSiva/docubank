from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma


CHROMA_DIR = "chroma_db"

def ingest_pdf(file_path:str,doc_id:str) -> int:
    pages = PyPDFLoader(file_path).load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=150)
    chunks = splitter.split_documents(pages)
    
    for c in chunks:
        c.metadata['doc_id'] = doc_id
    
    Chroma.from_documents(
        documents = chunks,
        embedding = OpenAIEmbeddings(model="text-embedding-3-small"),
        persist_directory = CHROMA_DIR
    )
    
    return len(chunks)

def delete_doc_chunks(doc_id:str):
    db = Chroma(
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
        persist_directory=CHROMA_DIR,
    )
    db.delete(where={"doc_id": doc_id})

