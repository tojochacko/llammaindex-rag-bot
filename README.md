# LlamaIndex RAG Bot

A Retrieval-Augmented Generation (RAG) chatbot built with LlamaIndex, using Ollama for local LLM inference and ChromaDB for vector storage.

## Overview

This project implements a document-based question-answering system that:
- Processes documents from a local directory
- Creates embeddings using Ollama's `nomic-embed-text` model
- Stores vectors in ChromaDB for efficient retrieval
- Uses Ollama's `gemma3` model for response generation
- Provides an interactive chat interface

## Project Structure

```
llammaindex-rag-bot/
├── .gitignore
├── chat_interface.py      # Interactive chat interface
├── document_processor.py  # Document ingestion and indexing
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- Required Ollama models:
  - `nomic-embed-text` (for embeddings)
  - `gemma3` (for text generation)

### Installing Ollama Models

```bash
ollama pull nomic-embed-text
ollama pull gemma3
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd llammaindex-rag-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Document Processing

First, prepare your documents:

1. Create a `daata` directory in the project root
2. Place your documents (PDF, TXT, etc.) in the `daata` directory
3. Run the document processor:

```bash
python document_processor.py
```

This will:
- Read all documents from the `daata` directory recursively
- Split text into chunks (512 characters with 10-character overlap)
- Generate embeddings using the `nomic-embed-text` model
- Store vectors in ChromaDB (`./chroma_db` directory)

### 2. Interactive Chat

Start the chat interface:

```bash
python chat_interface.py
```

- Type your questions and press Enter
- The system will retrieve relevant document chunks and generate responses
- Type 'exit' or 'quit' to end the session
- Each response includes source information and relevance scores

## Configuration

### Embedding Model
- Model: `nomic-embed-text` (via Ollama)
- Configurable in both `chat_interface.py` and `document_processor.py`

### Language Model
- Model: `gemma3` (via Ollama)
- Request timeout: 120 seconds
- JSON mode enabled
- Configurable in `chat_interface.py`

### Text Splitting
- Chunk size: 512 characters
- Chunk overlap: 10 characters
- Uses SentenceSplitter from LlamaIndex

### Vector Store
- Database: ChromaDB
- Collection name: "quickstart"
- Storage path: `./chroma_db`

## Key Features

- **Local Processing**: Uses Ollama for completely local LLM inference
- **Document Support**: Handles various document formats through LlamaIndex readers
- **Efficient Retrieval**: ChromaDB for fast vector similarity search
- **Source Attribution**: Shows source documents and relevance scores
- **Customizable Prompts**: Uses RichPromptTemplate for flexible prompt engineering

## File Descriptions

### `document_processor.py`
- Handles document ingestion and preprocessing
- Creates vector embeddings and stores them in ChromaDB
- Configures text splitting strategy
- Run once to process your document collection

### `chat_interface.py`
- Interactive chat interface for querying the knowledge base
- Loads existing vector index from ChromaDB
- Implements query engine with custom prompt templates
- Displays responses with source attribution

## Development Notes

The codebase includes several TODOs for future improvements:

- [ ] Implement Ingestion pipeline for better document handling
- [ ] Setup Poetry virtual environment
- [ ] Add model performance evaluation
- [ ] Implement step-back prompting techniques
- [ ] Explore Agentic RAG for improved search
- [ ] Add document grading strategies
- [ ] Make index name dynamic
- [ ] Convert query engine to retriever pattern

## Troubleshooting

### Common Issues

1. **Ollama models not found**: Ensure Ollama is running and models are pulled
2. **ChromaDB errors**: Check that the `chroma_db` directory is writable
3. **No documents found**: Verify documents are in the `daata` directory
4. **Memory issues**: Reduce chunk size or process documents in batches

### Dependencies

The project uses several key libraries:
- `llama-index`: Core RAG framework
- `chromadb`: Vector database
- `ollama`: Local LLM integration
- `transformers`: For tokenization utilities

## License

[Add your license information here]

## Contributing

[Add contributing guidelines here]
