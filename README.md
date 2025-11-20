# 🚀 LangGraph Extract Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)

**Production-ready extraction pipeline** using LangExtract, LangGraph, and MinIO for structured German business data extraction from Impressum/About pages.

## ✨ Features

- 🤖 **LangExtract Integration** - Google's structured extraction with German business prompts
- 🔄 **LangGraph Workflow** - State-based orchestration
- 📦 **MinIO Storage** - S3-compatible object storage
- ⚡ **Parallel Processing** - 5 workers with thread pool
- 🔁 **Retry Logic** - Exponential backoff (3 attempts)
- 🚦 **Rate Limiting** - API quota protection (20 req/min)
- 📊 **Statistics** - Real-time metrics & JSON reports
- 🐳 **Docker Ready** - Full containerization
- 🔌 **Model Flexibility** - Gemini API or Ollama (local)

## 🚀 Quick Start

### Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/MrBozkay/langraph_extract_agent.git
cd langraph_extract_agent

# Configure environment
cp .env.example .env
# Edit .env with your GOOGLE_API_KEY and MinIO credentials

# Run with Docker
docker-compose up --build
```

### Manual Setup

```bash
# Setup virtual environment
./setup_venv.sh
source venv/bin/activate

# Configure
cp .env.example .env
nano .env  # Add your credentials

# Run production batch
python src/agents/run_batch_production.py
```

## 📊 Agent Selection

| Agent | Use Case | Speed | Features |
|-------|----------|-------|----------|
| **Production Batch** | Production deployment | ⚡⚡⚡ | Parallel, Retry, Rate limit |
| **LangGraph** | State tracking | ⚡ | Workflow visualization |
| **Simple Batch** | Testing/Debug | ⚡ | Easy to understand |

**💡 Recommendation**: Use `run_batch_production.py` for production.

## 🎯 Example Output

```json
{
  "owner_name": "Hans Müller",
  "position": "Geschäftsführer",
  "company_name": "Mustermann GmbH",
  "email": "h.mueller@mustermann.de",
  "phone": "+49 123 456789",
  "website": "www.mustermann.de",
  "sector": "Consulting"
}
```

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md) - 5-minute setup
- [Agent Selection Guide](AGENT_GUIDE.md) - Choose the right agent
- [Production Deployment](PRODUCTION.md) - Production best practices
- [Contributing](CONTRIBUTING.md) - How to contribute

## 🔧 Configuration

```bash
# MinIO (Remote or Local)
MINIO_ENDPOINT=your-minio-server:9000
MINIO_ACCESS_KEY=your-access-key
MINIO_SECRET_KEY=your-secret-key
MINIO_BUCKET_NAME=your-bucket

# LLM Model
GOOGLE_API_KEY=your-gemini-api-key
LANGEXTRACT_MODEL=gemini-2.0-flash-exp

# Production Settings
EXTRACTION_MAX_WORKERS=5
EXTRACTION_RETRY_COUNT=3
RATE_LIMIT_REQUESTS_PER_MINUTE=20
```

## 🐳 Docker Commands

```bash
# Build image
docker build -t langraph-extract-agent .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f extraction-app

# Stop
docker-compose down
```

## 🧪 Testing

```bash
# Test MinIO connection
python test_minio.py

# Test extraction
python test_extraction.py

# Test production features
python test_production_features.py
```

## 📈 Performance

- **Processing Speed**: ~2-3 files/second (5 workers)
- **Success Rate**: >95% (with retry logic)
- **Extraction Time**: ~2-5 seconds per file

## 🔄 Ollama Support

Switch to local inference:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull gpt-oss:20b

# Update .env
LANGEXTRACT_MODEL=ollama/gpt-oss:20b
```

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangExtract](https://github.com/google/langextract) - Google's extraction library
- [LangGraph](https://github.com/langchain-ai/langgraph) - Workflow orchestration
- [MinIO](https://min.io/) - S3-compatible object storage

---

**Built with ❤️ for German business data extraction**
