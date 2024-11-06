from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai
import os

PINECONE_DEV_KEY = os.environ.get("PINECONE_DEV_KEY")
GEMINI_DEV_KEY = os.environ.get("GEMINI_DEV_KEY")


def create_context(question):
    """
    Create a context for a question by finding the most similar context from the pinecone index
    """
    pc = Pinecone(api_key=PINECONE_DEV_KEY)
    index = pc.Index('semantic-search-gemini')
    
    max_len=1800
    # Get the embeddings for the question
    q_embeddings  = genai.embed_content(
        model="models/text-embedding-004",
        content=question)
    
    # Get the distances from the embeddings
    res = index.query(vector=[q_embeddings['embedding']], top_k=5, include_metadata=True)
    results = []
    cur_len = 0
    for m in res.matches:
        text = m['metadata']['text']
        results.append(text)
 
    return r"\n\n###\n\n".join(results)

def answer_question(
    question="What is the R.31 reconnaissance aircraft?",
    model="gemini-1.5-flash-8b",
    debug=False,
    max_tokens=150,
    stop_sequence=None
):
    """
    Answer a question based on the most similar context from pinecone
    """

    genai.configure(api_key=GEMINI_DEV_KEY)

    context = create_context(question)
    model = genai.GenerativeModel(model)
    try:
        # Create a completions using the question and context
        message =  f"You are a chatbot for a Historical society and strictly answer the question based on the context below, and if the question can't be answered based on the context, say \"I'm sorry I cannot answer the question\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:"
        response = model.generate_content(message)

        return response.text
    except Exception as e:
        return ""
        
if __name__ == '__main__':
    print(answer_question('Which two companies created the R.31 reconnaissance aircraft?'))
    
