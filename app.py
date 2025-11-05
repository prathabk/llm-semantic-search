from flask import Flask, render_template, request, jsonify
import os
from services import OllamaService, TypesenseService

app = Flask(__name__)

# Configuration
TYPESENSE_HOST = os.getenv('TYPESENSE_HOST', 'localhost')
TYPESENSE_PORT = int(os.getenv('TYPESENSE_PORT', 8108))
TYPESENSE_API_KEY = os.getenv('TYPESENSE_API_KEY', 'vL1l1TOq2UYhPxKqJfvfWXvm0wIID6se')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'llm-semantic-search')

@app.route('/')
def index():
    """Main landing page with navigation to all concepts"""
    return render_template('index.html')

@app.route('/vectors')
def vectors():
    """Vectors concept explanation page"""
    return render_template('vectors.html')

@app.route('/knowledge-encoding')
def knowledge_encoding():
    """Knowledge encoding - vectors and embeddings combined"""
    return render_template('knowledge_encoding.html')

@app.route('/llm-overview')
def llm_overview():
    """LLM fundamentals - how large language models work"""
    return render_template('llm_overview.html')

@app.route('/embeddings')
def embeddings():
    """Embeddings concept explanation page"""
    return render_template('embeddings.html')

@app.route('/llm-models')
def llm_models():
    """LLM models with Ollama explanation page"""
    return render_template('llm_models.html')

@app.route('/vector-database')
def vector_database():
    """Vector database (Typesense) explanation page"""
    return render_template('vector_database.html')

@app.route('/semantic-search')
def semantic_search():
    """Semantic search demonstration page"""
    return render_template('semantic_search.html')

@app.route('/demo')
def demo():
    """Demo landing page with list of all demos"""
    return render_template('demo.html')

@app.route('/demo/full')
def demo_full():
    """Full pipeline demo - structure, store, and query"""
    return render_template('demo_full.html')

@app.route('/demo/query')
def demo_query():
    """Query-only demo - focused search experience"""
    return render_template('demo_query.html')

# API Endpoints

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available Ollama models"""
    try:
        models = OllamaService.get_available_models()
        return jsonify({'success': True, 'models': models})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check Typesense and Ollama health"""
    try:
        # Check Typesense
        ts = TypesenseService(
            host=TYPESENSE_HOST,
            port=TYPESENSE_PORT,
            api_key=TYPESENSE_API_KEY,
            collection_name=COLLECTION_NAME
        )
        ts_health = ts.health_check()

        # Check Ollama
        ollama_health = OllamaService.check_ollama_availability()

        return jsonify({
            'success': True,
            'typesense': {
                'healthy': ts_health.get('healthy', False),
                'host': TYPESENSE_HOST,
                'port': TYPESENSE_PORT,
                'error': ts_health.get('error')
            },
            'ollama': {
                'available': ollama_health.get('available', False),
                'error': ollama_health.get('error')
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/structure', methods=['POST'])
def structure_texts():
    """Structure unstructured texts using LLM"""
    try:
        data = request.json
        texts = data.get('texts', [])
        model = data.get('model', 'gemma3:1b')
        schema_hint = data.get('schema_hint')

        if not texts:
            return jsonify({'success': False, 'error': 'No texts provided'}), 400

        ollama = OllamaService(model=model)
        structured_data = ollama.structure_batch(texts, schema_hint)

        return jsonify({
            'success': True,
            'data': structured_data,
            'count': len(structured_data),
            'model': model
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/store', methods=['POST'])
def store_documents():
    """Store structured documents in Typesense"""
    try:
        data = request.json
        documents = data.get('documents', [])
        recreate = data.get('recreate', True)

        if not documents:
            return jsonify({'success': False, 'error': 'No documents provided'}), 400

        ts = TypesenseService(
            host=TYPESENSE_HOST,
            port=TYPESENSE_PORT,
            api_key=TYPESENSE_API_KEY,
            collection_name=COLLECTION_NAME
        )

        # Create/recreate collection
        if recreate:
            collection_info = ts.create_collection()

        # Insert documents
        result = ts.insert_documents(documents)

        return jsonify({
            'success': True,
            'inserted': result['count'],
            'collection': COLLECTION_NAME
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/query', methods=['POST'])
def query_search():
    """Query Typesense with natural language"""
    try:
        data = request.json
        query = data.get('query', '')
        model = data.get('model', 'gemma3:1b')
        generative = data.get('generative', False)  # New flag for generative output

        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400

        # Initialize services
        ollama = OllamaService(model=model)
        ts = TypesenseService(
            host=TYPESENSE_HOST,
            port=TYPESENSE_PORT,
            api_key=TYPESENSE_API_KEY,
            collection_name=COLLECTION_NAME
        )

        # Get collection schema
        try:
            collection_info = ts.get_collection_info()
            schema = collection_info.get('fields', [])
        except:
            schema = {}

        # Translate query to Typesense filter
        query_params = ollama.translate_query_to_filter(query, schema)

        # Search Typesense
        search_results = ts.search(
            q=query_params.get('q', '*'),
            filter_by=query_params.get('filter_by', '')
        )

        # Generate answer
        hits = search_results.get('hits', [])
        found_count = search_results.get('found', 0)

        if generative and found_count > 0:
            # Use LLM to generate natural language answer
            answer = ollama.generate_natural_answer(query, hits, found_count)
        else:
            # Static constructed answer
            if found_count == 0:
                answer = "No results found for your query."
            else:
                # Collect all names (or extract from text if no name field)
                names = []
                for hit in hits:
                    doc = hit['document']
                    name = doc.get('name')
                    if name:
                        names.append(name)
                    else:
                        # Try to extract name from text (first word that's likely a name)
                        text = doc.get('text', '')
                        words = text.split()
                        if words:
                            # First word is often the name
                            potential_name = words[0]
                            names.append(potential_name)

                if names:
                    # Show up to 3 names, add ellipsis if more
                    if len(names) <= 3:
                        answer = f"Found {found_count}: {', '.join(names)}"
                    else:
                        answer = f"Found {found_count}: {', '.join(names[:3])}, ..."
                else:
                    answer = f"Found {found_count} matching documents"

        return jsonify({
            'success': True,
            'query': query,
            'typesense_params': query_params,
            'results': search_results,
            'answer': answer,
            'found': found_count,
            'generative': generative
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9010)
