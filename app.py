from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9010)
