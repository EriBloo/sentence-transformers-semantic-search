from sentence_transformers import SentenceTransformer, util
import torch
import pickle
import os
import numpy
from type import Dataset, Embedding, Score
from helper import pluck
model_path = r'/app/model'
corpus_embeddings_path = '/app/corpus_cache.pkl'

def score(search: str, possible: list[str]) -> list[Score]:
    model = SentenceTransformer(model_path)
    embeddings = __load_corpus_embeddings()
    filtered = [embedding for embedding in embeddings if embedding['id'] in possible]

    if len(filtered) == 0:
        return []

    ids = pluck(filtered, 'id')
    corpus_embeddings = numpy.array(pluck(filtered, 'embedding'))
    query_embedding = model.encode(search)

    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=min(len(filtered), 10))

    results = []

    for score, idx in zip(top_results[0], top_results[1]):
        results.append({'id': ids[idx], 'score': f'{score:.4f}'})

    return results
    
def cache_corpus_embeddings(datasets: list[Dataset]) -> None:
    model = SentenceTransformer(model_path)

    ids = pluck(datasets, 'id')
    names = pluck(datasets, 'name')

    corpus_embeddings = model.encode(names, convert_to_numpy=True)

    cached = __load_corpus_embeddings()
    filtered = [embedding for embedding in cached if embedding['id'] not in ids]

    save_ids = ids
    save_embeddings = corpus_embeddings

    if (len(filtered) > 0):
        save_ids += pluck(filtered, 'id')
        save_embeddings += pluck(filtered, 'embedding')

    with open(corpus_embeddings_path, 'wb') as fOut:
        pickle.dump({'ids': save_ids, 'embeddings': save_embeddings}, fOut)

def __load_corpus_embeddings() -> list[Embedding]:
    if not os.path.exists(corpus_embeddings_path):
        return []

    with open(corpus_embeddings_path, 'rb') as fIn:
        cache_data = pickle.load(fIn)
        ids = cache_data['ids']
        embeddings = cache_data['embeddings']

    return [{'id': z[0], 'embedding': z[1]} for z in zip(ids, embeddings)]

