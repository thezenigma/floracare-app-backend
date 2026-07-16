import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
import chromadb
from sentence_transformers import SentenceTransformer

class FloraCareRAG:
    def __init__(self):
        self.db_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
        self.client = None
        self.collection = None
        
        # Load local embedding model
        model_name = "nomic-ai/nomic-embed-text-v1.5"
        try:
            self.model = SentenceTransformer(model_name, trust_remote_code=True)
            print("Loaded Nomic Embedding Model successfully.")
        except Exception as e:
            print(f"Failed to load embedding model: {e}")
            self.model = None

        self._init_db()

    def _init_db(self):
        try:
            from chromadb.config import Settings
            self.client = chromadb.PersistentClient(path=self.db_dir, settings=Settings(anonymized_telemetry=False))
            self.collection = self.client.get_or_create_collection(name="plants")
            print(f"Connected to ChromaDB at {self.db_dir}")
        except Exception as e:
            print(f"WARNING: ChromaDB failed to initialize. RAG will not work. Error: {e}")

    def query(self, text_query: str, n_results: int = 3) -> str:
        if not self.collection or not self.model:
            return ""
            
        try:
            # Generate embedding for the query
            query_vector = self.model.encode([f"search_query: {text_query}"])[0].tolist()
            
            # Query the collection
            results = self.collection.query(
                query_embeddings=[query_vector],
                n_results=n_results
            )
            
            # Combine the retrieved text documents
            documents = results.get("documents", [[]])[0]
            return "\n\n".join(documents)
            
        except Exception as e:
            print(f"RAG query failed: {e}")
            return ""

# Initialize a global instance
rag_system = FloraCareRAG()

def get_relevant_context(query: str, n_results: int = 3) -> str:
    """Wrapper function to maintain compatibility with main.py"""
    return rag_system.query(query, n_results)
