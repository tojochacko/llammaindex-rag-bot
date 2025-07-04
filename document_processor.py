from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import chromadb
from llama_index.core import Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import SentenceSplitter


# Define the embedding model
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")


# Load the documents in a Python list
reader = SimpleDirectoryReader(input_dir="daata", recursive=True)
documents = []
for docs in reader.iter_data(True):
    # <do something with the documents per file>
    documents.extend(docs)


# Initialize ChromaDB client
index_name = "quickstart" # TODO: How do I make this dynamic?

# set up ChromaVectorStore and load in data
db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection(index_name)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


# define the splitting strategy
text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)
Settings.text_splitter = text_splitter

index = VectorStoreIndex.from_documents(
    documents, 
    storage_context=storage_context,
    transformations=[text_splitter])
