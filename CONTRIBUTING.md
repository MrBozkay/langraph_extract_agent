# Contributing to LangGraph Extract Agent

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs
- Include reproduction steps
- Provide environment details (OS, Python version, etc.)

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Keep functions focused and small

### Testing
- Add tests for new features
- Ensure all tests pass before submitting PR
- Test with both Gemini API and Ollama (if applicable)

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/langraph_extract_agent.git
cd langraph_extract_agent

# Setup virtual environment
./setup_venv.sh
source venv/bin/activate

# Install dev dependencies
pip install -r requirements.txt

# Run tests
python test_minio.py
python test_extraction.py
python test_production_features.py
```

## Questions?

Feel free to open an issue for questions or discussions!
