from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from transformers import AutoTokenizer
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.prompts import RichPromptTemplate
from llama_index.core import Settings


# from llama_index.response.pprint_utils import pprint_response

# TODOs:
# TODO: Use Ingestion pipeline to handle the documents
# TODO: Setup Poetry virtual environment
# TODO: Evaluation of the model performance
# TODO: Step-back prompting. How to convert user's question into a prompt template that can elevate model performance?
# TODO: Agentic R.A.G - how can we use Agentic R.A.G to improve search techniques?
# TODO: How to grade documents? What are the Grading strategies?


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
query_engine = index.as_query_engine() # TODO: How do I convert this to a retriever and what is the difference between a retriever and query engine?


template_str = """We have provided context information below.
---------------------
{{ context_str }}
---------------------
Given this information, please answer the question: {{ query_str }}
"""
qa_template = RichPromptTemplate(template_str)

while True:
    question = input("Ask a question (or 'exit'): ").strip()
    if question.lower() in {"exit", "quit"}:
        break
    prompt = qa_template.format(query_str=question)
    print(prompt)
    response = query_engine.query(prompt) # TODO: Convert this to a prompt template
    print(response)
    # response.print_response_stream()

    for node in response.source_nodes:
        print("-----")
        text_fmt = node.node.get_content().strip().replace("\n", " ")[:1000]
        print(f"Text:\t {text_fmt} ...")
        print(f"Metadata:\t {node.node.metadata}")
        print(f"Score:\t {node.score:.3f}")
