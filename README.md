# Enterprise Extraction Pipeline

🚀 **Production-ready extraction pipeline** using LangExtract, LangGraph, and MinIO for structured German business data extraction.

## 🎯 Features

- **LangExtract Integration**: Google's structured extraction library with German business prompts
- **LangGraph Workflow**: State-based orchestration with automatic retry and error handling
- **MinIO Storage**: Object storage for markdown inputs and JSON outputs
- **Docker Support**: Full containerization with docker-compose
- **Model Flexibility**: Easy switching between Gemini API and Ollama (local inference)

## 📋 Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   MinIO     │─────▶│  LangExtract │─────▶│   MinIO     │
│ (.md files) │      │  + LangGraph │      │ (.json out) │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ Gemini API / │
                     │   Ollama     │
                     └──────────────┘
```

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
# Run automated setup
./setup_venv.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit with your credentials
nano .env
```

Required environment variables:
- `GOOGLE_API_KEY`: Your Gemini API key
- `MINIO_ENDPOINT`: MinIO server address (default: localhost:9000)
- `MINIO_ACCESS_KEY`: MinIO access key
- `MINIO_SECRET_KEY`: MinIO secret key

### 3. Start MinIO (Docker)

```bash
# Start MinIO only
docker-compose up -d minio

# Access MinIO console at http://localhost:9001
# Login: minioadmin / minioadmin
```

### 4. Run Extraction

We provide **3 different agents** for different use cases:

#### 🏆 **Production Batch (Recommended)**
```bash
python src/agents/run_batch_production.py
```
**Best for**: Production deployment, large datasets  
**Features**:
- ✅ Parallel processing (5 workers)
- ✅ Retry logic with exponential backoff
- ✅ Rate limiting (API quota protection)
- ✅ Comprehensive logging (file + console)
- ✅ Statistics tracking & JSON reports
- ✅ Error isolation per file

**When to use**: Always use this for production deployments and processing large batches of files.

---

#### 🔄 **LangGraph Workflow**
```bash
python src/agents/about_graph.py
```
**Best for**: State-based workflows, complex orchestration  
**Features**:
- ✅ State management (TypedDict)
- ✅ Conditional edges (dynamic routing)
- ✅ Visual workflow debugging
- ✅ Statistics tracking
- ⚠️ Sequential processing (slower)

**When to use**: When you need state tracking, workflow visualization, or plan to add complex conditional logic.

---

#### 🔧 **Simple Batch Runner**
```bash
python src/agents/run_about_extraction.py
```
**Best for**: Testing, debugging, small batches  
**Features**:
- ✅ Simple, easy to understand
- ✅ Basic statistics
- ⚠️ No retry logic
- ⚠️ No rate limiting
- ⚠️ Sequential processing

**When to use**: Quick tests, debugging extraction issues, or processing small batches (<10 files).

---

### 📊 Agent Comparison

| Feature | Production Batch | LangGraph | Simple Batch |
|---------|-----------------|-----------|--------------|
| **Speed** | ⚡⚡⚡ (Parallel) | ⚡ (Sequential) | ⚡ (Sequential) |
| **Retry Logic** | ✅ 3 attempts | ❌ | ❌ |
| **Rate Limiting** | ✅ 20 req/min | ❌ | ❌ |
| **Logging** | ✅ File + Console | ⚠️ Print only | ⚠️ Print only |
| **Statistics** | ✅✅ Detailed + JSON | ✅ Basic | ✅ Basic |
| **Error Handling** | ✅ Isolated | ⚠️ Basic | ⚠️ Basic |
| **Production Ready** | ✅✅ | ⚠️ | ❌ |

**💡 Recommendation**: Use **Production Batch** for all production deployments. Use **LangGraph** if you need state management. Use **Simple Batch** only for testing.

## 🐳 Docker Deployment

### Full Stack (MinIO + Extraction App)

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f extraction-app

# Stop services
docker-compose down
```

### Custom Commands

```bash
# Run batch extraction
docker-compose run extraction-app python src/agents/run_about_extraction.py

# Run LangGraph workflow
docker-compose run extraction-app python src/agents/about_graph.py
```

## 📊 Data Flow

1. **Input**: Markdown files in MinIO at `scraped-content/{domain}/{page}.md`
2. **Processing**: LangExtract extracts German business information
3. **Output**: JSON files at `scraped-content/{domain}/{page}.about.json`

### Example Output

```json
{
  "owner_name": "Hans Müller",
  "position": "Geschäftsführer",
  "company_name": "Mustermann GmbH",
  "email": "h.mueller@mustermann.de",
  "phone": "+49 123 456789",
  "fax": "+49 123 456788",
  "website": "www.mustermann.de",
  "profession": "",
  "sector": "Consulting"
}
```

## 🔄 Migration: Gemini → Ollama

To switch from Gemini API to local Ollama:

### 1. Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull gpt-oss:20b model
ollama pull gpt-oss:20b
```

### 2. Update Configuration

```bash
# In .env file
LANGEXTRACT_MODEL=ollama/gpt-oss:20b
OLLAMA_BASE_URL=http://localhost:11434
```

### 3. Install Ollama Dependencies

```bash
pip install langchain-community ollama
```

No code changes required! The extractor automatically detects the model type.

## 🧪 Testing

### Test MinIO Connection

```python
from src.modules.minio_manager import MinIOManager

minio = MinIOManager()
print(minio.list_objects())
```

### Test Extraction

```python
from src.agents.about_extractor import AboutExtractor

extractor = AboutExtractor()
text = """
Impressum
Mustermann GmbH
Geschäftsführer: Hans Müller
E-Mail: h.mueller@mustermann.de
"""

result = extractor.extract_from_markdown_text(text)
print(result)
```

## 📁 Project Structure

```
.
├── src/
│   ├── agents/
│   │   ├── about_extractor.py          # Basic LangExtract wrapper
│   │   ├── about_extractor_v2.py       # Production extractor (retry, rate limit)
│   │   ├── about_graph.py              # LangGraph workflow
│   │   ├── run_about_extraction.py     # Simple batch runner
│   │   └── run_batch_production.py     # Production batch (parallel)
│   ├── modules/
│   │   ├── minio_manager.py            # MinIO client
│   │   ├── logger.py                   # Logging system
│   │   ├── retry_handler.py            # Retry & rate limiting
│   │   └── statistics.py               # Statistics tracking
│   ├── models/
│   │   └── schemas.py                  # Pydantic models
│   └── config/
│       └── settings.py                 # Configuration
├── logs/                               # Log files & statistics
├── test_minio.py                       # MinIO connectivity test
├── test_extraction.py                  # Extraction test
├── test_production_features.py         # Production features test
├── create_sample_data.py               # Sample data generator
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── setup_venv.sh
├── .env.example
├── README.md                           # This file
├── QUICKSTART.md                       # Quick start guide
├── PRODUCTION.md                       # Production deployment guide
└── SUMMARY.md                          # Turkish summary
```

## 🔮 Future Enhancements

### Knowledge Graph Integration

Add Neo4j or Dgraph for relationship mapping:

```bash
# Install Neo4j driver
pip install neo4j

# Update docker-compose.yml to include Neo4j service
```

See `docs/knowledge-graph.md` for implementation guide (coming soon).

## 🐛 Troubleshooting

### MinIO Connection Error

```bash
# Check MinIO is running
docker-compose ps

# Restart MinIO
docker-compose restart minio
```

### Gemini API Rate Limits

```bash
# Reduce batch size in .env
EXTRACTION_BATCH_SIZE=5

# Add retry delay in settings.py
```

### Extraction Quality Issues

- Add more few-shot examples in `about_extractor.py`
- Adjust prompt in `ABOUT_PROMPT`
- Try different model: `gemini-2.0-flash-exp` vs `gemini-1.5-pro`

## 📚 Resources

- [LangExtract Documentation](https://github.com/google/langextract)
- [LangGraph Guide](https://langchain-ai.github.io/langgraph/)
- [MinIO Python SDK](https://min.io/docs/minio/linux/developers/python/minio-py.html)

## 📄 License

MIT License - feel free to use in your projects!

---

**Built with ❤️ using LangExtract, LangGraph, and MinIO**
