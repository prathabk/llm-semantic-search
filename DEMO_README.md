# Semantic Search Demo

Interactive demonstration of LLM-powered semantic search with Typesense.

## Features

✅ **Modular Architecture**: Clean separation of concerns with dedicated services
✅ **LLM Integration**: Use Ollama's Gemma3 models (270m, 1b, 4b) for text structuring
✅ **Vector Database**: Store and search documents using Typesense
✅ **Natural Language Queries**: Translate natural language to structured database queries
✅ **Interactive UI**: Step-by-step workflow with visual feedback

## Architecture

### Services

```
services/
├── __init__.py           # Service exports
├── ollama_service.py     # LLM text processing
└── typesense_service.py  # Vector database operations
```

#### OllamaService

Handles all interactions with Ollama for:
- **Text Structuring**: Convert unstructured text to structured JSON
- **Query Translation**: Translate natural language to Typesense filters
- **Model Selection**: Support for multiple Gemma3 model sizes

#### TypesenseService

Manages vector database operations:
- **Collection Management**: Create/delete collections with schemas
- **Document Storage**: Insert and manage documents
- **Search**: Query with filters and natural language
- **Health Checks**: Monitor Typesense availability

### API Endpoints

```
GET  /api/health       - Check Typesense connection
GET  /api/models       - List available Ollama models
POST /api/structure    - Structure text with LLM
POST /api/store        - Store documents in Typesense
POST /api/query        - Query with natural language
```

### Frontend

Three demo interfaces:

**1. Demo Hub** (`templates/demo.html`)
- Landing page with demo descriptions
- Quick action cards
- Navigation to specialized demos

**2. Full Pipeline Demo** (`templates/demo_full.html`)
- Step Indicator: Visual progress through workflow
- Status Banners: Real-time feedback
- Interactive Forms: Text input, model selection, query input
- Results Display: Answer first, then filter query and raw results

**3. Query Demo** (`templates/demo_query.html`)
- Simplified query interface
- Document cards with visual tags
- Example queries for quick testing
- Answer-first results layout
- Formatted JSON with syntax highlighting
- Copy-to-clipboard functionality

## Workflow

### 1. Input Data
- Enter unstructured text (one document per line)
- Select LLM model (gemma3:270m, 1b, or 4b)
- Load sample data option

### 2. Structure with LLM
- LLM extracts: name, gender, likes (color, food), text
- Displays structured JSON
- Shows document count and model used

### 3. Store in Typesense
- Creates/recreates collection with schema
- Flattens nested structures for filtering
- Inserts documents with IDs

### 4. Query
- Enter natural language query
- LLM translates to Typesense filter
- Displays:
  - Typesense query parameters
  - Raw search results
  - Natural language answer

## Schema

### Collection: llm-semantic-search

```json
{
  "name": "llm-semantic-search",
  "fields": [
    {"name": "name", "type": "string", "optional": true},
    {"name": "gender", "type": "string", "facet": true},
    {"name": "likes_color", "type": "string", "facet": true, "optional": true},
    {"name": "likes_food", "type": "string", "facet": true, "optional": true},
    {"name": "text", "type": "string"}
  ]
}
```

### Document Structure

```json
{
  "id": "1",
  "name": "Balu",
  "gender": "boy",
  "likes_color": "blue",
  "likes_food": "curd rice",
  "text": "Balu is a boy. He likes blue color and curd rice."
}
```

## Configuration

Environment variables (with defaults):

```bash
TYPESENSE_HOST=localhost
TYPESENSE_PORT=8108
TYPESENSE_API_KEY=vL1l1TOq2UYhPxKqJfvfWXvm0wIID6se
COLLECTION_NAME=llm-semantic-search
```

## Usage

### Start the Application

```bash
./venv/bin/python app.py
```

### Access the Demos

**Demo Hub**: http://localhost:9010/demo

From the hub, you can access:
- **Full Pipeline Demo** (`/demo/full`) - Complete workflow from data input to query
- **Query Demo** (`/demo/query`) - Simplified search interface for pre-loaded data

### Run Tests

```bash
./venv/bin/python test_demo.py
```

### Sample Data

```
Balu is a boy. He likes blue color and curd rice.
He like red color and his name is Babluo, but he always eats sambar rice.
Ram is a boy. He likes red color and briyani.
Bob sometimes eats curd rice but most of the time he prefers briyani while eating he always wears yellow dress
Sheela is a girl. She likes orange color and curd rice.
Sunita is a girl. She likes blue color and chicken bryani.
```

### Example Queries

- "how many boys like blue color"
- "who likes red color"
- "girls who like biryani"
- "find people who like curd rice"

## API Examples

### Structure Text

```bash
curl -X POST http://localhost:9010/api/structure \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Balu is a boy. He likes blue color and curd rice."],
    "model": "gemma3:1b"
  }'
```

### Store Documents

```bash
curl -X POST http://localhost:9010/api/store \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [{
      "name": "Balu",
      "gender": "boy",
      "likes": {"color": "blue", "food": "curd rice"},
      "text": "Balu is a boy. He likes blue color and curd rice."
    }],
    "recreate": true
  }'
```

### Query

```bash
curl -X POST http://localhost:9010/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "how many boys like blue color",
    "model": "gemma3:1b"
  }'
```

## Design System

Following the CLAUDE.md design system:
- **Primary Color**: #2563eb (blue)
- **Surface**: #ffffff (white cards)
- **Background**: #f8fafc (light gray)
- **Typography**: System fonts with clear hierarchy

## Key Features

### Modular & Reusable
- Services can be used independently
- Configuration through environment variables
- No hardcoded values

### Error Handling
- Comprehensive try-catch blocks
- User-friendly error messages
- Timeout handling for LLM calls

### User Experience
- Visual step indicators
- Loading spinners during processing
- Status banners for feedback
- Sample data for quick testing
- Keyboard-friendly forms

## Future Enhancements

Possible improvements:
- [ ] Support for more LLM models
- [ ] Batch query processing
- [ ] Export results to CSV/JSON
- [ ] Query history
- [ ] Document editing/deletion
- [ ] Advanced filter builder
- [ ] Semantic similarity search
- [ ] Vector embeddings visualization

## Testing

The test suite (`test_demo.py`) validates:
1. Typesense connectivity
2. Model availability
3. Text structuring with LLM
4. Document storage
5. Natural language queries

All tests pass successfully! ✅

## Technologies

- **Backend**: Flask (Python)
- **LLM**: Ollama (Gemma3 models)
- **Database**: Typesense
- **Frontend**: Vanilla JavaScript
- **Styling**: CSS with design system variables

## Notes

- Nested objects are automatically flattened for Typesense compatibility
- LLM responses may vary - using smaller models for speed
- Collection is recreated on each data load
- Query translation depends on LLM interpretation

---

**Version**: 1.0
**Status**: Production Ready
**Last Updated**: 2025-11-04
