from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline, HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from langchain_community.retrievers import BM25Retriever

model_name = "Qwen/Qwen3-0.6B"
embedding_model_name = "all-MiniLM-L6-v2"
path = "vllm-0.10.1"

model = AutoModelForCausalLM.from_pretrained(model_name,
                                             torch_dtype="auto",
                                             device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_name)

hf_pipeline = pipeline("text-generation",
                       model=model,
                       tokenizer=tokenizer,
                       max_new_tokens=10)
llm = HuggingFacePipeline(pipeline=hf_pipeline)
embidding_model = HuggingFaceEmbeddings(model_name=embedding_model_name,
                                        model_kwargs={"device": "cpu"})

def load_documents():
    
    loader = DirectoryLoader(path,
                glob=["**/*.txt", "**/*.md"],
                show_progress=True,
                silent_errors=True,
                loader_cls=TextLoader
                )

    documents = loader.load()

    return documents

def split_documents(docs):
    chunks = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    for i, doc in enumerate(chunks):
        doc.id = i
    return chunks

def index_chunks(chunks):
    texts = [doc.page_content for doc in chunks]
    vectors = embidding_model.embed_documents(texts)
    client = chromadb.PersistentClient("./chromdb")
    collection = client.get_or_create_collection(name="data")
    collection.add(
        documents=texts,
        embeddings=vectors,
        ids=[f"chunk {i}" for i,_ in enumerate(vectors)],
        metadatas=[doc.metadata for doc in chunks]
    )
    # print(collection.get())
    return collection

def main():
    print("\nhello from RAG...")

    # indexing
    docs = load_documents()
    document_chunks = split_documents(docs)
    chroma_vectors = index_chunks(document_chunks)

    # retrieval
    query = "What HTTP endpoint is used to dynamically load a LoRA adapter in vLLM?"
    embedding_query = embidding_model.embed_query(query)
    results = chroma_vectors.query(query_embeddings=[embedding_query],
                                   n_results = 5)
    context = "\n\n".join(doc[0] for doc in results["documents"])

    prompt = f"""Answer the question using the context below.

If the context does not contain the answer, say you don't know.

Context:
{context}

Question:
{query}

Answer:"""

    # print(llm.invoke(prompt))
    ids = results["ids"][0]
    print(results)


if __name__ == "__main__":
    main()
