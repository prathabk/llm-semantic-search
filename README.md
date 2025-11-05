# Semantic Search with LLM Models

An interactive learning portal and demonstration of semantic search using Large Language Models (LLMs) and vector databases.

## 🌟 Features

- **Interactive Demos**: Full pipeline and query-only demonstrations
- **LLM-Powered**: Uses Ollama with Gemma3 models for text structuring and query translation
- **Vector Database**: Typesense for fast, scalable semantic search
- **Generative Answers**: Context-aware natural language responses
- **Beautiful UI**: Modern, responsive interface with syntax-highlighted JSON
- **Modular Architecture**: Reusable services and components

## 📋 Prerequisites

### 1. Python 3.8+

Check your Python version:
```bash
python3 --version
```

### 2. Typesense Server

Typesense is a fast, typo-tolerant search engine with vector search capabilities.

**Installation Options:**

#### Option A: Using Docker (Recommended)
```bash
docker run -d \
  -p 8108:8108 \
  -v $(pwd)/typesense-data:/data \
  typesense/typesense:27.1 \
  --data-dir /data \
  --api-key=vL1l1TOq2UYhPxKqJfvfWXvm0wIID6se \
  --enable-cors
```

#### Option B: Using Homebrew (macOS)
```bash
brew install typesense-server
typesense-server --data-dir=/tmp/typesense-data --api-key=vL1l1TOq2UYhPxKqJfvfWXvm0wIID6se
```

#### Option C: Binary Download
Download from [Typesense Downloads](https://typesense.org/downloads/) and run:
```bash
./typesense-server --data-dir=/tmp/typesense-data --api-key=vL1l1TOq2UYhPxKqJfvfWXvm0wIID6se
```

**Verify Typesense is Running:**
```bash
curl http://localhost:8108/health
# Should return: {"ok":true}
```

### 3. Ollama

Ollama is a tool to run LLMs locally.

**Installation:**

#### macOS/Linux:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Windows:
Download from [https://ollama.ai/download](https://ollama.ai/download)

**Pull Required Models:**
```bash
# Pull Gemma3 models (choose at least one)
ollama pull gemma3:270m   # Fastest, smallest
ollama pull gemma3:1b     # Balanced (recommended)
ollama pull gemma3:4b     # Most accurate
```

**Verify Ollama is Running:**
```bash
ollama list
# Should show the models you pulled
```

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd llm-semantic-search
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

The application uses environment variables for configuration. Default values are provided.

**Optional: Create `.env` file**
```bash
# .env
TYPESENSE_HOST=localhost
TYPESENSE_PORT=8108
TYPESENSE_API_KEY=vL1l1TOq2UYhPxKqJfvfWXvm0wIID6se
COLLECTION_NAME=llm-semantic-search
```

## 🏃 Running the Application

### 1. Start Prerequisites
Ensure both Typesense and Ollama are running:

```bash
# Check Typesense
curl http://localhost:8108/health

# Check Ollama
ollama list
```

### 2. Start the Flask Server
```bash
python3 app.py
```

Or with virtual environment:
```bash
./venv/bin/python app.py
```

The server will start on `http://localhost:9010`

### 3. Access the Application

Open your browser and navigate to:

- **Home**: http://localhost:9010/
- **Demo Hub**: http://localhost:9010/demo
- **Full Pipeline Demo**: http://localhost:9010/demo/full
- **Query Demo**: http://localhost:9010/demo/query

## 📚 Project Structure

```
llm-semantic-search/
├── app.py                      # Flask application & API routes
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── CLAUDE.md                   # Design guidelines
├── DEMO_README.md             # Detailed demo documentation
│
├── services/                   # Modular services
│   ├── __init__.py
│   ├── ollama_service.py      # LLM text processing
│   └── typesense_service.py   # Vector database operations
│
├── templates/                  # HTML templates
│   ├── index.html             # Landing page
│   ├── demo.html              # Demo hub
│   ├── demo_full.html         # Full pipeline demo
│   ├── demo_query.html        # Query-only demo
│   ├── vectors.html           # Learning: Vectors
│   ├── knowledge_encoding.html
│   ├── llm_overview.html
│   └── semantic_search.html
│
└── static/                     # Static assets
    ├── css/
    │   ├── style.css          # Main styles
    │   ├── carousel.css       # Slide carousel
    └── json-formatter.css # JSON syntax highlighting
    └── js/
        └── json-formatter.js  # JSON formatting library
```

## 🎯 Usage

### Full Pipeline Demo

1. **Input Data**: Enter unstructured text (one document per line)
2. **Select Model**: Choose Gemma3 model size
3. **Structure**: LLM converts text to structured JSON
4. **Store**: Save documents in Typesense
5. **Query**: Ask questions in natural language

### Query Demo

- Simplified interface for querying pre-loaded data
- Toggle between static and generative answers
- View formatted JSON responses
- Copy results to clipboard

### Example Queries

```
how many boys like blue color
who likes red color
girls who like biryani
find people who like curd rice
list all boys
```

## 🧪 Testing

Run the included test suite:

```bash
./venv/bin/python test_demo.py
```

This tests:
- Typesense connectivity
- Ollama availability
- Text structuring
- Document storage
- Natural language queries

## 🔧 API Endpoints

### Health Check
```bash
GET /api/health
```

### Get Available Models
```bash
GET /api/models
```

### Structure Text
```bash
POST /api/structure
Content-Type: application/json

{
  "texts": ["Balu is a boy. He likes blue color."],
  "model": "gemma3:1b"
}
```

### Store Documents
```bash
POST /api/store
Content-Type: application/json

{
  "documents": [{
    "name": "Balu",
    "gender": "boy",
    "likes": {"color": "blue", "food": "rice"}
  }]
}
```

### Query
```bash
POST /api/query
Content-Type: application/json

{
  "query": "how many boys like blue color",
  "model": "gemma3:1b",
  "generative": true
}
```

## 🐛 Troubleshooting

### Typesense Connection Error

**Error**: `Cannot connect to Typesense at localhost:8108`

**Solution**:
1. Check if Typesense is running: `curl http://localhost:8108/health`
2. Restart Typesense
3. Verify port 8108 is not in use

### Ollama Not Available

**Error**: `Ollama is not installed`

**Solution**:
1. Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
2. Verify installation: `ollama --version`
3. Pull models: `ollama pull gemma3:1b`

### Model Not Found

**Error**: `Model gemma3:1b not found`

**Solution**:
```bash
ollama pull gemma3:1b
ollama list  # Verify it's installed
```

### Port Already in Use

**Error**: `Address already in use: 9010`

**Solution**:
1. Find process: `lsof -i :9010`
2. Kill process: `kill -9 <PID>`
3. Or change port in `app.py`: `app.run(port=9011)`

## 🌐 Browser Compatibility

Tested and working on:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- **Typesense** - Fast, typo-tolerant search engine
- **Ollama** - Run LLMs locally
- **Gemma3** - Google's open language models
- **Flask** - Python web framework

---

**Built with ❤️ for learning and exploration of semantic search with LLMs**
