import sys
from rag_client import get_relevant_context

def test_rag():
    try:
        print("Loading local Nomic model and connecting to ChromaDB...")
        # A test query about a common plant issue
        query = "why are the tips of my aloe vera turning brown?"
        context = get_relevant_context(query, n_results=1)
        
        if context:
            print("\n✅ RAG query successful! Top result context:")
            print("-" * 50)
            print(context)
            print("-" * 50)
        else:
            print("\n✅ Connection successful, but no documents were found matching the query.")
            
    except Exception as e:
        print(f"\n❌ RAG test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_rag()
