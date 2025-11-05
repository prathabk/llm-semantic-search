from flask import Flask, render_template, request, jsonify
import os
from services import OllamaService, TypesenseService
from services.similarity_service import SimilarityService

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

@app.route('/demo/techniques')
def demo_techniques():
    """Similarity techniques comparison demo"""
    return render_template('demo_techniques.html')

@app.route('/chunking')
def chunking():
    """Text chunking strategies explanation and demo"""
    return render_template('chunking.html')

@app.route('/demo/chunking')
def demo_chunking():
    """Interactive chunking strategies demo with Typesense"""
    return render_template('demo_chunking.html')

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

        # Check if collection exists and has data
        collection_exists = False
        document_count = 0
        try:
            collection_info = ts.get_collection_info()
            collection_exists = True
            document_count = collection_info.get('num_documents', 0)
        except:
            pass

        # Check Ollama
        ollama_health = OllamaService.check_ollama_availability()

        return jsonify({
            'success': True,
            'typesense': {
                'healthy': ts_health.get('healthy', False),
                'host': TYPESENSE_HOST,
                'port': TYPESENSE_PORT,
                'collection_name': COLLECTION_NAME,
                'collection_exists': collection_exists,
                'document_count': document_count,
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
        print("=== /api/store endpoint called ===")
        data = request.json
        print(f"Request data: {data}")

        documents = data.get('documents', [])
        recreate = data.get('recreate', True)

        print(f"Documents count: {len(documents)}")
        print(f"Recreate mode: {recreate}")

        if not documents:
            print("ERROR: No documents provided")
            return jsonify({'success': False, 'error': 'No documents provided'}), 400

        print(f"Connecting to Typesense at {TYPESENSE_HOST}:{TYPESENSE_PORT}")
        ts = TypesenseService(
            host=TYPESENSE_HOST,
            port=TYPESENSE_PORT,
            api_key=TYPESENSE_API_KEY,
            collection_name=COLLECTION_NAME
        )

        # Create/recreate collection
        if recreate:
            print("Creating/recreating collection...")
            # Clear existing data and create fresh collection
            collection_info = ts.create_collection()
            print(f"Collection created: {collection_info}")
        else:
            print("Append mode - checking if collection exists...")
            # Append mode: ensure collection exists, but don't recreate
            try:
                # Check if collection exists
                collection_info = ts.get_collection_info()
                print(f"Collection exists: {collection_info.get('name')}")
            except Exception as e:
                print(f"Collection doesn't exist, creating it: {e}")
                # Collection doesn't exist, create it
                collection_info = ts.create_collection()
                print(f"Collection created: {collection_info}")

        # Insert documents
        print("Inserting documents...")
        result = ts.insert_documents(documents)
        print(f"Insert result: {result}")

        response = {
            'success': True,
            'inserted': result['count'],
            'collection': COLLECTION_NAME
        }
        print(f"Sending response: {response}")
        return jsonify(response)

    except Exception as e:
        print(f"ERROR in /api/store: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/query', methods=['POST'])
def query_search():
    """Query Typesense with natural language"""
    try:
        print("=== /api/query endpoint called ===")
        data = request.json
        query = data.get('query', '')
        model = data.get('model', 'gemma3:1b')
        generative = data.get('generative', False)  # New flag for generative output
        per_page = data.get('per_page', 250)  # Allow custom per_page limit

        print(f"Query: '{query}', Model: {model}, Generative: {generative}, Per Page: {per_page}")

        if not query:
            print("ERROR: No query provided")
            return jsonify({'success': False, 'error': 'No query provided'}), 400

        # Initialize services
        print(f"Initializing Typesense connection to {TYPESENSE_HOST}:{TYPESENSE_PORT}")
        ts = TypesenseService(
            host=TYPESENSE_HOST,
            port=TYPESENSE_PORT,
            api_key=TYPESENSE_API_KEY,
            collection_name=COLLECTION_NAME
        )

        # Get collection schema
        try:
            print("Getting collection info...")
            collection_info = ts.get_collection_info()
            schema = collection_info.get('fields', [])
            print(f"Collection exists: {collection_info.get('name')}")
        except Exception as e:
            print(f"Warning: Could not get collection info: {e}")
            schema = {}

        # For wildcard query, skip LLM translation
        if query == '*':
            print("Wildcard query detected, skipping LLM translation")
            query_params = {'q': '*', 'filter_by': ''}
        else:
            # Initialize Ollama only if needed
            ollama = OllamaService(model=model)
            # Translate query to Typesense filter
            print("Translating query to filter...")
            query_params = ollama.translate_query_to_filter(query, schema)
            print(f"Query params: {query_params}")

        # Search Typesense
        print(f"Searching Typesense with q='{query_params.get('q')}', filter_by='{query_params.get('filter_by')}', per_page={per_page}")
        search_results = ts.search(
            q=query_params.get('q', '*'),
            filter_by=query_params.get('filter_by', ''),
            per_page=per_page
        )
        print(f"Search completed. Found: {search_results.get('found', 0)}, Hits: {len(search_results.get('hits', []))}")

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

        print("Query completed successfully")
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
        print(f"ERROR in /api/query: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/compare-techniques', methods=['POST'])
def compare_techniques():
    """Compare different similarity techniques"""
    try:
        data = request.json
        query = data.get('query', '')
        documents = data.get('documents', None)

        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400

        # Get results from all techniques
        results = SimilarityService.compare_all_methods(query, documents)

        # Get method information
        method_info = SimilarityService.get_method_info()

        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'method_info': method_info,
            'documents': documents if documents else SimilarityService.SAMPLE_DOCUMENTS
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sample-documents', methods=['GET'])
def get_sample_documents():
    """Get sample documents for similarity comparison"""
    try:
        return jsonify({
            'success': True,
            'documents': SimilarityService.SAMPLE_DOCUMENTS
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chunking/store', methods=['POST'])
def store_chunks():
    """Store chunks in Typesense using selected strategy"""
    try:
        data = request.json
        text = data.get('text', '')
        strategy = data.get('strategy', 'sentence')
        model = data.get('model', 'gemma3:1b')

        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400

        # Import chunking helper
        from services.chunking_service import ChunkingService

        # Get chunks based on strategy
        chunks = ChunkingService.chunk_text(text, strategy, model)

        # Store in Typesense with new collection
        ts = TypesenseService(
            host=TYPESENSE_HOST,
            port=TYPESENSE_PORT,
            api_key=TYPESENSE_API_KEY,
            collection_name='llm-chunking'
        )

        # Recreate collection (clears existing data)
        collection_info = ts.create_collection_for_chunks()

        # Prepare documents for Typesense
        documents = []
        for i, chunk in enumerate(chunks):
            documents.append({
                'id': str(i + 1),
                'chunk_id': i + 1,
                'text': chunk['text'],
                'strategy': strategy,
                'metadata': chunk.get('metadata', ''),
                'chunk_index': i
            })

        # Insert documents
        result = ts.insert_documents(documents)

        return jsonify({
            'success': True,
            'chunks': chunks,
            'count': len(chunks),
            'strategy': strategy,
            'collection': 'llm-chunking'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chunking/query', methods=['POST'])
def query_chunks():
    """Query stored chunks with a question"""
    try:
        data = request.json
        question = data.get('question', '')

        if not question:
            return jsonify({'success': False, 'error': 'No question provided'}), 400

        # Search in Typesense
        ts = TypesenseService(
            host=TYPESENSE_HOST,
            port=TYPESENSE_PORT,
            api_key=TYPESENSE_API_KEY,
            collection_name='llm-chunking'
        )

        # Perform semantic search
        search_results = ts.search(q=question, query_by='text', per_page=5)

        # Get top results
        hits = search_results.get('hits', [])

        if not hits:
            return jsonify({
                'success': True,
                'answer': 'No relevant chunks found to answer this question.',
                'chunks': [],
                'found': 0
            })

        # Extract relevant chunks
        relevant_chunks = []
        for hit in hits:
            doc = hit['document']
            relevant_chunks.append({
                'text': doc['text'],
                'chunk_id': doc['chunk_id'],
                'strategy': doc['strategy'],
                'metadata': doc.get('metadata', ''),
                'score': hit.get('text_match', 0)
            })

        # Generate answer using LLM
        ollama = OllamaService(model='gemma3:1b')
        context = '\n\n'.join([f"Chunk {c['chunk_id']}: {c['text']}" for c in relevant_chunks[:3]])

        prompt = f"""Based on the following context from a document, answer the question concisely.

Context:
{context}

Question: {question}

Answer:"""

        answer = ollama.generate_text(prompt)

        return jsonify({
            'success': True,
            'question': question,
            'answer': answer,
            'chunks': relevant_chunks,
            'found': len(hits)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9010)
