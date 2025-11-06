from flask import Flask, render_template, request, jsonify
import os
import time
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

@app.route('/vector-database-slides')
def vector_database_slides():
    """Typesense vector database slide presentation"""
    return render_template('vector_database_slides.html')

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

@app.route('/demo/chunking-strategies')
def demo_chunking_strategies():
    """Focused demo comparing all chunking strategies with Puducherry example"""
    return render_template('demo_chunking_strategies.html')

@app.route('/demo/typesense')
def demo_typesense():
    """Typesense vector similarity search demo"""
    return render_template('demo_typesense.html')

@app.route('/demo/typesense-gemma')
def demo_typesense_gemma():
    """Typesense similarity search demo with explicit Gemma embeddings"""
    return render_template('demo_typesense_gemma.html')

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

@app.route('/api/typesense-demo/index', methods=['POST'])
def typesense_demo_index():
    """Index documents with auto-embeddings for similarity search demo"""
    try:
        data = request.json
        documents = data.get('documents', [])
        mode = data.get('mode', 'clear')  # 'clear' or 'append'

        if not documents:
            return jsonify({'success': False, 'error': 'No documents provided'}), 400

        # Initialize Typesense service
        ts = TypesenseService(
            host=TYPESENSE_HOST,
            port=TYPESENSE_PORT,
            api_key=TYPESENSE_API_KEY,
            collection_name='llm_semsim'
        )

        # Create or check collection based on mode
        if mode == 'clear':
            # Clear & Store: Recreate collection with auto-embedding
            ts.create_auto_embedding_collection(model_name='ts/all-MiniLM-L12-v2')
        else:
            # Append: Check if collection exists, create if not
            try:
                ts.get_collection_info()
            except:
                # Collection doesn't exist, create it
                ts.create_auto_embedding_collection(model_name='ts/all-MiniLM-L12-v2')

        # Prepare documents (no need to generate embeddings manually!)
        docs_to_insert = []
        for i, text in enumerate(documents):
            docs_to_insert.append({
                'id': str(int(time.time() * 1000) + i),  # Unique ID using timestamp
                'text': text
                # Typesense will automatically generate embeddings!
            })

        # Insert documents
        result = ts.insert_documents(docs_to_insert)

        # Get total document count
        collection_info = ts.get_collection_info()
        total_docs = collection_info.get('num_documents', len(documents))

        # Generate Python code snippet
        mode_comment = "# Mode: Clear & Store - Recreates collection" if mode == 'clear' else "# Mode: Append - Adds to existing collection"
        code_snippet = f"""# Index documents in Typesense with auto-embeddings
{mode_comment}
# Typesense automatically generates embeddings using built-in model!
import requests
import json
import time

documents = {documents}

# Prepare documents (Typesense will auto-generate embeddings)
docs_to_insert = []
for i, text in enumerate(documents):
    docs_to_insert.append({{
        'id': str(int(time.time() * 1000) + i),
        'text': text
        # No embedding field needed - Typesense does it automatically!
    }})

# Import documents to Typesense
import_data = '\\n'.join([json.dumps(doc) for doc in docs_to_insert])

response = requests.post(
    'http://{TYPESENSE_HOST}:{TYPESENSE_PORT}/collections/llm_semsim/documents/import',
    headers={{'X-TYPESENSE-API-KEY': '{TYPESENSE_API_KEY}'}},
    data=import_data
)

print(f"Indexed {{len(documents)}} documents")
print(f"Total documents in collection: {total_docs}")
print("Embeddings generated automatically by Typesense!")"""

        return jsonify({
            'success': True,
            'count': len(documents),
            'total_docs': total_docs,
            'mode': mode,
            'model': 'ts/all-MiniLM-L12-v2',
            'code': code_snippet
        })

    except Exception as e:
        print(f"Error in typesense_demo_index: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/typesense-demo/search', methods=['POST'])
def typesense_demo_search():
    """Search documents using semantic similarity with auto-embeddings"""
    try:
        data = request.json
        query = data.get('query', '')

        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400

        # Initialize Typesense service
        ts = TypesenseService(
            host=TYPESENSE_HOST,
            port=TYPESENSE_PORT,
            api_key=TYPESENSE_API_KEY,
            collection_name='llm_semsim'
        )

        # Perform semantic search (Typesense auto-generates query embedding!)
        search_results = ts.semantic_search(query, k=5)

        # Extract results with scores
        results = []
        for hit in search_results.get('hits', []):
            doc = hit['document']
            # Vector distance is returned in vector_distance field
            # Convert to similarity score (1 / (1 + distance))
            distance = hit.get('vector_distance', 0)
            similarity_score = 1 / (1 + distance)

            results.append({
                'text': doc['text'],
                'score': similarity_score,
                'distance': distance
            })

        # Generate Python code snippet
        code_snippet = f"""# Search documents using semantic similarity
# Typesense automatically generates embeddings for your query!
import requests

query = "{query}"

# Search in Typesense (auto-generates query embedding)
response = requests.get(
    'http://{TYPESENSE_HOST}:{TYPESENSE_PORT}/collections/llm_semsim/documents/search',
    headers={{'X-TYPESENSE-API-KEY': '{TYPESENSE_API_KEY}'}},
    params={{
        'q': query,
        'query_by': 'embedding',
        'exclude_fields': 'embedding',
        'per_page': 5
    }}
)

results = response.json()
print(f"Found {{results['found']}} results")

for hit in results['hits']:
    distance = hit.get('vector_distance', 0)
    score = 1 / (1 + distance)
    print(f"Score: {{score:.3f}} - {{hit['document']['text']}}")"""

        return jsonify({
            'success': True,
            'results': results,
            'found': len(results),
            'code': code_snippet,
            'raw_response': search_results
        })

    except Exception as e:
        print(f"Error in typesense_demo_search: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/typesense-gemma/index', methods=['POST'])
def typesense_gemma_index():
    """Index documents with explicit Ollama embedding model"""
    try:
        data = request.json
        documents = data.get('documents', [])
        mode = data.get('mode', 'clear')  # 'clear' or 'append'
        model = data.get('model', 'nomic-embed-text')  # Selected embedding model

        if not documents:
            return jsonify({'success': False, 'error': 'No documents provided'}), 400

        # Initialize services
        ollama = OllamaService(model=model)
        ts = TypesenseService(
            host=TYPESENSE_HOST,
            port=TYPESENSE_PORT,
            api_key=TYPESENSE_API_KEY,
            collection_name='llm_semsim_gemma'
        )

        # Generate first embedding to get dimension
        print(f"Generating embedding with model: {model}")
        first_embedding = ollama.generate_embedding(documents[0], model=model)
        embedding_dim = len(first_embedding)
        print(f"Embedding dimension: {embedding_dim}")

        # Create or check collection based on mode
        if mode == 'clear':
            # Clear & Store: Recreate collection
            ts.create_vector_collection(embedding_dim=embedding_dim)
        else:
            # Append: Check if collection exists, create if not
            try:
                ts.get_collection_info()
            except:
                # Collection doesn't exist, create it
                ts.create_vector_collection(embedding_dim=embedding_dim)

        # Prepare documents with embeddings
        docs_with_embeddings = []
        for i, text in enumerate(documents):
            print(f"Generating embedding for document {i+1}/{len(documents)}")
            embedding = ollama.generate_embedding(text, model=model)
            docs_with_embeddings.append({
                'id': str(int(time.time() * 1000) + i),  # Unique ID using timestamp
                'text': text,
                'embedding': embedding
            })

        # Insert documents
        result = ts.insert_documents(docs_with_embeddings)

        # Get total document count
        collection_info = ts.get_collection_info()
        total_docs = collection_info.get('num_documents', len(documents))

        # Generate Python code snippet
        mode_comment = "# Mode: Clear & Store - Recreates collection" if mode == 'clear' else "# Mode: Append - Adds to existing collection"
        code_snippet = f"""# Index documents with explicit Gemma embeddings
{mode_comment}
# Model: {model}
import requests
import time

documents = {documents}

# Generate embeddings using Ollama with {model}
docs_with_embeddings = []
for i, text in enumerate(documents):
    # Call Ollama API to generate embedding
    response = requests.post(
        'http://localhost:11434/api/embeddings',
        json={{
            'model': '{model}',
            'prompt': text
        }}
    )
    embedding = response.json()['embedding']

    docs_with_embeddings.append({{
        'id': str(int(time.time() * 1000) + i),
        'text': text,
        'embedding': embedding
    }})

# Import documents to Typesense
import json
import_data = '\\n'.join([json.dumps(doc) for doc in docs_with_embeddings])

response = requests.post(
    'http://{TYPESENSE_HOST}:{TYPESENSE_PORT}/collections/llm_semsim_gemma/documents/import',
    headers={{'X-TYPESENSE-API-KEY': '{TYPESENSE_API_KEY}'}},
    data=import_data
)

print(f"Indexed {{len(documents)}} documents using {model}")
print(f"Embedding dimension: {embedding_dim}")
print(f"Total documents in collection: {total_docs}")"""

        return jsonify({
            'success': True,
            'count': len(documents),
            'total_docs': total_docs,
            'mode': mode,
            'model': model,
            'embedding_dim': embedding_dim,
            'code': code_snippet
        })

    except Exception as e:
        print(f"Error in typesense_gemma_index: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/typesense-gemma/search', methods=['POST'])
def typesense_gemma_search():
    """Search documents using explicit Ollama embedding model"""
    try:
        data = request.json
        query = data.get('query', '')
        model = data.get('model', 'nomic-embed-text')  # Must match the model used for indexing

        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400

        # Initialize services
        ollama = OllamaService(model=model)
        ts = TypesenseService(
            host=TYPESENSE_HOST,
            port=TYPESENSE_PORT,
            api_key=TYPESENSE_API_KEY,
            collection_name='llm_semsim_gemma'
        )

        # Log collection info for debugging
        try:
            collection_info = ts.get_collection_info()
            print(f"Collection: {collection_info.get('name')}, Documents: {collection_info.get('num_documents')}")
        except Exception as e:
            print(f"Could not get collection info: {e}")

        # Generate query embedding using the same model
        print(f"Generating query embedding with model: {model}")
        query_embedding = ollama.generate_embedding(query, model=model)
        print(f"Query embedding dimension: {len(query_embedding)}")

        # Perform vector search
        search_results = ts.vector_search(query_embedding, k=5)

        # Extract results with scores
        results = []
        for hit in search_results.get('hits', []):
            doc = hit['document']
            # Vector distance is returned in vector_distance field
            # Convert to similarity score (1 / (1 + distance))
            distance = hit.get('vector_distance', 0)
            similarity_score = 1 / (1 + distance)

            results.append({
                'text': doc['text'],
                'score': similarity_score,
                'distance': distance
            })

        # Generate Python code snippet
        code_snippet = f"""# Search documents using explicit Gemma embeddings
# Model: {model}
import requests

query = "{query}"

# Generate query embedding using Ollama with {model}
response = requests.post(
    'http://localhost:11434/api/embeddings',
    json={{
        'model': '{model}',
        'prompt': query
    }}
)
query_embedding = response.json()['embedding']

# Format vector query for Typesense
embedding_str = ','.join([str(x) for x in query_embedding])
vector_query = f'embedding:([{{embedding_str}}], k:5)'

# Search in Typesense using vector similarity
response = requests.get(
    'http://{TYPESENSE_HOST}:{TYPESENSE_PORT}/collections/llm_semsim_gemma/documents/search',
    headers={{'X-TYPESENSE-API-KEY': '{TYPESENSE_API_KEY}'}},
    params={{
        'q': '*',
        'vector_query': vector_query,
        'exclude_fields': 'embedding'
    }}
)

results = response.json()
print(f"Found {{results['found']}} results using {model}")

for hit in results['hits']:
    distance = hit.get('vector_distance', 0)
    score = 1 / (1 + distance)
    print(f"Score: {{score:.3f}} - {{hit['document']['text']}}")"""

        return jsonify({
            'success': True,
            'results': results,
            'found': len(results),
            'model': model,
            'code': code_snippet,
            'raw_response': search_results
        })

    except Exception as e:
        print(f"Error in typesense_gemma_search: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/typesense-gemma/list', methods=['GET'])
def typesense_gemma_list():
    """List all documents in the collection for debugging"""
    try:
        # Initialize Typesense service
        ts = TypesenseService(
            host=TYPESENSE_HOST,
            port=TYPESENSE_PORT,
            api_key=TYPESENSE_API_KEY,
            collection_name='llm_semsim_gemma'
        )

        # Get all documents
        search_results = ts.search(q='*', query_by='text', per_page=250)

        documents = []
        for hit in search_results.get('hits', []):
            doc = hit['document']
            documents.append({
                'id': doc.get('id'),
                'text': doc.get('text')
            })

        return jsonify({
            'success': True,
            'total': search_results.get('found', 0),
            'documents': documents
        })

    except Exception as e:
        print(f"Error in typesense_gemma_list: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9010)
