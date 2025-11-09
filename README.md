# Semantic Search with LLM Models

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)

An **interactive learning portal** and demonstration of semantic search using Large Language Models (LLMs) and vector databases. Built for education, exploration, and hands-on learning about modern search technologies.

> **Perfect for**: Students, developers, and anyone interested in learning about semantic search, vector databases, and LLMs through interactive examples.

## 📑 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Running the Application](#-running-the-application)
- [Project Structure](#-project-structure)
- [Usage Examples](#-usage-examples)
- [Using with AI Tools (Claude Code)](#-using-with-ai-tools-claude-code)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## 🌟 Features

- **🎓 Interactive Learning Portal**: Slide-based presentations for key concepts (vectors, embeddings, LLMs, vector databases)
- **🔍 Semantic Search Demos**: Multiple interactive demonstrations showing real-world applications
- **🤖 LLM-Powered**: Uses Ollama with Gemma3 models for text structuring and query translation
- **💾 Vector Database**: Typesense for fast, scalable semantic search
- **🧬 Generative Answers**: Context-aware natural language responses
- **🎨 Beautiful UI**: Modern, responsive interface with slide carousel navigation
- **📦 Modular Architecture**: Reusable services and clean separation of concerns
- **🔧 Educational**: Every concept explained with visual demonstrations

## 🚀 Quick Start

**TL;DR**: Get up and running in 5 minutes:

```bash
# 1. Clone the repository
git clone https://github.com/your-username/llm-semantic-search.git
cd llm-semantic-search

# 2. Install dependencies
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Start Typesense (Docker - easiest)
docker run -d -p 8108:8108 -v $(pwd)/typesense-data:/data \
  typesense/typesense:27.1 --data-dir /data \
  --api-key=vL1l1TOq2UYhPxKqJfvfWXvm0wIID6se --enable-cors

# 4. Install Ollama and pull a model
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull gemma3:1b

# 5. Run the app
python3 app.py

# 6. Open your browser
# Navigate to: http://localhost:9010
```

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

# Optional: Pull embedding models for advanced demos
ollama pull nomic-embed-text  # For explicit embeddings demo
```

**Verify Ollama is Running:**
```bash
ollama list
# Should show the models you pulled
```

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/llm-semantic-search.git
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

> **Note**: For production use, change the API key to a secure, randomly generated value.

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

- **🏠 Home**: http://localhost:9010/
- **📊 Learning Concepts**: Interactive slide presentations on vectors, embeddings, LLMs
- **🎮 Demo Hub**: http://localhost:9010/demo
- **🔍 Full Pipeline Demo**: http://localhost:9010/demo/full
- **⚡ Query Demo**: http://localhost:9010/demo/query
- **📝 Log Analysis Demo**: http://localhost:9010/demo/logs

## 📚 Project Structure

```
llm-semantic-search/
├── app.py                      # Flask application & API routes
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── CLAUDE.md                   # Design & content guidelines (for AI tools)
├── CONTRIBUTING.md             # Contribution guidelines
├── DEMO_README.md             # Detailed demo documentation
├── LICENSE                     # MIT License
│
├── services/                   # Modular services
│   ├── __init__.py
│   ├── ollama_service.py      # LLM text processing & embeddings
│   ├── typesense_service.py   # Vector database operations
│   ├── similarity_service.py  # Similarity algorithms comparison
│   └── chunking_service.py    # Text chunking strategies
│
├── templates/                  # HTML templates (Jinja2)
│   ├── index.html             # Landing page
│   ├── demo.html              # Demo hub
│   ├── demo_full.html         # Full pipeline demo
│   ├── demo_query.html        # Query-only demo
│   ├── demo_logs.html         # Log analysis demo
│   ├── demo_chunking.html     # Chunking strategies demo
│   ├── vectors.html           # Learning: Vectors (slide format)
│   ├── knowledge_encoding.html # Learning: Knowledge encoding
│   ├── llm_overview.html      # Learning: LLM fundamentals
│   └── semantic_search.html   # Learning: Semantic search
│
└── static/                     # Static assets
    ├── css/
    │   ├── style.css          # Main styles
    │   ├── carousel.css       # Slide carousel navigation
    │   └── json-formatter.css # JSON syntax highlighting
    └── js/
        └── json-formatter.js  # JSON formatting library
```

## 🎯 Usage Examples

### Full Pipeline Demo

1. **Input Data**: Enter unstructured text (one document per line)
2. **Select Model**: Choose Gemma3 model size (270m, 1b, 4b)
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

### Sample Data

```
Balu is a boy. He likes blue color and curd rice.
Ram is a boy. He likes red color and briyani.
Sheela is a girl. She likes orange color and curd rice.
Sunita is a girl. She likes blue color and chicken bryani.
```

## 🤖 Using with AI Tools (Claude Code)

This project is **optimized for AI-assisted development**, especially with [Claude Code](https://claude.com/claude-code). The `CLAUDE.md` file contains comprehensive guidelines for maintaining consistency when adding new content or features.

### Why Use AI Tools?

- **Rapid Content Creation**: Generate new learning modules with interactive visualizations
- **Consistent Design**: AI follows design system automatically via CLAUDE.md
- **Code Quality**: Reusable patterns and best practices built-in
- **Documentation**: Auto-generated inline documentation

### Getting Started with Claude Code

1. **Install Claude Code** following the [official documentation](https://docs.claude.com/claude-code)

2. **Open the project** in your terminal:
   ```bash
   cd llm-semantic-search
   claude
   ```

3. **Use the design guidelines**: Claude Code automatically reads `CLAUDE.md` and follows the design system, slide carousel format, and coding conventions.

### Example Prompts for Claude Code

**Adding New Learning Content:**
```
Create a new slide-based learning page about "cosine similarity"
following the design system in CLAUDE.md. Include:
- 8-10 focused slides
- Interactive canvas visualization showing vector similarity
- Real-world examples from semantic search
- Key takeaways slide
```

**Adding New Demos:**
```
Create a new demo showing multi-modal search (text + images)
following the existing demo patterns. Use the TypesenseService
and OllamaService.
```

**Enhancing Existing Pages:**
```
Add an interactive visualization to the embeddings.html page
showing how word embeddings cluster in 2D space using t-SNE.
Follow the carousel slide format.
```

### AI Development Workflow

1. **Read CLAUDE.md**: AI understands design system, color palette, layout patterns
2. **Follow existing patterns**: Services, API endpoints, and UI components
3. **Maintain consistency**: Automatic adherence to typography, spacing, carousel structure
4. **Generate tests**: Create test cases following `test_demo.py` pattern

### Key Files for AI Context

- **CLAUDE.md**: Complete design system, slide format, coding conventions
- **DEMO_README.md**: Architecture and demo patterns
- **services/**: Service layer patterns for reuse
- **templates/vectors.html**: Reference implementation of slide carousel

### Contributing with AI

When contributing with AI assistance:

1. **Review CLAUDE.md** before generating new content
2. **Test locally** - Run `python3 app.py` to verify
3. **Follow slide format** - Use carousel navigation for learning pages
4. **Update documentation** - Keep README and CLAUDE.md in sync
5. **Run tests** - `./venv/bin/python test_demo.py`

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🔧 API Documentation

### Health Check
```bash
GET /api/health
```

Returns status of Typesense and Ollama connections.

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
  }],
  "recreate": true
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

See [DEMO_README.md](DEMO_README.md) for complete API documentation.

## 🧪 Testing

Run the included test suite:

```bash
./venv/bin/python test_demo.py
```

This tests:
- ✅ Typesense connectivity
- ✅ Ollama availability
- ✅ Text structuring
- ✅ Document storage
- ✅ Natural language queries

## 🤝 Contributing

Contributions are welcome! This project is designed to be educational and collaborative.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Read CLAUDE.md** for design guidelines (especially important for UI changes)
4. **Make your changes**
5. **Test thoroughly**: Run `python3 app.py` and test manually
6. **Run tests**: `./venv/bin/python test_demo.py`
7. **Commit your changes**: `git commit -m 'Add amazing feature'`
8. **Push to the branch**: `git push origin feature/amazing-feature`
9. **Open a Pull Request**

### Contribution Ideas

- 📚 **New learning modules**: Attention mechanisms, transformer architecture, RAG
- 🎨 **Interactive visualizations**: More canvas-based demos
- 🔍 **Search improvements**: Hybrid search, reranking, filters
- 🌐 **Multi-language support**: i18n for international learners
- 📱 **Mobile optimization**: Responsive improvements
- 🧪 **Testing**: Unit tests, integration tests
- 📖 **Documentation**: Tutorials, guides, videos

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🐛 Troubleshooting

### Typesense Connection Error

**Error**: `Cannot connect to Typesense at localhost:8108`

**Solution**:
1. Check if Typesense is running: `curl http://localhost:8108/health`
2. Restart Typesense
3. Verify port 8108 is not in use: `lsof -i :8108`

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

### Module Not Found

**Error**: `ModuleNotFoundError: No module named 'typesense'`

**Solution**:
```bash
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt
```

## 🌐 Browser Compatibility

Tested and working on:
- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Typesense](https://typesense.org/)** - Fast, typo-tolerant search engine with vector search
- **[Ollama](https://ollama.ai/)** - Run large language models locally
- **[Google Gemma](https://ai.google.dev/gemma)** - Open language models
- **[Flask](https://flask.palletsprojects.com/)** - Python web framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/llm-semantic-search/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/llm-semantic-search/discussions)
- **Email**: your.email@example.com

## 🌐 Hosting on GitHub Pages

**Want to view the learning slides online without installing anything?**

This project includes a static version that can be hosted on GitHub Pages!

### What Works as Static Pages?

✅ **All Learning Modules** (slide presentations work perfectly):
- Knowledge Encoding
- Understanding LLMs
- Text Chunking Strategies
- Vector Databases
- Semantic Search & RAG

❌ **Interactive Demos** (require local Flask/Ollama/Typesense setup)

### Quick Setup

1. **Convert templates to static HTML**:
   ```bash
   python3 convert_to_static.py
   ```

2. **Push to GitHub**:
   ```bash
   git add docs/
   git commit -m "Add static site for GitHub Pages"
   git push origin main
   ```

3. **Enable GitHub Pages**:
   - Go to **Settings → Pages**
   - Source: **Deploy from a branch**
   - Branch: `main`, Folder: `/docs`
   - Save

4. **Visit your site**: `https://YOUR-USERNAME.github.io/llm-semantic-search/`

**Full instructions**: See [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md)

## 🗺️ Roadmap

- [x] GitHub Pages static hosting
- [ ] Add more LLM model support (GPT, Claude, etc.)
- [ ] Implement RAG (Retrieval Augmented Generation) demo
- [ ] Add multi-modal search (text + images)
- [ ] Create video tutorials
- [ ] Deploy live demo
- [ ] Add Jupyter notebooks for experiments
- [ ] Build REST API client libraries (Python, JS)

---

**Built with ❤️ for learning and exploration of semantic search with LLMs**

**Star ⭐ this repo if you find it useful!**
