# Quick Start Guide

## 🚀 5-Minute Setup

### 1. Clone & Setup
```bash
cd langraph_extract_agent
./setup_venv.sh
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 3. Start MinIO
```bash
docker-compose up -d minio
# Access console: http://localhost:9001 (minioadmin/minioadmin)
```

### 4. Create Sample Data
```bash
source venv/bin/activate
python create_sample_data.py
```

### 5. Run Extraction

**Choose the right agent for your needs:**

#### 🏆 Production (Recommended)
```bash
python src/agents/run_batch_production.py
```
✅ Parallel processing • ✅ Retry logic • ✅ Rate limiting • ✅ Full logging

#### 🔄 LangGraph Workflow
```bash
python src/agents/about_graph.py
```
✅ State management • ✅ Workflow visualization • ⚠️ Sequential

#### 🔧 Simple Testing
```bash
python src/agents/run_about_extraction.py
```
✅ Easy to debug • ⚠️ No retry • ⚠️ Sequential

**💡 Tip**: Use **Production Batch** for real deployments!

### 6. Verify Results
Check MinIO console for `.about.json` files or:
```bash
python test_minio.py
```

## 📊 Expected Output

```
🚀 Starting LangGraph extraction workflow...

📁 Listing markdown files from MinIO...
✓ Found 3 markdown files

[1/3] Processing: scraped-content/example.de/impressum.md
✓ Extracted: Mustermann Consulting GmbH
✓ Uploaded: scraped-content/example.de/impressum.about.json

============================================================
📊 Extraction Summary:
  ✅ Successful: 3
  ⏭️  Skipped: 0
  ❌ Errors: 0
  📁 Total: 3
============================================================
```

## 🧪 Testing

```bash
# Test MinIO connection
python test_minio.py

# Test extraction with samples
python test_extraction.py
```

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.
