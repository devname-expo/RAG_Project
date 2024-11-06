import json
import google.generativeai as genai
import time 

from pinecone import Pinecone, ServerlessSpec
from pathlib import Path
import os

PINECONE_DEV_KEY = os.environ.get("PINECONE_DEV_KEY")
GEMINI_DEV_KEY = os.environ.get("GEMINI_DEV_KEY")

def read_docs(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def upload_embeddings(docs, key):
    genai.configure(api_key=GEMINI_DEV_KEY)
    pc = Pinecone(api_key=PINECONE_DEV_KEY)
    spec = ServerlessSpec(cloud="aws", region='us-east-1')
    index_name = 'semantic-search-gemini'

    # check if index already exists 
    if index_name not in pc.list_indexes().names():
        # if does not exist, create index
        pc.create_index(
            index_name,
            dimension=768,  
            metric='dotproduct', # cosine?
            spec=spec
        )
        # wait for index to be initialized
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)

    # connect to index
    index = pc.Index(index_name)
    time.sleep(1)

    for i, doc in enumerate(docs):
        res  = genai.embed_content(
            model="models/text-embedding-004",
            content=docs[i],
            task_type="retrieval_document",
            )

        index.upsert([(f'{key}_{i}', res['embedding'], {'text':doc})]
        )

if __name__ == '__main__':
    for filename in ['.local/output/docs1.json','.local/output/docs2.json']:
        p = Path(filename)
        upload_embeddings(read_docs(p), p.stem)

# print(index.describe_index_stats())
# pc.delete_index(index_name)
# time.sleep(2)
