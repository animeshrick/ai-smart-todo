from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

'''
Smart Search & Task Matching
What it does: Semantic search through tasks using embeddings.
Free AI Options:

    Sentence Transformers
    Universal Sentence Encoder
    Word2Vec (custom training)
'''

model = SentenceTransformer('all-MiniLM-L6-v2')


def semantic_task_search(query, tasks):
    # Get embeddings for query
    query_embedding = model.encode([query])

    # Get embeddings for all tasks
    task_texts = [f"{task.title} {task.description}" for task in tasks]
    task_embeddings = model.encode(task_texts)

    # Calculate similarities
    similarities = cosine_similarity(query_embedding, task_embeddings)[0]
    print(f"Onion_semantic_task_search_similarities: {similarities}")

    # Return top 5 most similar tasks
    top_indices = np.argsort(similarities)[::-1][:5]
    print(f"Onion_semantic_task_search: {top_indices}")

    return [(tasks[i], similarities[i]) for i in top_indices]