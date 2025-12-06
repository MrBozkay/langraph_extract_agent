# Agent Development Guide
When you need to search docs, use `context7` tools.
If you are unsure how to do something, use `gh_grep` to search code examples from github.


## Build/Test Commands
```bash
# Setup environment
./setup_venv.sh && source venv/bin/activate

# Run single test
python test_extraction.py          # Test extraction logic
python test_minio.py              # Test MinIO connectivity  
python test_production_features.py # Test production features

# Run agents
python src/agents/run_batch_production.py  # Production batch processor
python src/agents/about_graph.py          # LangGraph workflow
python src/agents/about_extractor.py      # Simple extractor
```

## Code Style Guidelines
- **Imports**: Use absolute imports from project root (`from src.agents.about_extractor import AboutExtractor`)
- **Formatting**: Follow PEP 8, use type hints for all function parameters/returns
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Error Handling**: Use try/except with descriptive error messages, return None for extraction failures
- **Docstrings**: Use triple quotes with Args/Returns sections for all public methods
- **Configuration**: Use `src.config.settings` for all environment variables
- **Models**: Use Pydantic models from `src.models.schemas` for structured data
- **Logging**: Use print statements with emoji prefixes (✅, ❌, ⚠️, 📊) for user feedback
- **German Content**: All prompts and examples should be in German for business extraction