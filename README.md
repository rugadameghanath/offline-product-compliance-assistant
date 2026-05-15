# Offline Product & Compliance Assistant (OPCA)

A fully local, offline RAG system for banking RFPs, policies, and compliance documents. Runs on your laptop – no data leaves your machine.

## Features
- Ingest PDFs, DOCX, TXT from any folder
- Web UI for ingestion, audit, and Q&A
- Compare RFPs (e.g., Org A vs Org B) with markdown tables
- Fully offline after initial setup

## Requirements
- Python 3.8+
- Ollama (with llama3.2:3b or similar)
- 8GB+ RAM

## Quick Start
1. Clone repo
2. `pip install -r requirements.txt`
3. `ollama pull llama3.2:3b`
4. Double-click `start_server.bat`
5. Open browser to `http://localhost:5000`

## Usage
- **Ingest** – paste a file/folder path, click Ingest
- **Audit** – view all ingested files with page/word counts
- **Query** – ask questions (e.g., "Compare RFP requirements for behavioral biometrics between two vendors")

## License
MIT