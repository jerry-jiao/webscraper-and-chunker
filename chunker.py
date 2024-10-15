from typing import List
from openai import OpenAI
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(
  api_key=openai_api_key
)

THRESHOLD = 750

def break_up_content(content: str):
  by_newline = list(filter(lambda s: len(s), map(str.strip, content.split('\n'))))
  return by_newline

def chunk(content: str):
  pieces = break_up_content(content)
  embeddings = get_embeddings(pieces)
  neighboring_similarities = get_neighboring_similarities(embeddings)

  merged = merge_chunks_by_similarity(pieces, neighboring_similarities)

  return merged

def get_embeddings(content: List[str]):
  return list(map(lambda e: e.embedding, client.embeddings.create(
    input=content,
    model='text-embedding-3-small'
  ).data))

def get_neighboring_similarities(embeddings):
  return [cosine_similarity(embeddings[i], embeddings[i+1]) for i in range(0, len(embeddings) - 1)]

def cosine_similarity(embedding1, embedding2):
  dot_product = np.dot(embedding1, embedding2)
  norm1 = np.linalg.norm(embedding1)
  norm2 = np.linalg.norm(embedding2)

  return dot_product / (norm1 * norm2)

def merge_chunks_by_similarity(chunks, similarities):
  sorted_similarities = sorted(enumerate(similarities), key=lambda s: s[1], reverse=True)

  merged = chunks.copy()

  for i, _ in sorted_similarities:
    combined_string = merged[i] + "\n" + merged[i+1]
    if len(combined_string) <= THRESHOLD:
      # Merge the strings
      merged[i] = combined_string
      merged.pop(i+1)

      for j in range(len(sorted_similarities)):
        if sorted_similarities[j][0] > i:
          sorted_similarities[j] = (sorted_similarities[j][0] - 1, sorted_similarities[j][1])
  
  return merged