# Semantic Search with LLM - Learning Portal

An interactive web-based course for learning semantic search concepts using Large Language Models.

## Features

- **Vectors**: Interactive visualizations demonstrating vector mathematics and operations
- **Embeddings**: Text-to-vector conversion concepts (coming soon)
- **LLM Models**: Integration with Ollama for local LLM usage (coming soon)
- **Vector Database**: Using Typesense for vector storage and search (coming soon)
- **Semantic Search Demo**: Practical implementation (coming soon)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask development server:

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── index.html        # Home page with navigation
│   ├── vectors.html      # Interactive vectors tutorial
│   ├── embeddings.html   # Embeddings concept page
│   ├── llm_models.html   # LLM models page
│   ├── vector_database.html  # Vector DB page
│   └── semantic_search.html  # Demo page
└── static/
    └── css/
        └── style.css     # Styling
```

## Concepts Covered

1. **Vectors**: Mathematical foundation with interactive 2D visualizations
2. **Embeddings**: Converting text to numerical representations
3. **LLM Models**: Using Ollama for local language model operations
4. **Vector Databases**: Efficient storage and retrieval with Typesense
5. **Semantic Search**: Putting it all together

## Technologies

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (Canvas API for visualizations)
- **LLM**: Ollama (planned)
- **Vector DB**: Typesense (planned)
