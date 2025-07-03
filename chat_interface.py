from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from transformers import AutoTokenizer
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_indẻx.core import VectorStoreIndex
from llama_index.core import Settings

# TODOs:
# TODO: Use Ingestion pipeline to handle the documents
# TODO: Setup Poetry virtual environment
# TODO: Evaluation of the model performance


# Define the embedding model
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
Settings.llm = Ollama(model="gemma3", request_timeout=120.0, json_mode=True)
# Update the tokenizer to use for the correct model
# Settings.tokenizer = AutoTokenizer.from_pretrained(
#     "/Users/tojochacko/.ollama/models"
# )


# load from disk
index_name = "quickstart" # TODO: How do I make this dynamic?
db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection(index_name)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(
    vector_store
)
query_engine = index.as_query_engine()

while True:
    question = input("Ask a question (or 'exit'): ").strip()
    if question.lower() in {"exit", "quit"}:
        break
    response = query_engine.query("Can you summarize the content of the documents?") # TODO: Convert this to a prompt template
    print(response)