# Decanote
Decanote is an AI-powered code auditing tool leveraging Google Gemini. It intelligently batches files into chunks to perform systematic, large-scale codebase analysis without hitting LLM context limits.

## Key Features
- **Smart Chunking:** Processes large projects by grouping files (default: 20 per batch).
- **Format Agnostic:** Audits multiple file types with configurable rules.
- **Export Capabilities:** Generate detailed reports in `.xlsx` and `.docx` formats.
- **Testing:** Comprehensive test suite included using `pytest`.

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env 
# Add your GEMINI_API_KEY to .env
python run.py
```

## Architecture
- `app/api`: Request handling.
- `app/core`: Logic for chunking, file filtering, and AI integration.
- `app/export`: Report generation modules.
- `config/rules.json`: Fine-tune auditing parameters and supported file extensions.

## Testing
Run the audit logic tests:
```bash
pytest
```

## Security Notice
Ensure that the directory being scanned does not contain sensitive configuration files that you do not intend to share with the AI provider. Always sanitize your environment variables.