from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from transformers import AutoTokenizer
import chromadb

from llama_index.core import Settings

# TODOs:
# - Make the index name dynamic based on the input directory or some other criteria
# - Implement a local embedding model
# - Implement a local LLM
# - Use Ingestion pipeline to handle the documents
# - Setup Poetry virtual environment
# - Evaluation of the model performance
# - Prompt templates for querying


# define the embedding model
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
Settings.llm = Ollama(model="gemma3", request_timeout=120.0, json_mode=True)
# update the tokenizer to use for the correct model
# Settings.tokenizer = AutoTokenizer.from_pretrained(
#     "/Users/tojochacko/.ollama/models"
# )
# define the splitting strategy
text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)
Settings.text_splitter = text_splitter

reader = SimpleDirectoryReader(input_dir="daata", recursive=True)
documents = []
for docs in reader.iter_data(True):
    # <do something with the documents per file>
    documents.extend(docs)

# Initialize ChromaDB client
chroma_client = chromadb.Client()
index_name = "my_index" # How do I make this dynamic?
collection = chroma_client.create_collection(index_name)

index = VectorStoreIndex.from_documents(
    documents,
    transformations=[text_splitter]
    )
query_engine = index.as_query_engine()

while True:
    question = input("Ask a question (or 'exit'): ").strip()
    if question.lower() in {"exit", "quit"}:
        break
    response = query_engine.query("Can you summarize the content of the documents?")
    print(response)