from flask import Flask, jsonify, request
from marshmallow import ValidationError
from transformer import score, cache_corpus_embeddings, remove_cached_embeddings
from schema import DatasetsSchema, IdsSchema

app = Flask(__name__)

@app.route('/search')
def perform_search() -> tuple[str, int]:
    term = request.args.get('term') or ''
    possible = (request.args.get('possible') or '').split(',')

    if (len(term) == 0):
        return []

    return jsonify(score(term, possible))

@app.route('/corpus', methods=['POST'])
def generate_embeddings() -> tuple[str, int]:
    request_data = request.json
    schema = DatasetsSchema()

    try:
        result = schema.load(request_data)
        datasets = result['datasets'] or []

        if (len(datasets) > 0):
            cache_corpus_embeddings(datasets)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    return '', 204

@app.route('/corpus', methods=['DELETE'])
def remove_embeddings() -> tuple[str, int]:
    request_data = request.json
    schema = IdsSchema()

    try:
        result = schema.load(request_data)
        ids = result['ids'] or []

        if (len(ids) > 0):
            remove_cached_embeddings(ids)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    return '', 204
    

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)
