'''Purpose: to embed and retrieve teh data fetched from the pdf files'''

from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
import torch
import torch.nn.functional as F

class vectorize:
    def __init__(self, text):
        self.text = text

    def chunck_the_text(self, max_len=500):
        sentences = sent_tokenize(self.text)
        chunks = []
        chunk = ""

        for sentence in sentences:
            if len(chunk) + len(sentence) < max_len:
                chunk += " " + sentence
            else:
                chunks.append(chunk.strip())
                chunk = sentence
        
        chunks.append(chunk.strip())
        return chunks
    
    def get_embedding(self, chunks):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self.encoder.encode(chunks, convert_to_tensor=True)

    def search(self, query, top_k = 3):
        query_embedding = self.encoder.encode([query], convert_to_tensor=True)
        cos_scores = F.cosine_similarity(query_embedding, self.embeddings)
        top_results = torch.topk(cos_scores, k=top_k)

        res = []
        for scores, idx in zip(top_results.values, top_results.indices):
            res.append({
                "score":scores.item(),
                "chunk":self.chunks[idx]
            })
        return res

    def get_result(self, query):
        return self.search(query=query)


