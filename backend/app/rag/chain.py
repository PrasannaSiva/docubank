from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma



PROMPT = """
You are a banking document assistant. Answer the question only using the content below.
If you annot find the answer, then say you dont know about the asnwer

content:
{content}

Question:{Question}

Answer:
"""


def answer(question:str, doc_id:str) -> dict:
    db = Chroma(
        persist_directory = "chroma_db",
        embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
    )
    
    results = db.similarity_search_with_score(
        question,k=4,filter={"doc_id":doc_id}
    )
    
    context = "\n\n\n---\n\n\n".join(doc.page_content for doc,_ in results)
    
    citations = [
        {"page": doc.metadata.get("page") , "score": round(float(s),3)}
        for doc,s in results
    ]
    
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    response = llm.invoke(PROMPT.format(content=context,Question=question))
    
    return {"answer": response.content, "citations": citations}