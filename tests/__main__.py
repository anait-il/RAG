from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline, HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb


model_name = "Qwen/Qwen3-0.6B"
embedding_model = "all-MiniLM-L6-v2"
path = "vllm-0.10.1"

model = AutoModelForCausalLM.from_pretrained(model_name,
                                             torch_dtype="auto",
                                             device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_name)

hf_pipeline = pipeline("text-generation",
                       model=model,
                       tokenizer=tokenizer)
llm = HuggingFacePipeline(pipeline=hf_pipeline)


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
    
    return chunks

def index_chunks(chunks):
    texts = [doc.page_content for doc in chunks]
    embidding_model = HuggingFaceEmbeddings(model_name=embedding_model,
                                            model_kwargs={"device": "cpu"})
    vectors = embidding_model.embed_documents(texts)
    print(type(vectors))
    client = chromadb.PersistentClient("./chramdb")
    collection = client.create_collection(name="data")
    collection.add(
        embeddings=vectors,
        ids=[f"chunk {i}" for i,_ in enumerate(vectors)]
    )
    return collection

def main():
    print("\nhello from RAG...")

    docs = load_documents()
    document_chunks = split_documents(docs)
    chroma_vectors = index_chunks(document_chunks)
    print(type(chroma_vectors))


if __name__ == "__main__":
    main()
